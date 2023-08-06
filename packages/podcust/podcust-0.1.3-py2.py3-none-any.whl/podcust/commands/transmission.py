import click
from subprocess import run as srun
from podcust.transmission.custodian import TransmissionCust
from podcust.transmission import service as pservice


@click.group()
@click.pass_context
def transmission(ctx):
    """Podcust tools for transmission container image."""
    # We can only use ctx.obj to create and share between commands.
    ctx.obj = TransmissionCust()
    click.echo("Initializing Podman Custodian Transmission class.")


@click.command()
@click.pass_obj
def deploy(obj):
    """Deploy transmission container within a pod."""
    click.echo("Deploying transmission container within a pod")
    obj.deploy()
    click.echo("Transmission container deployed!")


@click.command()
@click.pass_obj
def stop(obj):
    """Stop transmission pod."""
    click.echo("Stopping transmission pod.")
    obj.stop()
    click.echo("Transmission pod stopped!")


@click.command()
@click.pass_obj
def start(obj):
    """Start transmission pod."""
    click.echo("Starting transmission pod.")
    obj.stop()
    click.echo("Transmission pod started!")


@click.command()
@click.pass_obj
def rm(obj):
    """Delete transmission pod."""
    click.echo("Delete transmission pod.")
    obj.stop()
    click.echo("Transmission pod deleted!")


@click.command()
@click.pass_obj
def update(obj):
    """Update transmission pod."""
    click.echo("Updating transmission pod.")
    obj.update_running_image()
    click.echo("Transmission pod updated!")


@click.command()
@click.pass_obj
def clear(obj):
    """Clear data of transmission image."""
    obj.clear_location()
    click.echo("All files used by the transmission image have been deleted.")


transmission.add_command(deploy)
transmission.add_command(stop)
transmission.add_command(start)
transmission.add_command(rm)
transmission.add_command(update)
transmission.add_command(clear)


@click.group()
def service(args=None):
    """Podcust service tools for transmission container image."""


@click.command()
def setup():
    """
    Install podcust transmission-pod service for current user.
    """

    click.echo("Installing podcust transmission-pod service.")
    unit_path = pservice.create_user_unit_path(create_folder=True)
    pservice.create_service_unit(unit_path=unit_path)
    click.echo("podcust transmission-pod service installed.")


@click.command()
def activate():
    """
    Activate podcust transmission-pod service after installing it for current user.
    """
    click.echo("Activating podcust transmission-pod service.")
    pservice.activate_service()
    click.echo("podcust transmission-pod service activated.")


@click.command()
def deactivate():
    """
    Deactivate podcust transmission-pod service for current user.
    """
    click.echo("Dectivating podcust transmission-pod service.")
    pservice.deactivate_service()
    click.echo("podcust transmission-pod service deactivated.")


@click.command()
def logs(
    since: str = "today",
    help=(
        "Date from which we want to see logs. String in format 'YYYY-MM-DD hh:mm:ss'. "
        "Defaults to today."
    ),
):
    """
    See podman custodian's transmission-pod user service logs from specified time.
    """
    click.echo("Showing Podman Custodian transmission-pod service logs.")
    srun(
        ["journalctl", "--user-unit=transmission-pod.service", f"--since={since}"],
        check=True,
    )


@click.command()
@click.pass_obj
def delete(obj):
    """Delete transmission service unit file."""
    obj.delete_service_unit()
    click.echo("Transmission service unit file deleted.")


transmission.add_command(service)
service.add_command(setup)
service.add_command(activate)
service.add_command(deactivate)
service.add_command(logs)
service.add_command(delete)
