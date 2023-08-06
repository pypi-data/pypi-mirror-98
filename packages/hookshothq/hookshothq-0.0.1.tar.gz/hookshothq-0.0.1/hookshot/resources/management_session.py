import json
import requests

import hookshot


class ManagementSession(object):

  @classmethod
  def create(
      cls,
      api_key=None,
      idempotency_key=None,
      **params
  ):
    """
    Create a new ManagementSession against the API
    """

    api_base = hookshot.api_base
    _api_key = api_key or hookshot.api_key

    print(f"Making management_session on {api_base}")
    res = requests.post(
        f"{api_base}/management_sessions",
        headers={
            "Authorization": f"token {_api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        data=json.dumps(params),
    )
    # Todo (nrmitchi): Return full created object
    if res.status_code == 201:
      return res.json()
    
    res.raise_for_status()
