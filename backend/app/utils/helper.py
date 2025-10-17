import requests
from requests.exceptions import JSONDecodeError


def safe_json_response(response):
    """
    Safely parse JSON response from a requests.Response object.

    Args:
        response (requests.Response): The response object to parse.

    Returns:
        dict: Parsed JSON data if successful, otherwise an empty dict.
    """
    try:
        return response.json()
    except (JSONDecodeError, ValueError):
        print(f"Invalid JSON response: {response.text}")
        print(f"Status code: {response.status_code}")
        raise ValueError(f"API returned invalid JSON response: [{response.status_code}] -  {response.reason}")
