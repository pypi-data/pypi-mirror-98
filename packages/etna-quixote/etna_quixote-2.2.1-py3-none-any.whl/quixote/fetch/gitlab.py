from datetime import datetime

from etna_api import EtnaSession

from quixote import get_context
from quixote.fetch.git import clone


def gitlab(*, ignore_end_date: bool = False):
    """
    Fetch the delivery from our own GitLab server

    The following entries must be provided in the context:
    - module_id:        the ID of the corresponding module, as integer
    - activity_id:      the ID of the corresponding activity, as integer
    - group_id:         the ID of the target group, as integer
    - stage_end:        the stage's end date in %Y-%m-%dT%H:%M:%S%z format
    - intra_user:       the username to use to connect to the intranet
    - intra_password:   the password to use to connect to the intranet
    - gitlab_token:     the OAuth token to use to authenticate to GitLab
    - stage_end:        the date at which the stage ends, as a string like "2019-05-15T18:02:00+01:00"
    """
    module_id = get_context()["module_id"]
    activity_id = get_context()["activity_id"]
    group_id = get_context()["group_id"]

    session = EtnaSession(
        username=get_context()["intra_user"],
        password=get_context()["intra_password"],
        request_retries=10,
        retry_on_statuses=(500, 502, 504)
    )

    grp = session.get_group_by_id(module_id, activity_id, group_id)
    stage_end = None
    if not ignore_end_date:
        stage_end = datetime.strptime(get_context()["stage_end"], '%Y-%m-%dT%H:%M:%S%z')
    url = "https://" + "oauth2:" + get_context()["gitlab_token"] + "@" + grp['rendu'][8:]
    clone(url, maximum_date=stage_end)
