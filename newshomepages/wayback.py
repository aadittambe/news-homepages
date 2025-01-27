import time

import click
import savepagenow

from . import utils


@click.group()
def cli():
    """Shoot a screenshot."""
    pass


@cli.command()
@click.argument("handle")
def single(handle: str) -> str:
    """Archive a URL."""
    # Pull the source’s metadata
    data = utils.get_site(handle)
    # Upload it
    wayback_url = savepagenow.capture(data["url"])
    click.echo(f"Archived {data['url']} at {wayback_url}")
    return wayback_url


@cli.command()
@click.argument("slug")
def bundle(slug: str) -> list:
    """Archive a bundle of sources."""
    bundle = utils.get_bundle(slug)
    handle_list = [
        h["handle"] for h in utils.get_site_list() if h["bundle"] == bundle["slug"]
    ]
    url_list = []
    for handle in handle_list:
        # Pull the source’s metadata
        data = utils.get_site(handle)
        # Upload
        wayback_url = savepagenow.capture(data["url"])
        click.echo(f"Archived {data['url']} at {wayback_url}")
        # Pause
        time.sleep(2.5)
        url_list.append([data["handle"], wayback_url])
    return url_list


if __name__ == "__main__":
    cli()
