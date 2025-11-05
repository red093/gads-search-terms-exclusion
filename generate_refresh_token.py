#!/usr/bin/env python3
"""
Google Ads API Refresh Token Generator

This script helps you generate a refresh token for the Google Ads API.
The refresh token is used for authentication and can be reused indefinitely.

Usage:
    python generate_refresh_token.py

You will need:
1. Client ID from Google Cloud Console
2. Client Secret from Google Cloud Console
3. A web browser to authorize the application
"""

import sys
from google_auth_oauthlib.flow import InstalledAppFlow


# The scope for the Google Ads API
SCOPES = ['https://www.googleapis.com/auth/adwords']

# Google's OAuth2 endpoints
AUTHORIZATION_URL = 'https://accounts.google.com/o/oauth2/v2/auth'
TOKEN_URI = 'https://oauth2.googleapis.com/token'


def main():
    """Generate a refresh token for Google Ads API."""

    print("="*70)
    print("Google Ads API - Refresh Token Generator")
    print("="*70)
    print()
    print("This script will help you generate a refresh token for Google Ads API.")
    print("You will need your Client ID and Client Secret from Google Cloud Console.")
    print()
    print("Steps:")
    print("1. Enter your Client ID and Client Secret below")
    print("2. A browser window will open for you to authorize the application")
    print("3. Sign in with the Google account that has access to Google Ads")
    print("4. Grant the requested permissions")
    print("5. The refresh token will be displayed")
    print()
    print("="*70)
    print()

    # Get client credentials from user
    client_id = input("Enter your Client ID: ").strip()
    if not client_id:
        print("Error: Client ID is required")
        sys.exit(1)

    client_secret = input("Enter your Client Secret: ").strip()
    if not client_secret:
        print("Error: Client Secret is required")
        sys.exit(1)

    print()
    print("Starting OAuth2 flow...")
    print("A browser window will open. Please authorize the application.")
    print()

    # Create OAuth2 flow
    client_config = {
        "installed": {
            "client_id": client_id,
            "client_secret": client_secret,
            "auth_uri": AUTHORIZATION_URL,
            "token_uri": TOKEN_URI,
        }
    }

    try:
        flow = InstalledAppFlow.from_client_config(
            client_config,
            scopes=SCOPES
        )

        # Run the OAuth flow
        # This will open a browser window for authorization
        credentials = flow.run_local_server(port=0)

        print()
        print("="*70)
        print("SUCCESS! Your refresh token has been generated.")
        print("="*70)
        print()
        print("Copy the following information to your google-ads.yaml file:")
        print()
        print(f"client_id: {client_id}")
        print(f"client_secret: {client_secret}")
        print(f"refresh_token: {credentials.refresh_token}")
        print()
        print("="*70)
        print()
        print("IMPORTANT: Keep your refresh token secure!")
        print("- Do not share it with anyone")
        print("- Do not commit it to version control")
        print("- It provides access to your Google Ads account")
        print()
        print("The refresh token does not expire unless you revoke it.")
        print("="*70)

    except Exception as e:
        print()
        print(f"Error: {e}")
        print()
        print("Troubleshooting:")
        print("1. Make sure your Client ID and Client Secret are correct")
        print("2. Ensure you've enabled the Google Ads API in Google Cloud Console")
        print("3. Check that your OAuth consent screen is configured")
        print("4. Verify the redirect URI includes http://localhost")
        sys.exit(1)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(0)
