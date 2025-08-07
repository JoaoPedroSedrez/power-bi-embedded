import requests

# --- CONFIGURAÇÕES ---
TENANT_ID = "COLOQUE_SEU_TENANT_ID_AQUI"
CLIENT_ID = "COLOQUE_SEU_CLIENT_ID_AQUI"
CLIENT_SECRET = "COLOQUE_SEU_CLIENT_SECRET_AQUI"
WORKSPACE_ID = "COLOQUE_SEU_WORKSPACE_ID_AQUI"
REPORT_ID = "COLOQUE_SEU_REPORT_ID_AQUI"
# ---------------------

def get_access_token():
    url = f"https://login.microsoftonline.com/{TENANT_ID}/oauth2/v2.0/token"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    data = {
        "client_id": CLIENT_ID,
        "scope": "https://analysis.windows.net/powerbi/api/.default",
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials"
    }
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    return response.json()["access_token"]

def get_embed_token(access_token):
    url = f"https://api.powerbi.com/v1.0/myorg/groups/{WORKSPACE_ID}/reports/{REPORT_ID}/GenerateToken"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access_token}"
    }
    body = {
        "accessLevel": "View"
    }
    response = requests.post(url, headers=headers, json=body)
    response.raise_for_status()
    return response.json()["token"]

def main():
    print("Obtendo access token do Azure AD...")
    access_token = get_access_token()
    print("Gerando embed token do Power BI...")
    embed_token = get_embed_token(access_token)
    print("\nEmbed Token:\n")
    print(embed_token)

if __name__ == "__main__":
    main()
