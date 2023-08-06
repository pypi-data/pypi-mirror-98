import argparse
import logging
import os
import pathlib
import squaddata.datasets
import squaddata.reports
from squad_client.core.api import SquadApi
from squad_client.core.api import ApiException as SquadApiException
from squad_client.core.models import Squad, Build
from squad_client.utils import getid

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def parse_args():
    parser = argparse.ArgumentParser(
        description="Create a report using data from SQUAD"
    )

    parser.add_argument(
        "--url",
        default=os.environ.get("SQUAD_URL", "https://qa-reports.linaro.org"),
        help="URL of the SQUAD service",
    )

    parser.add_argument(
        "--token",
        default=os.environ.get("SQUAD_TOKEN", None),
        help="Authentication token of the SQUAD service",
    )

    parser.add_argument(
        "--group",
        help="SQUAD group",
    )

    parser.add_argument(
        "--project",
        help="SQUAD project",
    )

    parser.add_argument(
        "--build",
        help="SQUAD build",
    )

    parser.add_argument(
        "--base-build",
        help="SQUAD build to compare to",
    )

    parser.add_argument(
        "--unfinished",
        action="store_true",
        default=False,
        help="Create a report even if a build is not finished",
    )

    environments_group = parser.add_mutually_exclusive_group()
    environments_group.add_argument(
        "--environments",
        help="List of SQUAD environments to include",
    )

    environments_group.add_argument(
        "--environment-prefixes",
        help="List of prefixes of SQUAD environments to include",
    )

    suites_group = parser.add_mutually_exclusive_group()
    suites_group.add_argument(
        "--suites",
        help="List of SQUAD suites to include",
    )

    suites_group.add_argument(
        "--suite-prefixes",
        help="List of prefixes of SQUAD suites to include",
    )

    parser.add_argument(
        "--template",
        help="Create the report with this template",
        default="report",
    )

    parser.add_argument(
        "--output",
        help="Write the report to this file",
        default="report.txt",
    )

    return parser.parse_args()


def report():
    args = parse_args()

    import requests_cache

    requests_cache.install_cache("squaddata")

    try:
        SquadApi.configure(url=args.url, token=args.token)
    except SquadApiException as sae:
        logger.error("Failed to configure the squad api: %s", sae)
        return -1

    squad = Squad()
    group = squad.group(args.group)
    project = group.project(args.project)
    build = project.build(args.build)

    if args.base_build:
        base_build = project.build(args.base_build)
    else:
        base_build_id = getid(build.status.baseline)
        base_build = Build().get(base_build_id)

    if not args.unfinished:
        if not build.finished:
            logger.error(
                f"Build {build.version} has not yet finished. Use --unfinished to force a report."
            )
            return -1

        if not base_build.finished:
            logger.error(
                f"Build {base_build.version} has not yet finished."
                "Use --unfinished to force a report."
            )
            return -1

    results = squaddata.datasets.results(
        group, project, build, base_build, args.unfinished
    )
    changes = squaddata.datasets.changes(
        group, project, build, base_build, args.unfinished
    )

    if args.environments:
        results = squaddata.dataframe.filter_isin(
            results, "environment", tuple(args.environments.split(","))
        )
        changes = squaddata.dataframe.filter_isin(
            changes, "environment", tuple(args.environments.split(","))
        )

    if args.suites:
        results = squaddata.dataframe.filter_isin(
            results, "suite", tuple(args.suites.split(","))
        )
        changes = squaddata.dataframe.filter_isin(
            changes, "suite", tuple(args.suites.split(","))
        )

    if args.environment_prefixes:
        results = squaddata.dataframe.filter_startswith(
            results, "environment", tuple(args.environment_prefixes.split(","))
        )
        changes = squaddata.dataframe.filter_startswith(
            changes, "environment", tuple(args.environment_prefixes.split(","))
        )

    if args.suite_prefixes:
        results = squaddata.dataframe.filter_startswith(
            results, "suite", tuple(args.suite_prefixes.split(","))
        )
        changes = squaddata.dataframe.filter_startswith(
            changes, "suite", tuple(args.suite_prefixes.split(","))
        )

    text = squaddata.reports.create_report(
        args.template, group, project, build, base_build, changes, results
    )

    pathlib.Path(args.output).write_text(text)

    return 0
