from mcp.server.fastmcp import FastMCP
import requests
import os
from dotenv import load_dotenv

load_dotenv()

required_api_keys = ["CONGRESS_GOV_API_KEY"]

missing_keys = []
for key in required_api_keys:
    if key not in os.environ:
        missing_keys.append(key)

if missing_keys:
    raise EnvironmentError(f"Required environment variables are missing: {', '.join(missing_keys)}")

mcp = FastMCP("usgov_mcp")
congress_gov_api_key = os.environ.get("CONGRESS_GOV_API_KEY")


@mcp.tool()
def get_bills(
    congress: int | None = None,
    bill_type: str | None = None,
    bill_number: int | None = None,
    offset: int = 0,
    limit: int = 20,
    from_datetime: str | None = None,
    to_datetime: str | None = None,
    sort: str = "updateDate+desc"
) -> dict:
    """
    Retrieve bills from the Congress.gov API.

    Args:
        congress: Congress number (e.g., 118 for 118th Congress)
        bill_type: Type of bill (hr, s, hjres, sjres, hconres, sconres, hres, sres)
        bill_number: Specific bill number (requires congress and bill_type)
        offset: Starting record (default 0)
        limit: Maximum records to return (max 250, default 20)
        from_datetime: Start timestamp (YYYY-MM-DDTHH:MM:SSZ format)
        to_datetime: End timestamp (YYYY-MM-DDTHH:MM:SSZ format)
        sort: Sort order ('updateDate+asc' or 'updateDate+desc')

    Returns:
        dict: Bill data from Congress.gov API
    """
    base_url = "https://api.congress.gov/v3/bill"

    url = base_url
    if congress:
        url += f"/{congress}"
        if bill_type:
            url += f"/{bill_type}"
            if bill_number:
                url += f"/{bill_number}"

    params = {
        "api_key": congress_gov_api_key,
        "format": "json",
        "offset": offset,
        "limit": min(limit, 100)  # Enforce API max limit
    }

    if from_datetime:
        params["fromDateTime"] = from_datetime
    if to_datetime:
        params["toDateTime"] = to_datetime
    if not bill_number:
        params["sort"] = sort

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        return {
            "error": f"Failed to retrieve bills: {str(e)}",
            "status_code": getattr(e.response, "status_code", None)
        }
