SharepointIO
=============

An easy use of Office365-REST-Python-Client to download/upload/list sharepoint files

**********
How to use
**********

Init sharepoint connexion
*************************

from sharepointio import sharepointio

tenant = 'https://mypersonnal.sharepoint.com'

site = '/sites/12345-MyTeams-Channel'

sharepoint = sharepointio.SharePointBytesIO(tenant, site, username=USERNAME, password=PASSWORD)

********
Commands
********

**sharepoint.read(path)** : 
Read file in the given path



**sharepoint.list_files(folder, site=None, keep_only=None, start_with=None, str_contains=None)** :
List all files in a folder


**sharepoint.list_folders(folder)** :
List all folders in a folder


**sharepoint.move(file, old_path, new_path, site=None)** :
Move file to another directory


**sharepoint.copy(old_path, new_path)** :
Copy file to another directory


**sharepoint.download(file, folder=None, site=None, download_path=None, get_download_path=False)** :
Download file in a temporary directory

*******
License
*******

SharepointIO is licensed under the Apache 2.0 license.