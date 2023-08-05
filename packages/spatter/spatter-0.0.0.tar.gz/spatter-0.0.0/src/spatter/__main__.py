"""Command-line interface."""
import click


@click.command()
@click.version_option()
def main() -> None:
    """Spatter."""


if __name__ == "__main__":
    main(prog_name="spatter")  # pragma: no cover
