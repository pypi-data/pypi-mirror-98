import itertools
import json
import os
import sys

import click
import six
from click_aliases import ClickAliasedGroup

from . import exceptions, localdev, messages
from .check_system import check_requirements, check_requirements_human
from .cloud import CloudClient, get_endpoint
from .localdev.utils import allow_remote_id_override
from .upload.addon import upload_addon
from .upload.boilerplate import upload_boilerplate
from .utils import (
    Map,
    get_cp_url,
    get_git_checked_branch,
    hr,
    open_project_cloud_site,
    table,
)
from .validators.addon import validate_addon
from .validators.boilerplate import validate_boilerplate


try:
    import ipdb as pdb
except ImportError:
    import pdb


@click.group()
@click.option(
    "-d",
    "--debug/--no-debug",
    default=False,
    help="Drop into the debugger if command execution raises an exception.",
)
@click.pass_context
def cli(ctx, debug):
    if debug:

        def exception_handler(type, value, traceback):
            click.secho(
                "\nAn exception occurred while executing the requested "
                "command:",
                fg="red",
            )
            hr(fg="red")
            sys.__excepthook__(type, value, traceback)
            click.secho("\nStarting interactive debugging session:", fg="red")
            hr(fg="red")
            pdb.post_mortem(traceback)

        sys.excepthook = exception_handler

    ctx.obj = Map()
    ctx.obj.client = CloudClient(get_endpoint(), debug)

    try:
        is_version_command = sys.argv[1] == "version"
    except IndexError:
        is_version_command = False

    # skip if 'divio version' is run
    if not is_version_command:
        # check for newer versions
        update_info = ctx.obj.client.config.check_for_updates()
        if update_info["update_available"]:
            click.secho(
                "New version {} is available. Type `divio version` to "
                "show information about upgrading.".format(
                    update_info["remote"]
                ),
                fg="yellow",
            )


def login_token_helper(ctx, value):
    if not value:
        url = ctx.obj.client.get_access_token_url()
        click.secho("Your browser has been opened to visit: {}".format(url))
        click.launch(url)
        value = click.prompt(
            "Please copy the access token and paste it here. (your input is not displayed)",
            hide_input=True,
        )
    return value


@cli.command()
@click.argument("token", required=False)
@click.option(
    "--check",
    is_flag=True,
    default=False,
    help="Check for current login status.",
)
@click.pass_context
def login(ctx, token, check):
    """Authorise your machine with the Divio Control Panel."""
    success = True
    if check:
        success, msg = ctx.obj.client.check_login_status()
    else:
        token = login_token_helper(ctx, token)
        msg = ctx.obj.client.login(token)

    click.echo(msg)
    sys.exit(0 if success else 1)


@cli.group(cls=ClickAliasedGroup)
def project():
    """Manage your projects."""


@project.command(name="list")
@click.option(
    "-g",
    "--grouped",
    is_flag=True,
    default=False,
    help="Group by organisation.",
)
@click.option("--json", "as_json", is_flag=True, default=False)
@click.pass_obj
def project_list(obj, grouped, as_json):
    """List all your projects."""
    api_response = obj.client.get_projects()

    if as_json:
        click.echo(json.dumps(api_response, indent=2, sort_keys=True))
        return

    header = ("ID", "Slug", "Name", "Organisation")

    # get all users + organisations
    groups = {
        "users": {
            account["id"]: {"name": "Personal", "projects": []}
            for account in api_response["accounts"]
            if account["type"] == "user"
        },
        "organisations": {
            account["id"]: {"name": account["name"], "projects": []}
            for account in api_response["accounts"]
            if account["type"] == "organisation"
        },
    }

    # sort websites into groups
    for website in api_response["websites"]:
        organisation_id = website["organisation_id"]
        if organisation_id:
            owner = groups["organisations"][website["organisation_id"]]
        else:
            owner = groups["users"][website["owner_id"]]
        owner["projects"].append(
            (six.text_type(website["id"]), website["domain"], website["name"])
        )

    accounts = itertools.chain(
        groups["users"].items(), groups["organisations"].items()
    )

    def sort_projects(items):
        return sorted(items, key=lambda x: x[0].lower())

    # print via pager
    if grouped:
        output_items = []
        for group, data in accounts:
            projects = data["projects"]
            if projects:
                output_items.append(
                    u"{title}\n{line}\n\n{table}\n\n".format(
                        title=data["name"],
                        line="=" * len(data["name"]),
                        table=table(sort_projects(projects), header[:3]),
                    )
                )
        output = os.linesep.join(output_items).rstrip(os.linesep)
    else:
        # add account name to all projects
        projects = [
            each + (data["name"],)
            for group, data in accounts
            for each in data["projects"]
        ]
        output = table(sort_projects(projects), header)

    click.echo_via_pager(output)


@project.command(name="deploy")
@click.argument("stage", default="test")
@allow_remote_id_override
@click.pass_obj
def project_deploy(obj, remote_id, stage):
    """Deploy project."""
    obj.client.deploy_project_or_get_progress(remote_id, stage)


@project.command(name="deploy-log")
@click.argument("stage", default="test")
@allow_remote_id_override
@click.pass_obj
def project_deploy_log(obj, remote_id, stage):
    """View last deployment log."""
    obj.client.show_deploy_log(remote_id, stage)


@project.command(name="logs")
@click.argument("stage", default="test")
@click.option(
    "--tail", "tail", default=False, is_flag=True, help="Tail the output."
)
@click.option(
    "--utc", "utc", default=False, is_flag=True, help="Show times in UTC/"
)
@allow_remote_id_override
@click.pass_obj
def project_logs(obj, remote_id, stage, tail, utc):
    """View logs."""
    obj.client.show_log(remote_id, stage, tail, utc)


@project.command(name="ssh")
@click.argument("stage", default="test")
@allow_remote_id_override
@click.pass_obj
def project_ssh(obj, remote_id, stage):
    """Establish SSH connection."""
    obj.client.ssh(remote_id, stage)


@project.command(name="configure")
@click.pass_obj
def configure(obj):
    """Associate a local project with a Divio cloud project."""
    localdev.configure(client=obj.client)


@project.command(name="dashboard")
@allow_remote_id_override
@click.pass_obj
def project_dashboard(obj, remote_id):
    """Open the project dashboard on the Divio Control Panel."""
    click.launch(get_cp_url(client=obj.client, project_id=remote_id))


@project.command(name="up", aliases=["start"])
def project_up():
    """Start the local project (equivalent to: docker-compose up)."""
    localdev.start_project()


@project.command(name="stop", aliases=["down"])
def project_stop():
    """Stop the local project."""
    localdev.stop_project()


@project.command(name="open")
@click.argument("stage", default="")
@allow_remote_id_override
@click.pass_obj
def project_open(obj, remote_id, stage):
    """Open local or cloud projects in a browser."""
    if stage:
        open_project_cloud_site(obj.client, project_id=remote_id, stage=stage)
    else:
        localdev.open_project()


@project.command(name="update")
@click.option(
    "--strict",
    "strict",
    default=False,
    is_flag=True,
    help="A strict update will fail on a warning.",
)
@click.pass_obj
def project_update(obj, strict):
    """Update the local project with new code changes, then build it.

    Runs:

    git pull
    docker-compose pull
    docker-compose build
    docker-compose run web start migrate"""

    localdev.update_local_project(
        get_git_checked_branch(), client=obj.client, strict=strict
    )


@project.command(name="env-vars")
@click.option(
    "-s",
    "--stage",
    default="test",
    type=six.text_type,
    help="Manage the cloud project's environment variables.",
)
@click.option(
    "--all/--custom",
    "show_all_vars",
    default=False,
    help="--all shows automatically applied environment variables as well as user-specified variables.",
)
@click.option("--json", "as_json", is_flag=True, default=False)
@click.option(
    "--get",
    "get_vars",
    default=None,
    type=six.text_type,
    multiple=True,
    help="Get a specific environment variable.",
)
@click.option(
    "--set",
    "set_vars",
    default=None,
    type=click.Tuple([six.text_type, six.text_type]),
    multiple=True,
    help=(
        "Set a specific custom environment variable\n\n"
        "example: divio project env-vars set DEBUG False"
    ),
)
@click.option(
    "--unset",
    "unset_vars",
    default=None,
    type=six.text_type,
    multiple=True,
    help="Remove an environment variable.",
)
@allow_remote_id_override
@click.pass_obj
def environment_variables(
    obj,
    remote_id,
    stage,
    show_all_vars,
    as_json,
    get_vars,
    set_vars,
    unset_vars,
):
    """
    Get and set environment vars.

    WARNING: This command is experimental and may change in a future release.
    """
    if set_vars or unset_vars:
        set_vars = dict(set_vars)
        data = obj.client.set_custom_environment_variables(
            website_id=remote_id,
            stage=stage,
            set_vars=set_vars,
            unset_vars=unset_vars,
        )
    else:
        data = obj.client.get_environment_variables(
            website_id=remote_id, stage=stage, custom_only=not show_all_vars
        )
        if get_vars:
            data = {
                key: value for key, value in data.items() if key in get_vars
            }
    if as_json:
        click.echo(json.dumps(data, indent=2, sort_keys=True))
    else:
        header = ("Key", "Value")
        data = sorted([(key, value) for key, value in data.items()])
        output = table(data, header)
        click.echo_via_pager(output)


@project.command(name="status")
def project_status():
    """Show local project status."""
    localdev.show_project_status()


@project.command(name="setup")
@click.argument("slug")
@click.option(
    "-s",
    "--stage",
    default="test",
    help="Specify environment from which media and content data will be pulled.",
)
@click.option(
    "-p",
    "--path",
    default=".",
    help="Install project in path.",
    type=click.Path(writable=True, readable=True),
)
@click.option(
    "--overwrite",
    is_flag=True,
    default=False,
    help="Overwrite the project directory if it already exists.",
)
@click.option(
    "--skip-doctor",
    is_flag=True,
    default=False,
    help="Skip system test before setting up the project.",
)
@click.pass_obj
def project_setup(obj, slug, stage, path, overwrite, skip_doctor):
    """Set up a development environment for a Divio project."""
    if not skip_doctor and not check_requirements_human(
        config=obj.client.config, silent=True
    ):
        click.secho(
            "There was a problem while checking your system. Please run "
            "'divio doctor'.",
            fg="red",
        )
        sys.exit(1)

    localdev.create_workspace(obj.client, slug, stage, path, overwrite)


@project.group(name="pull")
def project_pull():
    """Pull db or files from the Divio cloud environment."""


@project_pull.command(name="db")
@click.argument("stage", default="test")
@click.argument("prefix", default=localdev.DEFAULT_SERVICE_PREFIX)
@allow_remote_id_override
@click.pass_obj
def pull_db(obj, remote_id, stage, prefix):
    """
    Pull database the Divio cloud environment.
    """
    from .localdev import utils

    project_home = utils.get_project_home()
    db_type = utils.get_db_type(prefix, path=project_home)
    localdev.ImportRemoteDatabase(
        client=obj.client,
        stage=stage,
        prefix=prefix,
        remote_id=remote_id,
        db_type=db_type,
    )()


@project_pull.command(name="media")
@click.argument("stage", default="test")
@allow_remote_id_override
@click.pass_obj
def pull_media(obj, remote_id, stage):
    """
    Pull media files from the Divio cloud environment.
    """
    localdev.pull_media(obj.client, stage=stage, remote_id=remote_id)


@project.group(name="push")
def project_push():
    """Push db or media files to the Divio cloud environment."""


@project_push.command(name="db")
@click.argument("stage", default="test")
@click.option(
    "-d",
    "--dumpfile",
    default=None,
    type=click.Path(exists=True),
    help="Specify a dumped database file to upload.",
)
@click.option(
    "--noinput",
    is_flag=True,
    default=False,
    help="Don't ask for confirmation.",
)
@click.argument("prefix", default=localdev.DEFAULT_SERVICE_PREFIX)
@allow_remote_id_override
@click.pass_obj
def push_db(obj, remote_id, prefix, stage, dumpfile, noinput):
    """
    Push database to the Divio cloud environment..
    """
    from .localdev import utils

    project_home = utils.get_project_home()
    db_type = utils.get_db_type(prefix, path=project_home)
    if not dumpfile:
        if not noinput:
            click.secho(messages.PUSH_DB_WARNING.format(stage=stage), fg="red")
            if not click.confirm("\nAre you sure you want to continue?"):
                return
        localdev.push_db(
            client=obj.client,
            stage=stage,
            remote_id=remote_id,
            prefix=prefix,
            db_type=db_type,
        )
    else:
        if not noinput:
            click.secho(messages.PUSH_DB_WARNING.format(stage=stage), fg="red")
            if not click.confirm("\nAre you sure you want to continue?"):
                return
        localdev.push_local_db(
            obj.client,
            stage=stage,
            dump_filename=dumpfile,
            website_id=remote_id,
            prefix=prefix,
        )


@project_push.command(name="media")
@click.argument("stage", default="test")
@click.option(
    "--noinput",
    is_flag=True,
    default=False,
    help="Don't ask for confirmation.",
)
@click.argument("prefix", default=localdev.DEFAULT_SERVICE_PREFIX)
@allow_remote_id_override
@click.pass_obj
def push_media(obj, remote_id, prefix, stage, noinput):
    """
    Push database to the Divio cloud environment..
    """

    if not noinput:
        click.secho(messages.PUSH_MEDIA_WARNING.format(stage=stage), fg="red")
        if not click.confirm("\nAre you sure you want to continue?"):
            return
    localdev.push_media(
        obj.client, stage=stage, remote_id=remote_id, prefix=prefix
    )


@project.group(name="import")
def project_import():
    """Import local database dump."""


@project_import.command(name="db")
@click.argument("prefix", default=localdev.DEFAULT_SERVICE_PREFIX)
@click.argument(
    "dump-path",
    default=localdev.DEFAULT_DUMP_FILENAME,
    type=click.Path(exists=True),
)
@click.pass_obj
def import_db(obj, dump_path, prefix):
    """
    Load a database dump into your local database.
    """
    from .localdev import utils

    project_home = utils.get_project_home()
    db_type = utils.get_db_type(prefix, path=project_home)
    localdev.ImportLocalDatabase(
        client=obj.client,
        custom_dump_path=dump_path,
        prefix=prefix,
        db_type=db_type,
    )()


@project.group(name="export")
def project_export():
    """Export local database dump."""


@project_export.command(name="db")
@click.argument("prefix", default=localdev.DEFAULT_SERVICE_PREFIX)
def export_db(prefix):
    """
    Export a dump of your local database
    """
    localdev.export_db(prefix=prefix)


@project.command(name="develop")
@click.argument("package")
@click.option(
    "--no-rebuild",
    is_flag=True,
    default=False,
    help="Do not rebuild docker container automatically.",
)
def project_develop(package, no_rebuild):
    """Add a package 'package' to your local project environment."""
    localdev.develop_package(package, no_rebuild)


@cli.group()
@click.option("-p", "--path", default=".", help="Addon directory")
@click.pass_obj
def addon(obj, path):
    """Validate and upload addons packages to the Divio cloud."""


@addon.command(name="validate")
@click.pass_context
def addon_validate(ctx):
    """Validate addon configuration."""
    try:
        validate_addon(ctx.parent.params["path"])
    except exceptions.DivioException as exc:
        raise click.ClickException(*exc.args)
    click.echo("Addon is valid!")


@addon.command(name="upload")
@click.pass_context
def addon_upload(ctx):
    """Upload addon to the Divio Control Panel."""
    try:
        ret = upload_addon(ctx.obj.client, ctx.parent.params["path"])
    except exceptions.DivioException as exc:
        raise click.ClickException(*exc.args)
    click.echo(ret)


@addon.command(name="register")
@click.argument("verbose_name")
@click.argument("package_name")
@click.option(
    "-o",
    "--organisation",
    help="Register an addon for an organisation.",
    type=int,
)
@click.pass_context
def addon_register(ctx, package_name, verbose_name, organisation):
    """Register your addon on the Divio Control Panel\n
    - Verbose Name:        Name of the Addon as it appears in the Marketplace
    - Package Name:        System wide unique Python package name
    """
    ret = ctx.obj.client.register_addon(
        package_name, verbose_name, organisation
    )
    click.echo(ret)


@cli.group()
@click.option("-p", "--path", default=".", help="Boilerplate directory")
@click.pass_obj
def boilerplate(obj, path):
    """Validate and upload boilerplate packages to the Divio cloud."""


@boilerplate.command(name="validate")
@click.pass_context
def boilerplate_validate(ctx):
    """Validate boilerplate configuration."""
    try:
        validate_boilerplate(ctx.parent.params["path"])
    except exceptions.DivioException as exc:
        raise click.ClickException(*exc.args)
    click.echo("Boilerplate is valid.")


@boilerplate.command(name="upload")
@click.option(
    "--noinput",
    is_flag=True,
    default=False,
    help="Don't ask for confirmation.",
)
@click.pass_context
def boilerplate_upload(ctx, noinput):
    """Upload boilerplate to the Divio Control Panel."""
    try:
        ret = upload_boilerplate(
            ctx.obj.client, ctx.parent.params["path"], noinput
        )
    except exceptions.DivioException as exc:
        raise click.ClickException(*exc.args)
    click.echo(ret)


@cli.command()
@click.option(
    "-s",
    "--skip-check",
    is_flag=True,
    default=False,
    help="Don't check PyPI for newer version.",
)
@click.option("-m", "--machine-readable", is_flag=True, default=False)
@click.pass_obj
def version(obj, skip_check, machine_readable):
    """Show version info."""
    if skip_check:
        from . import __version__

        update_info = {"current": __version__}
    else:
        update_info = obj.client.config.check_for_updates(force=True)

    update_info["location"] = os.path.dirname(os.path.realpath(sys.executable))

    if machine_readable:
        click.echo(json.dumps(update_info))
    else:
        click.echo(
            "divio-cli {} from {}\n".format(
                update_info["current"], update_info["location"]
            )
        )

        if not skip_check:
            if update_info["update_available"]:
                click.secho(
                    "New version {version} is available. Upgrade options:\n\n"
                    " - Using pip\n"
                    "   pip install --upgrade divio-cli\n\n"
                    " - Download the latest release from GitHub\n"
                    "   https://github.com/divio/divio-cli/releases".format(
                        version=update_info["remote"]
                    ),
                    fg="yellow",
                )
            elif update_info["pypi_error"]:
                click.secho(
                    "There was an error while trying to check for the latest "
                    "version on pypi.python.org:\n"
                    "{}".format(update_info["pypi_error"]),
                    fg="red",
                )
            else:
                click.echo("You have the latest version of divio-cli.")


@cli.command()
@click.option("-m", "--machine-readable", is_flag=True, default=False)
@click.option("-c", "--checks", default=None)
@click.pass_obj
def doctor(obj, machine_readable, checks):
    """Check that your system meets the development requirements.

    To disable checks selectively in case of false positives, see
    https://docs.divio.com/en/latest/reference/divio-cli/#using-skip-doctor-checks"""

    if checks:
        checks = checks.split(",")

    if machine_readable:
        errors = {
            check: error
            for check, check_name, error in check_requirements(
                obj.client.config, checks
            )
        }
        exitcode = 1 if any(errors.values()) else 0
        click.echo(json.dumps(errors), nl=False)
    else:
        click.echo("Verifying your system setup...")
        exitcode = (
            0 if check_requirements_human(obj.client.config, checks) else 1
        )

    sys.exit(exitcode)
