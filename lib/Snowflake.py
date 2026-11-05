import os

import requests
from snowflake.sqlalchemy import URL
from sqlalchemy import create_engine


def oauth_token_request(username: str, password: str):
    """
    This function sends a request to retrieve an OAuth token for the Snowflake connection 
    using the user's credentials.

    Args:
        username: Data warehouse network username
        password: Network password supplied interactively
    Returns:
        An OAuth token for Snowflake connection
    """

    curl_url = os.getenv("SNOWFLAKE_OAUTH_TOKEN_URL", "")
    client_id = os.getenv("SNOWFLAKE_OAUTH_CLIENT_ID", "")
    client_secret = os.getenv("SNOWFLAKE_OAUTH_CLIENT_SECRET", "")

    if not curl_url or not client_id:
        raise ValueError(
            "Configure SNOWFLAKE_OAUTH_TOKEN_URL and SNOWFLAKE_OAUTH_CLIENT_ID "
            "before connecting."
        )
    
    curl_data = {
        "client_id": client_id,
        "grant_type": "password",
        "username": username,
        "password": password,
        "client_secret": client_secret,
        "scope": "session:role-any"
    }
    response = requests.post(curl_url, data=curl_data, timeout=30)
    response.raise_for_status()
    oauth_token = response.json()
    
    if "access_token" not in oauth_token:
        error_msg = oauth_token.get("error_description", oauth_token.get("error", str(oauth_token)))
        raise ValueError(f"OAuth token request failed: {error_msg}")
    
    return oauth_token["access_token"]




def open_connection(oauth_token, username: str):
    """
    This function takes an OAuth token and creates the Snowflake connection using the
    setup below. Users need access to the configured Snowflake data cloud before connecting.
    Users can modify the database, schema, warehouse, role, etc. as needed.

    Args:
        oauth_token: An OAuth token for Snowflake connection
        username: The data warehouse username

    Returns:
        A configured Snowflake SQLAlchemy engine
    """

    account = os.getenv("SNOWFLAKE_ACCOUNT")
    database = os.getenv("SNOWFLAKE_DATABASE", "EXAMPLE_DATA")
    warehouse = os.getenv("SNOWFLAKE_WAREHOUSE", "EXAMPLE_WH")
    role = os.getenv("SNOWFLAKE_ROLE", "PUBLIC")

    if not account:
        raise ValueError("Configure SNOWFLAKE_ACCOUNT before connecting.")

    engine = create_engine(URL(
        account=account,
        authenticator='oauth',
        token=oauth_token,
        user=username,
        database=database,
        warehouse=warehouse,
        role=role,
    ))
    return engine
