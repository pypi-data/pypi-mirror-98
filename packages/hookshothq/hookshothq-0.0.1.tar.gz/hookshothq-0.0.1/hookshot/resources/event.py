import json
import requests

import hookshot


class Event(object):

  @classmethod
  def create(
      cls,
      api_key=None,
      idempotency_key=None,
      **params
  ):
    """
    Create a new Event against the API
    """

    api_base = hookshot.api_base
    _api_key = api_key or hookshot.api_key

    ## Todo (nrmitchi): Figure out how to manage the passing of "payload" (vs realm/key)
    key = params.get("event")
    realm = params.get("realm")

    if not key:
        # TODO: scope this exception down
        raise Exception("event is required")
    if not realm:
        # TODO: scope this exception down
        raise Exception("realm is required")

    params["key"] = params.get("event")

    print(params)

    res = requests.post(
        f"{api_base}/events",
        headers={
            "Authorization": f"token {_api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        data=json.dumps(params),
    )

    if res.status_code == 201:
      return res.json()

    res.raise_for_status()

  @classmethod
  def list(
      cls,
      api_key=None,
      **params
  ):
    """
    List Events from the API
    """
    pass
