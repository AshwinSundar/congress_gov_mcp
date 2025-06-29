# <span>Congress.gov</span> MCP server

[![smithery badge](https://smithery.ai/badge/@AshwinSundar/congress_gov_mcp)](https://smithery.ai/server/@AshwinSundar/congress_gov_mcp)

Ever wonder what our (US) Congress is up to? Tired of reading the news to find out? Ask the US Congress API yourself.

Unofficial MCP server for the [Congress.gov API](https://api.congress.gov)

## Installation

### Installing via Smithery

To install congress_gov_mcp for Claude Desktop automatically via [Smithery](https://smithery.ai/server/@AshwinSundar/congress_gov_mcp):

```bash
npx -y @smithery/cli install @AshwinSundar/congress_gov_mcp --client claude
```

### Manual Installation

#### Prerequisites

1. Install [uv](https://docs.astral.sh/uv/getting-started/installation/). The easiest way on macOS and Linux is:
    ```
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```
2. Get a [Congress.gov API key](https://api.congress.gov/sign-up/).

3. Install Claude Desktop, Claude Code, or another client that supports [MCP Integrations](https://modelcontextprotocol.io/clients)


#### Initial Setup

1. Complete [Prerequisites](#Prerequisites)
2. Clone this repository, and `cd` in:

    ```
    git clone http://github.com/AshwinSundar/congress_gov_mcp
    ```

    ```
    cd congress_gov_mcp
    ```

3. Install dependencies:

    ```
    uv sync
    ```

3. Create a `.env` file from the template:

    ```
    cp .env.template .env
    ```

4. Add your Congress.gov API key to the `.env` file:

><u>congress_gov_mcp/.env</u>
>```
>CONGRESS_GOV_API_KEY="your-api-key-here"
>```

### Client Configuration

#### Claude Desktop

1. Complete [Prerequisites](#Prerequisites)

2. Copy the absolute path to your `uv` installation:

```
which uv
```
2. Add the following to your Claude Desktop configuration file, inside the `mcpServers` block:

    **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`

    **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "congress_gov_mcp": {
      "command": "/absolute_path/to/uv",
      "args": [
        "run",
        "/absolute_path_to/congress_gov_mcp/server.py"
      ]
    }
  }
}

````

#### Claude Code

1. Complete [Prerequisites](#Prerequisites)

2. Add the following to `.mcp.json` in the directory you are running Claude Code in, inside the `mcpServers` block:

```json
{
  "mcpServers": {
    "congress_gov_mcp": {
      "command": "uv",
      "args": [
        "run",
        "/absolute_path_to/congress_gov_mcp/server.py"
      ]
    }
  }
}

````

## Roadmap

- [x] api.congress.gov
    - [x] /bill
        - [x] /{congress}
        - [x] /{congress}/{billType}
        - [x] /{congress}/{billType}/{billNumber}
            - [ ] /actions
            - [ ] /amendments
            - [ ] /committees
            - [ ] /cosponsors
            - [ ] /relatedbills
            - [ ] /subjects
            - [ ] /summaries
            - [ ] /text
            - [ ] /titles
    - [x] /amendment
        - [x] /{congress}
        - [x] /{congress}/{amendmentType}
        - [x] /{congress}/{amendmentType}/{amendmentNumber}
            - [ ] /actions
            - [ ] /cosponsors
            - [ ] /amendments
            - [ ] /text
    - [x] /summaries
        - [x] /{congress}
        - [x] /{congress}/{billType}
    - [x] /congress
        - [x] /{congress}
        - [ ] /current
    - [x] /member
        - [x] /{bioguideId}
            - [ ] /sponsored-legislation
            - [ ] /cosponsored-legislation
    - [x] /committee
        - [x] /{systemCode}
            - [ ] /bills
            - [ ] /reports
            - [ ] /nominations
            - [ ] /meetings
            - [ ] /hearings
            - [ ] /house-communication
            - [ ] /senate-communication
    - [x] /committee-report
        - [x] /{congress}
        - [x] /{congress}/{reportType}
        - [x] /{congress}/{reportType}/{reportNumber}
            - [ ] /text
    - [x] /committee-print
        - [x] /{congress}
        - [x] /{congress}/{printType}
        - [x] /{congress}/{printType}/{printNumber}
            - [ ] /text
    - [x] /committee-meeting
        - [x] /{congress}
        - [x] /{congress}/{chamber}
            - [ ] /meetings
    - [x] /hearing
        - [x] /{congress}
        - [x] /{congress}/{chamber}
        - [x] /{congress}/{chamber}/{hearingNumber}
    - [x] /house-vote
        - [x] /{congress}
        - [x] /{congress}/{session}
        - [x] /{congress}/{session}/{rollCallNumber}
    - [x] /congressional-record
        - [x] /{volume}
        - [x] /{volume}/{pagePrefix}
        - [x] /{volume}/{pagePrefix}/{pageNumber}
    - [x] /daily-congressional-record
        - [x] /{volume}
        - [x] /{volume}/{issue}
    - [x] /bound-congressional-record
        - [x] /{year}
        - [x] /{year}/{month}
        - [x] /{year}/{month}/{day}
    - [x] /house-communication
        - [x] /{congress}
        - [x] /{congress}/{communicationType}
        - [x] /{congress}/{communicationType}/{communicationNumber}
    - [x] /house-requirement
        - [x] /{congress}
        - [x] /{congress}/{requirementNumber}
    - [x] /senate-communication
        - [x] /{congress}
        - [x] /{congress}/{communicationType}
        - [x] /{congress}/{communicationType}/{communicationNumber}
    - [x] /nomination
        - [x] /{congress}
        - [x] /{congress}/{nominationNumber}
            - [ ] /actions
            - [ ] /hearings
    - [x] /crsreport
        - [x] /{productCode}
    - [x] /treaty
        - [x] /{congress}
        - [x] /{congress}/{treatyNumber}
            - [ ] /actions
            - [ ] /committees
