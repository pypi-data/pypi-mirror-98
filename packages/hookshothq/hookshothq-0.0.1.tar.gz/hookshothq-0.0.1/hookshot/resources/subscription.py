import json
import requests

import hookshot


class Subscription(object):

  @classmethod
  def create(
      cls,
      api_key=None,
      idempotency_key=None,
      **params
  ):
    """
    Create a new Subscription against the API
    """

    api_base = hookshot.api_base
    _api_key = api_key or hookshot.api_key

    res = requests.post(
        f"{api_base}/subscriptions",
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
    List Subscriptions from the API
    """
    api_base = hookshot.api_base
    _api_key = api_key or hookshot.api_key

    print(f"Listing subscriptions on {api_base}")
    res = requests.get(
        f"{api_base}/subscriptions",
        headers={
            "Authorization": f"token {_api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
    )

    if res.status_code == requests.codes.ok:
      return res.json()
    
    res.raise_for_status()
