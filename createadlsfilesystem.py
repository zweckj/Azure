import adal
import requests

authentication_endpoint = 'https://login.microsoftonline.com/'
resource  = 'https://storage.azure.com/'


# Make sure that the application is storage blob data contributor on the storage account

# application settings
clientid = "CLIENT_ID"
clientsecret = "CLIENT SECRET"
tenantid = "TENANT ID"

# name of storage account
storageaccountname = "NAME OF STORAGE"
# name of file system to create
filesystem = "FILE SYSTEM NAME"
# name of directory to create
dirname = "DIRECTORY NAME"

# get auth token from AAD
context = adal.AuthenticationContext(authentication_endpoint + tenantid)
token_response = context.acquire_token_with_client_credentials(
    resource=resource,
    client_id=clientid,
    client_secret=clientsecret
)
access_token = token_response.get('accessToken')

# create API endpoint url
adlsFQDN = f'{storageaccountname}.dfs.core.windows.net'

# create authorization header
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
