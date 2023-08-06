import click
from podcust.demo.custodian import DemoCust


@click.group()
@click.pass_context
def demo(ctx):
    """Podcust tools for demo container image."""
    # We can only use ctx.obj to create and share between commands.
    ctx.obj = DemoCust()
    click.echo("Initializing Podman Custodian Demo class.")


@click.command()
@click.pass_obj
def rmi(obj):
    """Remove a demo image."""
    click.echo("Removing Demo image.")
    obj.remove_stored_image()
    click.echo("Image removed!")


@click.command()
@click.pass_obj
def rmec(obj):
    """Remove an exited demo container."""
    click.echo("Removing Demo containers.")
    obj.removed_exited_containers()
    click.echo("Containers removed!")


@click.command()
@click.pass_obj
def build(obj):
    """Build a demo image."""
    click.echo("building Demo image.")
    obj.build_demo_image()
    click.echo("Image built!")


@click.command()
@click.pass_obj
def start(obj):
    """Start a demo container."""
    click.echo("Starting Demo container.")
    obj.run_container()
    click.echo("Demo container started!")


@click.command()
@click.pass_obj
def stop(obj):
    """Stop a demo container."""
    click.echo("Stopping Demo container.")
    obj.stop_container()
    click.echo("Demo container stopped!")


@click.command()
@click.pass_obj
def activate(obj):
    """Activate a demo container's service."""
    click.echo("Activating Demo container.")
    obj.activate_container()
    click.echo("Demo container service activated!")


@click.command()
@click.pass_obj
def deactivate(obj):
    """Deactivate a demo container's service."""
    click.echo("Deactivating Demo container.")
    obj.deactivate_container()
    click.echo("Demo container service deactivated!")


@click.command()
@click.pass_obj
def health(obj):
    """Health check of a demo container's service."""
    click.echo("Checking Demo container.")
    obj.health_check()


demo.add_command(rmi)
demo.add_command(rmec)
demo.add_command(build)
demo.add_command(start)
demo.add_command(stop)
demo.add_command(activate)
demo.add_command(deactivate)
demo.add_command(health)
