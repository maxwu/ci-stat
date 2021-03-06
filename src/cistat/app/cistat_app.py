#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Entry point of console_cli app for CIstat
Cmd 'cistat-cli' is registered with PyPi dist and installed by pip.

..moduleauthor:: Max Wu < http: // maxwu.me >
"""
import pprint
from cistat.model import Xunitrpt
from cistat.reqs import CircleCiReq
from docopt import docopt
from cistat.version import get_version

DOC_OPT = """
Usage: 
    cistat --sample
    cistat (-h | --help)
    cistat (-v | --version)

Options:
    -h --help       Show this help message
    -v --version    Print cistat version
    --sample        Show sample statistic charts
"""


def cli_app():
    arguments = docopt(DOC_OPT, version=get_version())
    if arguments.get('--sample'):
        return cli_app_sample()


def cli_app_sample():
    # Another way with local ~/.cistat/config.yaml or environmental variables
    # vcs, project, username = config.get_circleci_vcs(), config.get_circleci_project(), config.get_circleci_username()

    vcs, project, username = 'github', 'cistat', 'maxwu'
    urls = CircleCiReq.get_recent_artifacts(vcs=vcs, project=project, username=username)

    report = Xunitrpt()

    for artifact in urls:
        print("fetching {}".format(artifact))
        report += Xunitrpt(xunit=CircleCiReq.get_artifact_report(url=artifact))

    print("Top 10 failure cases:")
    pprint.pprint(report.get_cases_in_rate()[:10])

    print("Plot Bar Chart on Pass Rate per Case")
    report.plot_barchart_rate(project, "Pass Rate per Case")

    print("Plot Bar Chart on Pass Rate per Class")
    report.get_class_rpt().plot_barchart_rate(project, "Pass Rate per Class")

    print("Plot Pie Chart on Case Num per Class")
    report.get_class_rpt().plot_piechart_casenum(project, "Case Num per Class")

    print("Plot Bubble Chart on Test ROI per Class")
    report.get_class_rpt().plot_scatter_roi(project, "Test ROI per Class")

if __name__ == '__main__':
    cli_app()
