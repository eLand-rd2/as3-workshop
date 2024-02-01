import click

import settings
from schedule_scripts import run_spider_task, run_greet_task
@click.command()

def greet():
    run_greet_task()

# run periodic task
@click.command()
def run_spider():
    run_spider_task()
    # """Run periodic task."""
    # TARGETS = settings.spider_target
    # for target in TARGETS:
    #     spider_cls = target['spider_class']
    #     target_url_list = target['urls']
    #
    #     spider = spider_cls()
    #
    #     for target_url in target_url_list:
    #         spider.run(target_url)


# run generate report task
@click.command()
@click.option('--begin_date', default=None, help='Begin date of report.')
@click.option('--end_date', default=None, help='End date of report.')
@click.option('--output', default=None, help='Output file path.')
def generate_report(begin_date, end_date, output):
    """Generate report."""
    # step 1: get data from database
    # step 2: generate report
    # step 3: save report to file
    raise NotImplementedError


# Create Click command group
@click.group()
def cli():
    """A simple command-line tool."""
    pass


# Add commands to the group
cli.add_command(run_spider)
cli.add_command(generate_report)
cli.add_command(greet)

if __name__ == '__main__':
    cli()
