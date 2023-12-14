import click


@click.command()
@click.option('--count', default=1, help='Number of greetings.')
@click.option('--name', prompt='Your name',
              help='The person to greet.')
def say_hello(count, name):
    """Simple program that greets NAME for a total of COUNT times."""
    for x in range(count):
        click.echo(f"Hello {name}!")


def print_time(timezone):
    # TODO print current time
    pass


@click.command()
@click.option('--height', prompt='Your height (in meters)', type=float, help='Number of height.')
@click.option('--weight', prompt='Your weight (in kg)', type=float, help='Number of weight.')
def calculate_bmi(height, weight):
    bmi = weight/(height**2)
    click.echo(f"您的bmi為 {bmi:.2f}!")


# Create Click command group
@click.group()
def cli():
    """A simple command-line tool."""
    pass


# Add commands to the group
cli.add_command(say_hello)
cli.add_command(calculate_bmi)

if __name__ == '__main__':
    cli()
