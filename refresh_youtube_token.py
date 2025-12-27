import os
import pickle
import base64
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

# Scopes required for YouTube API
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def refresh_token():
    """
    Forces a new authentication flow and prints the Base64 encoded token 
    for use in GitHub Actions.
    """
    print("=" * 60)
    print("YouTube Token Refresher for GitHub Actions")
    print("=" * 60)
    
    # 1. Clear existing token to force re-authentication
    if os.path.exists("token.pickle"):
        print("\n[1] Removing old token.pickle...")
        os.remove("token.pickle")
    
    # 2. Check for client_secrets.json
    if not os.path.exists("client_secrets.json"):
        print("\n[!] ERROR: client_secrets.json not found!")
        print("Please download your OAuth 2.0 Client Credentials from Google Cloud Console")
        print("and save them as 'client_secrets.json' in this directory.")
        return

    # 3. Run the authentication flow
    print("\n[2] Starting authentication flow...")
    print("A browser window will open. Please log in and authorize the application.")
    
    flow = InstalledAppFlow.from_client_secrets_file("client_secrets.json", SCOPES)
    creds = flow.run_local_server(port=0)
    
    # 4. Save the new token
    with open("token.pickle", "wb") as token:
        pickle.dump(creds, token)
    print("\n[3] Successfully created new token.pickle.")

    # 5. Convert to Base64 for GitHub Secrets
    with open("token.pickle", "rb") as f:
        token_data = f.read()
        base64_token = base64.b64encode(token_data).decode('utf-8')
    
    print("\n" + "=" * 60)
    print("SUCCESS! Follow these steps to update GitHub Actions:")
    print("=" * 60)
    print("\n1. Copy the long Base64 string below:")
    print("-" * 60)
    print(base64_token)
    print("-" * 60)
    print("\n2. Go to your GitHub Repository")
    print("3. Settings -> Secrets and variables -> Actions")
    print("4. Update 'TOKEN_PICKLE_BASE64' with this new value.")
    print("\n" + "=" * 60)

if __name__ == "__main__":
    refresh_token()
