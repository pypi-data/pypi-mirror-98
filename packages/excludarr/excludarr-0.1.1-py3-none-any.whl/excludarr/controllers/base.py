from cement import Controller, ex
from cement import shell
from cement.utils.version import get_version_banner
from ..core.version import get_version

from ..core.pyradarr import Radarr
from ..core.pytmdb import TMDB, TMDBException

from rich.live import Live
from rich.table import Table


VERSION_BANNER = """
Excludarr %s
%s
""" % (
    get_version(),
    get_version_banner(),
)


class Base(Controller):
    class Meta:
        label = "base"

        # text displayed at the top of --help output
        description = "Exclude streaming services such as netflix from Radarr"

        # text displayed at the bottom of --help output
        epilog = "Usage: excludarr delete --providers neflix --country nl"

        # controller level arguments. ex: 'excludarr --version'
        arguments = [
            ### add a version banner
            (["-v", "--version"], {"action": "version", "version": VERSION_BANNER}),
        ]

    def _default(self):
        """Default action if no sub-command is passed."""

        self.app.args.print_help()

    @ex(
        label="delete",
        help="Delete the media that is also available on streaming providers",
        arguments=[
            (
                ["-p", "--providers"],
                {
                    "help": "a single streaming provider, can be set multiple times",
                    "action": "append",
                    "default": [],
                    "dest": "providers",
                },
            ),
            (
                ["-c", "--country"],
                {
                    "help": "the 2 letter country code you are living in",
                    "action": "store",
                },
            ),
            (
                ["-t", "--type"],
                {
                    "help": "the type of endpoint to reach. Only Radarr is supported at the moment.",
                    "action": "store",
                    "default": "radarr",
                    "choices": ["radarr"],
                },
            ),
            (
                ["-r", "--remove-not-found"],
                {
                    "help": "delete the movie as well when it cannot be found on tmdb",
                    "action": "store_true",
                },
            ),
            (
                ["-d", "--delete-files"],
                {
                    "help": "delete currently downloaded files as well",
                    "action": "store_true",
                },
            ),
            (
                ["-e", "--exclusion"],
                {
                    "help": "add a exclusion in Radarr to prevent future importing the movie from a list",
                    "action": "store_true",
                },
            ),
            (
                ["-l", "--legacy"],
                {
                    "help": "if this flag is set, delete the movies one by one instead of a single API call",
                    "action": "store_true",
                },
            ),
            (
                ["-f", "--force"],
                {"help": "force deletion without user input", "action": "store_true"},
            ),
        ],
    )
    def delete_media(self):
        # Get command line arguments
        exclude_providers = self.app.pargs.providers
        country = self.app.pargs.country
        media_type = self.app.pargs.type
        force = self.app.pargs.force
        remove_if_not_found = self.app.pargs.remove_not_found
        delete_files = self.app.pargs.delete_files
        add_import_exclusion = self.app.pargs.exclusion
        legacy_delete = self.app.pargs.legacy

        # Get TMDB configuration
        tmdb_api_key = self.app.config.get("tmdb", "api_key")

        # Set defaults if there are none provided
        if len(exclude_providers) == 0:
            exclude_providers = self.app.config.get("general", "providers")
        if country == None:
            country = self.app.config.get("general", "country")

        # Ensure the 2 letter country code is uppercase
        country = country.upper()

        # Ensure the providers list is all lowercase
        exclude_providers = [x.lower() for x in exclude_providers]

        # Check wether to list sonarr or radarr
        if media_type == "sonarr":
            pass
        elif media_type == "radarr":
            # Get radarr variables
            radarr_url = self.app.config.get("radarr", "url")
            radarr_api_key = self.app.config.get("radarr", "api_key")
            radarr_verify_ssl = self.app.config.get("radarr", "verify_ssl")

            # Setup Radarr and TMDB
            radarr = Radarr(radarr_url, radarr_api_key, ssl_verify=radarr_verify_ssl)
            tmdb = TMDB(tmdb_api_key)

            # Setup a list of ids to delete
            delete_ids = []

            # Setup the rich table
            table = Table()
            table.add_column("ID")
            table.add_column("Title")
            table.add_column("Providers")

            with Live(table):
                # Get all movies from radarr and check if tmdbid is being streamed on configured providers
                for movie in radarr.movie.get_all_movies():
                    try:
                        # Get the providers in the specified country of the movie from TMDB
                        tmdb_providers = tmdb.movie.get_watch_providers(
                            movie["tmdbId"]
                        )["results"][country]

                        # Add all found providers to a list
                        local_providers = [
                            x["provider_name"].lower()
                            for x in tmdb_providers["flatrate"]
                        ]

                        # Check if the founded providers are in
                        providers = [
                            x for x in local_providers if x in exclude_providers
                        ]
                        if providers:
                            delete_ids.append(movie["id"])
                            table.add_row(
                                f"{movie['id']}",
                                f"{movie['title']}",
                                f"{', '.join(providers)}",
                            )

                    except TMDBException:
                        if remove_if_not_found:
                            delete_ids.append(movie["id"])
                            table.add_row(
                                f"{movie['id']}",
                                f"{movie['title']}",
                                f"TMDB ID UNKNOWN",
                            )
                    except KeyError:
                        # This will only raise if there is no streaming provider found
                        # using the selected country
                        pass

            # Set delete to false
            delete = False

            # Prompt when force is not set
            if not force:
                p = shell.Prompt(
                    "Are you sure you want to delete the movies listed in the table from radarr? (y/N)",
                    default="N",
                )
                res = p.prompt()

                if res.upper() == "Y":
                    delete = True
            else:
                delete = True

            # Delete the movies
            if delete_ids and delete and not legacy_delete:
                radarr.movie.delete_movies(
                    delete_ids,
                    delete_files=delete_files,
                    add_import_exclusion=add_import_exclusion,
                )
                self.app.print("Succesfully deleted the movies from Radarr")
            elif delete_ids and delete and legacy_delete:
                for id in delete_ids:
                    radarr.movie.delete_movie(
                        id,
                        delete_files=delete_files,
                        add_import_exclusion=add_import_exclusion,
                    )
                self.app.print("Succesfully deleted the movies from Radarr")
