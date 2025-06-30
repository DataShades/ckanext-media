import click


@click.group(short_help="media CLI.")
def media():
    """media CLI."""
    pass


@media.command()
@click.argument("name", default="media")
def command(name):
    """Docs."""
    click.echo("Hello, {name}!".format(name=name))


def get_commands():
    return [media]
