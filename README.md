# 🔗 Site Address Matcher

A portfolio demonstration of a Streamlit application that matches research site addresses against a master address dataset using semantic embeddings and fuzzy matching.

> This repository uses generic configuration and synthetic identifiers. It does not contain employer-specific credentials, proprietary data, or real study records.

## Features

- **SSO-ready Login**: Authentication through an organization-configured OAuth endpoint
- **Semantic Matching**: Uses sentence-transformer embeddings for intelligent address matching
- **Multi-Stage Pipeline**: Cascading matching against DD, LONG_CTMS, CITELINE, and SHORT_CTMS sources
- **Real-time Progress**: Visual progress tracking during matching
- **Export Results**: Download matched results as CSV

## Prerequisites

- Python 3.9+
- Access to a configured Snowflake account
- Valid credentials for your configured OAuth provider

## Installation

1. Clone the repository:
```bash
git clone <your-repository-url>/site-address-matcher.git
cd site-address-matcher
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

Set these environment variables for your own test environment:

```text
SNOWFLAKE_OAUTH_TOKEN_URL=https://example-idp.example.com/oauth/token
SNOWFLAKE_OAUTH_CLIENT_ID=example-client-id
SNOWFLAKE_OAUTH_CLIENT_SECRET=example-client-secret
SNOWFLAKE_ACCOUNT=example_account.region
SNOWFLAKE_DATABASE=EXAMPLE_DATA
SNOWFLAKE_WAREHOUSE=EXAMPLE_WH
SNOWFLAKE_ROLE=PUBLIC
```

Do not commit real environment values or credentials.

## Usage

1. Run the application:
```bash
streamlit run app.py
```

2. Login with credentials for your configured identity provider

3. Upload a CSV file with the following columns:
   - `site_business_name`: Site/facility name
   - `address_line_1`: Street address
   - `city`: City name
   - `state`: State code (e.g., "CA", "NY")
   
   (if exists --> `zip` or `postal_code`: ZIP/postal code)

4. Click "Start Matching" and wait for results

5. Download the matched results

## Input File Format

Your CSV should have these columns:
| Column | Required | Description |
|--------|----------|-------------|
| site_business_name | Yes | Name of the site/facility |
| address_line_1 | Yes | Street address |
| city | Yes | City name |
| state | Yes | State code |

## Output

The output CSV includes:
- Original input columns
- `matched_site_id`: Matched master-site ID
- `platinum_name`: Matched site name
- `matched_address`: Matched address
- `confidence_score`: Match confidence (0-1)
- `source_type`: Match source (DD, LONG_CTMS, etc.)

## Project Structure

```
site-address-matcher/
├── app.py                 # Main Streamlit application
├── lib/
│   ├── __init__.py
│   ├── Snowflake.py       # Snowflake connection utilities
│   └── Queries.py         # SQL queries (if needed)
├── requirements.txt       # Python dependencies
├── .gitignore
└── README.md
```

## Security Notes

- Credentials and OAuth tokens are stored only in Streamlit session memory
- Environment variables are used instead of embedded secrets
- No passwords are saved to disk or logged
- OAuth tokens expire after 1 hour
- Example SQL and identifiers are synthetic and contain no real study participants
- Do not add employer-owned data to a public repository
