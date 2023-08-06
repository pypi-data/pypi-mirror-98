import os


ci_envs = [
    "CI",  # GitHub Actions, Travis CI, CircleCI, Cirrus CI, GitLab CI, AppVeyor, CodeShip, dsari
    "BUILD_NUMBER",  # Jenkins, TeamCity
    "RUN_ID",  # TaskCluster, dsari
]


def is_ci() -> bool:
    """Detects if we're in a CI environment or not.

    Based on: https://github.com/watson/ci-info/blob/074a5a9f2fae5f066abb6fb3c9e59992fee62c17/index.js#L52
    """
    return any([bool(os.environ.get(ci, False)) for ci in ci_envs])
