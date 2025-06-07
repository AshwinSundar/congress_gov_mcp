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


@mcp.tool()
def get_amendments(
    congress: int | None = None,
    amendment_type: str | None = None,
    amendment_number: int | None = None,
    offset: int = 0,
    limit: int = 20,
    from_datetime: str | None = None,
    to_datetime: str | None = None
) -> dict:
    """
    Retrieve amendments from the Congress.gov API.

    Args:
        congress: Congress number (e.g., 118 for 118th Congress)
        amendment_type: Type of amendment (hamdt, samdt, suamdt)
        amendment_number: Specific amendment number (requires congress and amendment_type)
        offset: Starting record (default 0)
        limit: Maximum records to return (max 250, default 20)
        from_datetime: Start timestamp (YYYY-MM-DDTHH:MM:SSZ format)
        to_datetime: End timestamp (YYYY-MM-DDTHH:MM:SSZ format)

    Returns:
        dict: Amendment data from Congress.gov API
    """
    base_url = "https://api.congress.gov/v3/amendment"

    url = base_url
    if congress:
        url += f"/{congress}"
        if amendment_type:
            url += f"/{amendment_type}"
            if amendment_number:
                url += f"/{amendment_number}"

    params = {
        "api_key": congress_gov_api_key,
        "format": "json",
        "offset": offset,
        "limit": min(limit, 250)  # API max limit for amendments
    }

    if from_datetime:
        params["fromDateTime"] = from_datetime
    if to_datetime:
        params["toDateTime"] = to_datetime

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        return {
            "error": f"Failed to retrieve amendments: {str(e)}",
            "status_code": getattr(e.response, "status_code", None)
        }


@mcp.tool()
def get_summaries(
    congress: int | None = None,
    bill_type: str | None = None,
    offset: int = 0,
    limit: int = 20,
    from_datetime: str | None = None,
    to_datetime: str | None = None,
    sort: str = "updateDate+desc"
) -> dict:
    """
    Retrieve bill summaries from the Congress.gov API.

    Args:
        congress: Congress number (e.g., 118 for 118th Congress)
        bill_type: Type of bill (hr, s, hjres, sjres, hconres, sconres, hres, sres)
        offset: Starting record (default 0)
        limit: Maximum records to return (max 250, default 20)
        from_datetime: Start timestamp (YYYY-MM-DDTHH:MM:SSZ format)
        to_datetime: End timestamp (YYYY-MM-DDTHH:MM:SSZ format)
        sort: Sort order ('updateDate+asc' or 'updateDate+desc')

    Returns:
        dict: Summary data from Congress.gov API
    """
    base_url = "https://api.congress.gov/v3/summaries"

    url = base_url
    if congress:
        url += f"/{congress}"
        if bill_type:
            url += f"/{bill_type}"

    params = {
        "api_key": congress_gov_api_key,
        "format": "json",
        "offset": offset,
        "limit": min(limit, 250),  # API max limit for summaries
        "sort": sort
    }

    if from_datetime:
        params["fromDateTime"] = from_datetime
    if to_datetime:
        params["toDateTime"] = to_datetime

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        return {
            "error": f"Failed to retrieve summaries: {str(e)}",
            "status_code": getattr(e.response, "status_code", None)
        }


@mcp.tool()
def get_congress(
    congress: int | None = None,
    offset: int = 0,
    limit: int = 20
) -> dict:
    """
    Retrieve congress information from the Congress.gov API.

    Args:
        congress: Specific congress number (e.g., 118 for 118th Congress) or None for all
        offset: Starting record (default 0)
        limit: Maximum records to return (max 250, default 20)

    Returns:
        dict: Congress data from Congress.gov API
    """
    base_url = "https://api.congress.gov/v3/congress"

    url = base_url
    if congress:
        url += f"/{congress}"

    params = {
        "api_key": congress_gov_api_key,
        "format": "json",
        "offset": offset,
        "limit": min(limit, 250)  # API max limit for congress
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        return {
            "error": f"Failed to retrieve congress information: {str(e)}",
            "status_code": getattr(e.response, "status_code", None)
        }


@mcp.tool()
def get_members(
    bioguide_id: str | None = None,
    offset: int = 0,
    limit: int = 20,
    from_datetime: str | None = None,
    to_datetime: str | None = None,
    current_member: bool | None = None
) -> dict:
    """
    Retrieve member information from the Congress.gov API.

    Args:
        bioguide_id: Specific member bioguide ID (e.g., "A000374")
        offset: Starting record (default 0)
        limit: Maximum records to return (max 250, default 20)
        from_datetime: Start timestamp (YYYY-MM-DDTHH:MM:SSZ format)
        to_datetime: End timestamp (YYYY-MM-DDTHH:MM:SSZ format)
        current_member: Filter by current member status (true/false)

    Returns:
        dict: Member data from Congress.gov API
    """
    base_url = "https://api.congress.gov/v3/member"

    url = base_url
    if bioguide_id:
        url += f"/{bioguide_id}"

    params = {
        "api_key": congress_gov_api_key,
        "format": "json",
        "offset": offset,
        "limit": min(limit, 250)  # API max limit for members
    }

    if from_datetime:
        params["fromDateTime"] = from_datetime
    if to_datetime:
        params["toDateTime"] = to_datetime
    if current_member is not None:
        params["currentMember"] = str(current_member).lower()

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        return {
            "error": f"Failed to retrieve member information: {str(e)}",
            "status_code": getattr(e.response, "status_code", None)
        }


@mcp.tool()
def get_house_votes(
    congress: int | None = None,
    session: int | None = None,
    roll_call_number: int | None = None,
    offset: int = 0,
    limit: int = 20,
    from_datetime: str | None = None,
    to_datetime: str | None = None
) -> dict:
    """
    Retrieve House vote information from the Congress.gov API.

    Args:
        congress: Congress number (e.g., 118 for 118th Congress)
        session: Session number (1 or 2)
        roll_call_number: Specific roll call vote number
        offset: Starting record (default 0)
        limit: Maximum records to return (max 250, default 20)
        from_datetime: Start timestamp (YYYY-MM-DDTHH:MM:SSZ format)
        to_datetime: End timestamp (YYYY-MM-DDTHH:MM:SSZ format)

    Returns:
        dict: House vote data from Congress.gov API
    """
    base_url = "https://api.congress.gov/v3/house-vote"

    url = base_url
    if congress:
        url += f"/{congress}"
        if session:
            url += f"/{session}"
            if roll_call_number:
                url += f"/{roll_call_number}"

    params = {
        "api_key": congress_gov_api_key,
        "format": "json",
        "offset": offset,
        "limit": min(limit, 250)  # API max limit for house votes
    }

    if from_datetime:
        params["fromDateTime"] = from_datetime
    if to_datetime:
        params["toDateTime"] = to_datetime

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        return {
            "error": f"Failed to retrieve house vote information: {str(e)}",
            "status_code": getattr(e.response, "status_code", None)
        }


@mcp.tool()
def get_committees(
    system_code: str | None = None,
    offset: int = 0,
    limit: int = 20,
    from_datetime: str | None = None,
    to_datetime: str | None = None
) -> dict:
    """
    Retrieve committee information from the Congress.gov API.

    Args:
        system_code: Specific committee system code (e.g., "hsag" for House Agriculture)
        offset: Starting record (default 0)
        limit: Maximum records to return (max 250, default 20)
        from_datetime: Start timestamp (YYYY-MM-DDTHH:MM:SSZ format)
        to_datetime: End timestamp (YYYY-MM-DDTHH:MM:SSZ format)

    Returns:
        dict: Committee data from Congress.gov API
    """
    base_url = "https://api.congress.gov/v3/committee"

    url = base_url
    if system_code:
        url += f"/{system_code}"

    params = {
        "api_key": congress_gov_api_key,
        "format": "json",
        "offset": offset,
        "limit": min(limit, 250)  # API max limit for committees
    }

    if from_datetime:
        params["fromDateTime"] = from_datetime
    if to_datetime:
        params["toDateTime"] = to_datetime

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        return {
            "error": f"Failed to retrieve committee information: {str(e)}",
            "status_code": getattr(e.response, "status_code", None)
        }


@mcp.tool()
def get_committee_reports(
    congress: int | None = None,
    report_type: str | None = None,
    report_number: int | None = None,
    offset: int = 0,
    limit: int = 20,
    from_datetime: str | None = None,
    to_datetime: str | None = None
) -> dict:
    """
    Retrieve committee report information from the Congress.gov API.

    Args:
        congress: Congress number (e.g., 118 for 118th Congress)
        report_type: Type of report (hrpt, srpt, etc.)
        report_number: Specific report number
        offset: Starting record (default 0)
        limit: Maximum records to return (max 250, default 20)
        from_datetime: Start timestamp (YYYY-MM-DDTHH:MM:SSZ format)
        to_datetime: End timestamp (YYYY-MM-DDTHH:MM:SSZ format)

    Returns:
        dict: Committee report data from Congress.gov API
    """
    base_url = "https://api.congress.gov/v3/committee-report"

    url = base_url
    if congress:
        url += f"/{congress}"
        if report_type:
            url += f"/{report_type}"
            if report_number:
                url += f"/{report_number}"

    params = {
        "api_key": congress_gov_api_key,
        "format": "json",
        "offset": offset,
        "limit": min(limit, 250)  # API max limit for committee reports
    }

    if from_datetime:
        params["fromDateTime"] = from_datetime
    if to_datetime:
        params["toDateTime"] = to_datetime

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        return {
            "error": f"Failed to retrieve committee report information: {str(e)}",
            "status_code": getattr(e.response, "status_code", None)
        }


@mcp.tool()
def get_committee_prints(
    congress: int | None = None,
    print_type: str | None = None,
    print_number: int | None = None,
    offset: int = 0,
    limit: int = 20,
    from_datetime: str | None = None,
    to_datetime: str | None = None
) -> dict:
    """
    Retrieve committee print information from the Congress.gov API.

    Args:
        congress: Congress number (e.g., 118 for 118th Congress)
        print_type: Type of print (hprt, sprt, etc.)
        print_number: Specific print number
        offset: Starting record (default 0)
        limit: Maximum records to return (max 250, default 20)
        from_datetime: Start timestamp (YYYY-MM-DDTHH:MM:SSZ format)
        to_datetime: End timestamp (YYYY-MM-DDTHH:MM:SSZ format)

    Returns:
        dict: Committee print data from Congress.gov API
    """
    base_url = "https://api.congress.gov/v3/committee-print"

    url = base_url
    if congress:
        url += f"/{congress}"
        if print_type:
            url += f"/{print_type}"
            if print_number:
                url += f"/{print_number}"

    params = {
        "api_key": congress_gov_api_key,
        "format": "json",
        "offset": offset,
        "limit": min(limit, 250)  # API max limit for committee prints
    }

    if from_datetime:
        params["fromDateTime"] = from_datetime
    if to_datetime:
        params["toDateTime"] = to_datetime

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        return {
            "error": f"Failed to retrieve committee print information: {str(e)}",
            "status_code": getattr(e.response, "status_code", None)
        }


@mcp.tool()
def get_committee_meetings(
    congress: int | None = None,
    chamber: str | None = None,
    offset: int = 0,
    limit: int = 20,
    from_datetime: str | None = None,
    to_datetime: str | None = None
) -> dict:
    """
    Retrieve committee meeting information from the Congress.gov API.

    Args:
        congress: Congress number (e.g., 118 for 118th Congress)
        chamber: Chamber (house, senate)
        offset: Starting record (default 0)
        limit: Maximum records to return (max 250, default 20)
        from_datetime: Start timestamp (YYYY-MM-DDTHH:MM:SSZ format)
        to_datetime: End timestamp (YYYY-MM-DDTHH:MM:SSZ format)

    Returns:
        dict: Committee meeting data from Congress.gov API
    """
    base_url = "https://api.congress.gov/v3/committee-meeting"

    url = base_url
    if congress:
        url += f"/{congress}"
        if chamber:
            url += f"/{chamber}"

    params = {
        "api_key": congress_gov_api_key,
        "format": "json",
        "offset": offset,
        "limit": min(limit, 250)  # API max limit for committee meetings
    }

    if from_datetime:
        params["fromDateTime"] = from_datetime
    if to_datetime:
        params["toDateTime"] = to_datetime

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        return {
            "error": f"Failed to retrieve committee meeting information: {str(e)}",
            "status_code": getattr(e.response, "status_code", None)
        }


@mcp.tool()
def get_hearings(
    congress: int | None = None,
    chamber: str | None = None,
    hearing_number: int | None = None,
    offset: int = 0,
    limit: int = 20,
    from_datetime: str | None = None,
    to_datetime: str | None = None
) -> dict:
    """
    Retrieve hearing information from the Congress.gov API.

    Args:
        congress: Congress number (e.g., 118 for 118th Congress)
        chamber: Chamber (house, senate)
        hearing_number: Specific hearing number
        offset: Starting record (default 0)
        limit: Maximum records to return (max 250, default 20)
        from_datetime: Start timestamp (YYYY-MM-DDTHH:MM:SSZ format)
        to_datetime: End timestamp (YYYY-MM-DDTHH:MM:SSZ format)

    Returns:
        dict: Hearing data from Congress.gov API
    """
    base_url = "https://api.congress.gov/v3/hearing"

    url = base_url
    if congress:
        url += f"/{congress}"
        if chamber:
            url += f"/{chamber}"
            if hearing_number:
                url += f"/{hearing_number}"

    params = {
        "api_key": congress_gov_api_key,
        "format": "json",
        "offset": offset,
        "limit": min(limit, 250)  # API max limit for hearings
    }

    if from_datetime:
        params["fromDateTime"] = from_datetime
    if to_datetime:
        params["toDateTime"] = to_datetime

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        return {
            "error": f"Failed to retrieve hearing information: {str(e)}",
            "status_code": getattr(e.response, "status_code", None)
        }


@mcp.tool()
def get_congressional_record(
    volume: int | None = None,
    page_prefix: str | None = None,
    page_number: int | None = None,
    offset: int = 0,
    limit: int = 20,
    from_datetime: str | None = None,
    to_datetime: str | None = None
) -> dict:
    """
    Retrieve congressional record information from the Congress.gov API.

    Args:
        volume: Volume number
        page_prefix: Page prefix (e.g., "h", "s", "e")
        page_number: Specific page number
        offset: Starting record (default 0)
        limit: Maximum records to return (max 250, default 20)
        from_datetime: Start timestamp (YYYY-MM-DDTHH:MM:SSZ format)
        to_datetime: End timestamp (YYYY-MM-DDTHH:MM:SSZ format)

    Returns:
        dict: Congressional record data from Congress.gov API
    """
    base_url = "https://api.congress.gov/v3/congressional-record"

    url = base_url
    if volume:
        url += f"/{volume}"
        if page_prefix:
            url += f"/{page_prefix}"
            if page_number:
                url += f"/{page_number}"

    params = {
        "api_key": congress_gov_api_key,
        "format": "json",
        "offset": offset,
        "limit": min(limit, 250)
    }

    if from_datetime:
        params["fromDateTime"] = from_datetime
    if to_datetime:
        params["toDateTime"] = to_datetime

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        return {
            "error": f"Failed to retrieve congressional record information: {str(e)}",
            "status_code": getattr(e.response, "status_code", None)
        }


@mcp.tool()
def get_daily_congressional_record(
    volume: int | None = None,
    issue: str | None = None,
    offset: int = 0,
    limit: int = 20,
    from_datetime: str | None = None,
    to_datetime: str | None = None
) -> dict:
    """
    Retrieve daily congressional record information from the Congress.gov API.

    Args:
        volume: Volume number
        issue: Issue identifier
        offset: Starting record (default 0)
        limit: Maximum records to return (max 250, default 20)
        from_datetime: Start timestamp (YYYY-MM-DDTHH:MM:SSZ format)
        to_datetime: End timestamp (YYYY-MM-DDTHH:MM:SSZ format)

    Returns:
        dict: Daily congressional record data from Congress.gov API
    """
    base_url = "https://api.congress.gov/v3/daily-congressional-record"

    url = base_url
    if volume:
        url += f"/{volume}"
        if issue:
            url += f"/{issue}"

    params = {
        "api_key": congress_gov_api_key,
        "format": "json",
        "offset": offset,
        "limit": min(limit, 250)
    }

    if from_datetime:
        params["fromDateTime"] = from_datetime
    if to_datetime:
        params["toDateTime"] = to_datetime

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        return {
            "error": f"Failed to retrieve daily congressional record information: {str(e)}",
            "status_code": getattr(e.response, "status_code", None)
        }


@mcp.tool()
def get_bound_congressional_record(
    year: int | None = None,
    month: int | None = None,
    day: int | None = None,
    offset: int = 0,
    limit: int = 20,
    from_datetime: str | None = None,
    to_datetime: str | None = None
) -> dict:
    """
    Retrieve bound congressional record information from the Congress.gov API.

    Args:
        year: Year
        month: Month (1-12)
        day: Day (1-31)
        offset: Starting record (default 0)
        limit: Maximum records to return (max 250, default 20)
        from_datetime: Start timestamp (YYYY-MM-DDTHH:MM:SSZ format)
        to_datetime: End timestamp (YYYY-MM-DDTHH:MM:SSZ format)

    Returns:
        dict: Bound congressional record data from Congress.gov API
    """
    base_url = "https://api.congress.gov/v3/bound-congressional-record"

    url = base_url
    if year:
        url += f"/{year}"
        if month:
            url += f"/{month:02d}"
            if day:
                url += f"/{day:02d}"

    params = {
        "api_key": congress_gov_api_key,
        "format": "json",
        "offset": offset,
        "limit": min(limit, 250)
    }

    if from_datetime:
        params["fromDateTime"] = from_datetime
    if to_datetime:
        params["toDateTime"] = to_datetime

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        return {
            "error": f"Failed to retrieve bound congressional record information: {str(e)}",
            "status_code": getattr(e.response, "status_code", None)
        }


@mcp.tool()
def get_house_communication(
    congress: int | None = None,
    communication_type: str | None = None,
    communication_number: int | None = None,
    offset: int = 0,
    limit: int = 20,
    from_datetime: str | None = None,
    to_datetime: str | None = None
) -> dict:
    """
    Retrieve House communication information from the Congress.gov API.

    Args:
        congress: Congress number (e.g., 118 for 118th Congress)
        communication_type: Type of communication (ec, ml, pm, pt)
        communication_number: Specific communication number
        offset: Starting record (default 0)
        limit: Maximum records to return (max 250, default 20)
        from_datetime: Start timestamp (YYYY-MM-DDTHH:MM:SSZ format)
        to_datetime: End timestamp (YYYY-MM-DDTHH:MM:SSZ format)

    Returns:
        dict: House communication data from Congress.gov API
    """
    base_url = "https://api.congress.gov/v3/house-communication"

    url = base_url
    if congress:
        url += f"/{congress}"
        if communication_type:
            url += f"/{communication_type}"
            if communication_number:
                url += f"/{communication_number}"

    params = {
        "api_key": congress_gov_api_key,
        "format": "json",
        "offset": offset,
        "limit": min(limit, 250)
    }

    if from_datetime:
        params["fromDateTime"] = from_datetime
    if to_datetime:
        params["toDateTime"] = to_datetime

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        return {
            "error": f"Failed to retrieve house communication information: {str(e)}",
            "status_code": getattr(e.response, "status_code", None)
        }


@mcp.tool()
def get_house_requirement(
    congress: int | None = None,
    requirement_number: int | None = None,
    offset: int = 0,
    limit: int = 20,
    from_datetime: str | None = None,
    to_datetime: str | None = None
) -> dict:
    """
    Retrieve House requirement information from the Congress.gov API.

    Args:
        congress: Congress number (e.g., 118 for 118th Congress)
        requirement_number: Specific requirement number
        offset: Starting record (default 0)
        limit: Maximum records to return (max 250, default 20)
        from_datetime: Start timestamp (YYYY-MM-DDTHH:MM:SSZ format)
        to_datetime: End timestamp (YYYY-MM-DDTHH:MM:SSZ format)

    Returns:
        dict: House requirement data from Congress.gov API
    """
    base_url = "https://api.congress.gov/v3/house-requirement"

    url = base_url
    if congress:
        url += f"/{congress}"
        if requirement_number:
            url += f"/{requirement_number}"

    params = {
        "api_key": congress_gov_api_key,
        "format": "json",
        "offset": offset,
        "limit": min(limit, 250)
    }

    if from_datetime:
        params["fromDateTime"] = from_datetime
    if to_datetime:
        params["toDateTime"] = to_datetime

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        return {
            "error": f"Failed to retrieve house requirement information: {str(e)}",
            "status_code": getattr(e.response, "status_code", None)
        }


@mcp.tool()
def get_senate_communication(
    congress: int | None = None,
    communication_type: str | None = None,
    communication_number: int | None = None,
    offset: int = 0,
    limit: int = 20,
    from_datetime: str | None = None,
    to_datetime: str | None = None
) -> dict:
    """
    Retrieve Senate communication information from the Congress.gov API.

    Args:
        congress: Congress number (e.g., 118 for 118th Congress)
        communication_type: Type of communication (ec, ml, pm, pt)
        communication_number: Specific communication number
        offset: Starting record (default 0)
        limit: Maximum records to return (max 250, default 20)
        from_datetime: Start timestamp (YYYY-MM-DDTHH:MM:SSZ format)
        to_datetime: End timestamp (YYYY-MM-DDTHH:MM:SSZ format)

    Returns:
        dict: Senate communication data from Congress.gov API
    """
    base_url = "https://api.congress.gov/v3/senate-communication"

    url = base_url
    if congress:
        url += f"/{congress}"
        if communication_type:
            url += f"/{communication_type}"
            if communication_number:
                url += f"/{communication_number}"

    params = {
        "api_key": congress_gov_api_key,
        "format": "json",
        "offset": offset,
        "limit": min(limit, 250)
    }

    if from_datetime:
        params["fromDateTime"] = from_datetime
    if to_datetime:
        params["toDateTime"] = to_datetime

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        return {
            "error": f"Failed to retrieve senate communication information: {str(e)}",
            "status_code": getattr(e.response, "status_code", None)
        }


@mcp.tool()
def get_nomination(
    congress: int | None = None,
    nomination_number: int | None = None,
    offset: int = 0,
    limit: int = 20,
    from_datetime: str | None = None,
    to_datetime: str | None = None
) -> dict:
    """
    Retrieve nomination information from the Congress.gov API.

    Args:
        congress: Congress number (e.g., 118 for 118th Congress)
        nomination_number: Specific nomination number
        offset: Starting record (default 0)
        limit: Maximum records to return (max 250, default 20)
        from_datetime: Start timestamp (YYYY-MM-DDTHH:MM:SSZ format)
        to_datetime: End timestamp (YYYY-MM-DDTHH:MM:SSZ format)

    Returns:
        dict: Nomination data from Congress.gov API
    """
    base_url = "https://api.congress.gov/v3/nomination"

    url = base_url
    if congress:
        url += f"/{congress}"
        if nomination_number:
            url += f"/{nomination_number}"

    params = {
        "api_key": congress_gov_api_key,
        "format": "json",
        "offset": offset,
        "limit": min(limit, 250)
    }

    if from_datetime:
        params["fromDateTime"] = from_datetime
    if to_datetime:
        params["toDateTime"] = to_datetime

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        return {
            "error": f"Failed to retrieve nomination information: {str(e)}",
            "status_code": getattr(e.response, "status_code", None)
        }


@mcp.tool()
def get_crsreport(
    product_code: str | None = None,
    offset: int = 0,
    limit: int = 20,
    from_datetime: str | None = None,
    to_datetime: str | None = None
) -> dict:
    """
    Retrieve CRS report information from the Congress.gov API.

    Args:
        product_code: Specific product code for CRS report
        offset: Starting record (default 0)
        limit: Maximum records to return (max 250, default 20)
        from_datetime: Start timestamp (YYYY-MM-DDTHH:MM:SSZ format)
        to_datetime: End timestamp (YYYY-MM-DDTHH:MM:SSZ format)

    Returns:
        dict: CRS report data from Congress.gov API
    """
    base_url = "https://api.congress.gov/v3/crsreport"

    url = base_url
    if product_code:
        url += f"/{product_code}"

    params = {
        "api_key": congress_gov_api_key,
        "format": "json",
        "offset": offset,
        "limit": min(limit, 250)
    }

    if from_datetime:
        params["fromDateTime"] = from_datetime
    if to_datetime:
        params["toDateTime"] = to_datetime

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        return {
            "error": f"Failed to retrieve CRS report information: {str(e)}",
            "status_code": getattr(e.response, "status_code", None)
        }


@mcp.tool()
def get_treaty(
    congress: int | None = None,
    treaty_number: int | None = None,
    offset: int = 0,
    limit: int = 20,
    from_datetime: str | None = None,
    to_datetime: str | None = None
) -> dict:
    """
    Retrieve treaty information from the Congress.gov API.

    Args:
        congress: Congress number (e.g., 118 for 118th Congress)
        treaty_number: Specific treaty number
        offset: Starting record (default 0)
        limit: Maximum records to return (max 250, default 20)
        from_datetime: Start timestamp (YYYY-MM-DDTHH:MM:SSZ format)
        to_datetime: End timestamp (YYYY-MM-DDTHH:MM:SSZ format)

    Returns:
        dict: Treaty data from Congress.gov API
    """
    base_url = "https://api.congress.gov/v3/treaty"

    url = base_url
    if congress:
        url += f"/{congress}"
        if treaty_number:
            url += f"/{treaty_number}"

    params = {
        "api_key": congress_gov_api_key,
        "format": "json",
        "offset": offset,
        "limit": min(limit, 250)
    }

    if from_datetime:
        params["fromDateTime"] = from_datetime
    if to_datetime:
        params["toDateTime"] = to_datetime

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        return {
            "error": f"Failed to retrieve treaty information: {str(e)}",
            "status_code": getattr(e.response, "status_code", None)
        }
