import os

import click
from flask import cli
from tw5_server.app import create_app

os.environ.setdefault('FLASK_APP', 'tw5_server.app')


@click.group()
@click.option('-c', '--config-file')
def main(config_file):
    if config_file:
        os.environ.setdefault('TW5_CONFIG_FILE', config_file)


def show_server_banner(env, debug, app_import_path, eager_loading):
    if env == 'production':
        click.secho(
            '   WARNING: This is a development server. '
            'Do not use it in a production deployment.',
            fg='red',
        )


@main.command(help='Serve wiki in dev mode')
@click.option('-h', '--host')
@click.option('-p', '--port')
def serve(host, port):
    app = create_app()
    cli.show_server_banner = show_server_banner
    app.run(host=host, port=port)


@main.command(help='Initial a new wiki')
@click.argument('wiki_name')
def init(wiki_name):
    from tw5_server.wiki.storage import Wiki
    Wiki.initialize(wiki_name)


if __name__ == '__main__':
    main()
