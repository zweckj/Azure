import adal
import requests
import argparse

# get auth token from AAD
authentication_endpoint = 'https://login.microsoftonline.com/'
resource  = 'https://storage.azure.com/'


# Make sure that the application is storage blob data contributor on the storage account

clientid = "CLIENT_ID"
clientsecret = "CLIENT SECRET"
tenantid = "TENANT ID"

storageaccountname = "NAME OF STORAGE"
filesystem = "FILE SYSTEM NAME"
dirname = "DIRECTORY NAME"

context = adal.AuthenticationContext(authentication_endpoint + tenantid)
token_response = context.acquire_token_with_client_credentials(
    resource=resource,
    client_id=clientid,
    client_secret=clientsecret
)
access_token = token_response.get('accessToken')

# issue request to API
adlsFQDN = f'{storageaccountname}.dfs.core.windows.net'

recursive = "true"
resource = "filesystem"


headers = {"Authorization": 'Bearer ' + access_token}


# create file system
apiLink = f'https://{adlsFQDN}/{filesystem}?resource=filesystem'
response = requests.put(apiLink, headers=headers)
if response.status_code == 201:
    print(f'Filesystem "{filesystem}" created successfully')
else:
    print(f'Error for Filesystem {filesystem}: {response.text}')

# create directory 
apiLink = f'https://{adlsFQDN}/{filesystem}/{dirname}?resource=directory'
response = requests.put(apiLink, headers=headers)
if response.status_code == 201:
    print(f'Directory "{dirname}" created successfully')
else:
    print(f'Error while creating directory {dirname}: {response.text}')