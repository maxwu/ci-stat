#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'maxwu'

import json

from me.maxwu.cistat import config
from me.maxwu.cistat.reqs.circleci_request import CircleCiReq
from me.maxwu.cistat.stats.xunit_report import Xunitrpt

"""Main script file to provide configuration loading, cli_app and version.
"""

VERSION = "1.0"


def cli_app():
    cases = Xunitrpt()

    artifacts =CircleCiReq.get_recent_artifacts(
            token=config.get_circleci_token(),
            vcs=config.get_circleci_vcs(),
            project=config.get_circleci_project(),
            username=config.get_circleci_username(),
            limit=10
    )
    for artifact in artifacts:
        print("fetching {}".format(artifact))
        cases.accumulate_xunit(CircleCiReq.get_artifact_report(artifact))

    print("Top 10 failure cases: {}".format(json.dumps(cases.get_cases_in_rate()[:10], indent=2)))


if __name__ == '__main__':
    cli_app()