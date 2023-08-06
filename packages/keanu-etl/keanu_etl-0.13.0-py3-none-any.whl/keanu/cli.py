import logging
import sys
from os import environ

import click
from click_aliases import ClickAliasedGroup

from . import config, helpers, util
from .db_destination import DBDestination
from .sql_loader import SqlLoader
from .test import TestLoaders


@click.group(cls=ClickAliasedGroup)
def cli():
    pass


def positive_int(ctx, param, value):
    v = int(value)
    if v >= 1:
        return v
    else:
        raise click.BadParameter("-t thread_number must be a positive integer")


@cli.command(aliases=["l"])
@click.option(
    "-i", "--incremental", is_flag=True, default=False, help="incremental load"
)
@click.option("-n", "--dry-run", is_flag=True, default=False, help="dry run")
@click.option(
    "-o",
    "--order",
    default="0:",
    help="specify order of files to run by (eg. 10 or 10,12 or 10:15,60 etc)",
)
@click.option("-d", "--display", is_flag=True, default=False, help="display SQL")
@click.option("-W", "--warn", is_flag=True, default=False, help="display SQL warnings")
@click.option(
    "-t",
    "--threads",
    default=1,
    callback=positive_int,
    help="Number of threads for parallel python scripts",
)
@click.option("-v", "--verbose", is_flag=True, default=False, help="More logging")
@click.argument("config_or_dir", default="keanu.yaml", type=click.Path(exists=True))
def load(incremental, order, dry_run, display, warn, threads, config_or_dir, verbose):
    set_verbose(verbose)
    mode = {
        "incremental": incremental,
        "display": display,
        "warn": warn,
        "order": order,
        "dry_run": dry_run,
        "rewind": False,
        "threads": threads,
    }

    configuration = config.configuration_from_argument(config_or_dir)
    batch = config.build_batch(mode, configuration)

    for event, data in batch.execute():
        scr = data["script"]
        if event.startswith("sql.script.start"):
            click.echo(
                "🚚 [{:3d}] {} ({} lines, {} statements)".format(
                    scr.order, scr.filename, len(scr.lines), len(scr.statements)
                )
            )

        elif event.startswith("sql.statement.start"):
            click.echo(
                "📦 {0}...".format(
                    util.highlight_sql(scr.statement_abbrev(data["sql"]))
                ),
                nl=display,
            )

        elif event.startswith("sql.statement.end"):
            code = util.highlight_sql(scr.statement_abbrev(data["sql"]))

            # If display (-d) is set, the code was already shown on start,
            # and we are not overwriting the same line
            if display:
                code = ""

            
            util.clear_line()
            click.echo(
                "✅️ {} rows in {:0.2f}s {:}".format(
                    data["result"].rowcount, data["time"], code
                )
            )

        elif event.startswith("py.script.start"):
            util.clear_line()
            click.echo(
                "🐍 [{:3d}] {}".format(scr.order, scr.filename), nl=(display or dry_run)
            )

        elif event.startswith("py.script.end"):
            util.clear_line()
            click.echo(
                "✅ [{:3d}] {} in {:0.2f}s".format(
                    scr.order, scr.filename, data["time"]
                )
            )


@cli.command(aliases=["d"])
@click.option("-n", "--dry-run", is_flag=True, default=False, help="dry run")
@click.option(
    "-o",
    "--order",
    default="0:",
    help="specify order of files to run by (eg. 10 or 10,12 or 10:15,60 etc)",
)
@click.option("-d", "--display", is_flag=True, default=False, help="display SQL")
@click.option("-W", "--warn", is_flag=True, default=False, help="display SQL warnings")
@click.argument("config_or_dir", default="keanu.yaml", type=click.Path(exists=True))
def delete(order, display, dry_run, warn, config_or_dir):
    mode = {
        "order": order,
        "display": display,
        "dry_run": dry_run,
        "warn": warn,
        "rewind": True,
    }
    configuration = config.configuration_from_argument(config_or_dir)
    batch = config.build_batch(mode, configuration)

    for event, data in batch.execute():
        scr = data["script"]
        if event.startswith("sql.script.start"):
            click.echo(
                "🚒️ [{:3d}] {} ({})".format(
                    scr.order,
                    scr.filename,
                    ", ".join(
                        map(
                            lambda s: s.rstrip(), map(util.highlight_sql, scr.deleteSql)
                        )
                    ),
                ),
                color=True,
            )
        elif event.startswith("sql.statement.start"):
            click.echo(
                "🔥 {0}".format(util.highlight_sql(scr.statement_abbrev(data["sql"])))
            )
        elif event.startswith("py.script.start"):
            click.echo("💨 [{:3d}] {}".format(scr.order, scr.filename))


@cli.command(aliases=["s"])
@click.option(
    "-D",
    "--drop",
    is_flag=True,
    default=False,
    help="DROP TABLEs before running the script",
)
@click.option("-L", "--loads", default=[], multiple=True, help="Load this SQL file")
@click.option("-H", "--helper", default=[], multiple=True, help="Load this helper SQL")
@click.argument("database_url")
def schema(drop, loads, helper, database_url):
    dest = DBDestination({"db": {"url": database_url or environ.get("DATABASE_URL")}})
    connection = dest.connection()

    if drop:
        for (table, _) in connection.execute(
            "show full tables where Table_Type = 'BASE TABLE'"
        ):
            connection.execute("SET FOREIGN_KEY_CHECKS = 0")
            click.echo("💥 Dropping table {}".format(table))
            connection.execute("DROP TABLE {}".format(table))

    loads = [helpers.schema_path(x) for x in helper] + list(loads)

    if loads:
        for load in loads:
            script = SqlLoader(load, {}, None, dest)
            click.echo("🚚 Loading {}...".format(script.filename))
            with connection.begin():
                for event, data in script.execute():
                    scr = data["script"]
                    if event.startswith("sql.statement.start"):
                        click.echo(
                            "📦 {0}...".format(
                                util.highlight_sql(scr.statement_abbrev(data["sql"]))
                            ),
                            nl=False,
                        )
                    elif event.startswith("sql.statement.end"):
                        util.clear_line()
                        click.echo(
                            "✅️ {} rows in {:0.2f}s {:}".format(
                                data["result"].rowcount,
                                data["time"],
                                util.highlight_sql(scr.statement_abbrev(data["sql"])),
                            )
                        )

    if not drop and not loads:
        click.echo("Specify -D to drop tables and/or")
        click.echo(
            "Specify -L schema_file.sql and/or -H helper_name to load anything to the database"
        )


@cli.command(aliases=["t"])
@click.option(
    "--no-fixtures",
    is_flag=True,
    help="Do not load configured fixtures before running the test suite",
)
@click.argument("test_config", default="keanu-test.yaml", type=click.Path(exists=True))
@click.argument("test_dir", default="tests", type=click.Path(exists=True))
@click.argument("spec", required=False)
def test(test_config, test_dir, spec, no_fixtures):
    """
    Run tests from TEST_DIR (default tests), using batch configuration from TEST_CONFIG (default keanu-test.yaml).
    You should configure the batch in test file in a way that is similar to your production setup. Each test will make a full load of loaders defined by script ORDER variable, similar to load -o option format.

    Use spec to limit test files, it defaults to test*.py when omitted.
    """
    configuration = config.configuration_from_argument(test_config)
    suite = TestLoaders(configuration, no_fixtures)
    result = suite.run(test_dir, spec)

    if result.wasSuccessful():
        click.echo("All {} tests pass".format(result.testsRun))
        return 0

    for (t, tb) in result.errors:
        click.echo("💔  Error in {}\n{}".format(t, tb))

    for (t, tb) in result.failures:
        click.echo("😞  Failure in {}\n{}".format(t, tb))

    click.echo("{} tests failed".format(len(result.failures)))

    sys.exit(1)


def set_verbose(verbose):
    if verbose:
        logging.basicConfig()
        logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
