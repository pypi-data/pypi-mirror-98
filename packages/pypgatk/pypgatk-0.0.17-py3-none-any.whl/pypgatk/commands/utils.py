import click

CONTEXT_SETTINGS = {
    'help_option_names': ['-h', '--help'],
}


def echo_success(text, nl=True):
    click.secho(text, fg='cyan', bold=True, nl=nl)


def echo_failure(text, nl=True):
    click.secho(text, fg='red', bold=True, nl=nl)


def echo_warning(text, nl=True):
    click.secho(text, fg='yellow', bold=True, nl=nl)


def echo_waiting(text, nl=True):
    click.secho(text, fg='magenta', bold=True, nl=nl)


def echo_info(text, nl=True):
    click.secho(text, bold=True, nl=nl)


def print_help():
    """
    Print the help of the tool
    :return:
    """
    ctx = click.get_current_context()
    click.echo(ctx.get_help())
    ctx.exit()
