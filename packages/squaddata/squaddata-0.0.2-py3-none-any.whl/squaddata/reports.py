import jinja2
import requests.compat
import squaddata.dataframe
from squad_client.core.api import SquadApi

te = jinja2.Environment(
    extensions=["jinja2.ext.loopcontrols"],
    loader=jinja2.PackageLoader(__name__),
    trim_blocks=True,
    lstrip_blocks=True,
    undefined=jinja2.StrictUndefined,
)


def test_results(results):
    summary = squaddata.dataframe.summary(results)
    passing = failing = skiping = xfailing = 0
    for key in summary:
        if key[1] != "build":
            passing = passing + summary[key].get("pass")
            failing = failing + summary[key].get("fail")
            skiping = skiping + summary[key].get("skip")
            xfailing = xfailing + summary[key].get("xfail")
    total = passing + failing + skiping + xfailing
    test_result = {
        "total": total,
        "pass": passing,
        "fail": failing,
        "skip": skiping,
        "xfail": xfailing,
    }
    return test_result


def create_report(template_stem, group, project, build, base_build, changes, results):
    args = {
        "build": build,
        "build_url": squad_build_url(group, project, build),
        "base_build": base_build,
        "regressions": squaddata.dataframe.regressions(changes),
        "fixes": squaddata.dataframe.fixes(changes),
        "test_result": test_results(results),
        "summary": squaddata.dataframe.summary(results),
        "environments": squaddata.dataframe.environments(results),
        "suites": squaddata.dataframe.suites(results),
        "fails": squaddata.dataframe.fails(results),
        "skips": squaddata.dataframe.skips(results),
        "total_tests": len(results),
    }
    return te.get_template(template_stem + ".txt.jinja").render(**args)


def squad_build_url(group, project, build):
    return requests.compat.urljoin(
        SquadApi.url, "/".join([group.slug, project.slug, "build", build.version])
    )
