from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

gauth = GoogleAuth()

gauth.LoadCredentialsFile("mycreds.txt")
if gauth.credentials is None:
    # Authenticate if they're not there
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    # Refresh them if expired
    gauth.Refresh()
else:
    # Initialize the saved creds
    gauth.Authorize()
# Save the current credentials to a file
gauth.SaveCredentialsFile("mycreds.txt")

drive = GoogleDrive(gauth)
service = gauth.service

def partial(total_byte_len, part_size_limit):
    s = []
    for p in range(0, total_byte_len, part_size_limit):
        last = min(total_byte_len - 1, p + part_size_limit - 1)
        s.append([p, last])
    return s


def GD_download_file(service, file_id):
    drive_file = service.files().get(fileId=file_id).execute()
    download_url = drive_file.get('downloadUrl')
    print(download_url)
    total_size = int(drive_file.get('fileSize'))
    s = partial(total_size, 100000000) # I'm downloading BIG files, so 100M chunk size is fine for me
    title = drive_file.get('title')
    originalFilename = drive_file.get('originalFilename')
    filename = './' + originalFilename
    if download_url:
      with open(filename, 'wb') as file:
        print ("Bytes downloaded: ")
        for bytes in s:
          headers = {"Range" : 'bytes=%s-%s' % (bytes[0], bytes[1])}
          resp, content = service._http.request(download_url, headers=headers)
          if resp.status == 206 :
                file.write(content)
                file.flush()
          else:
            print ('An error occurred: %s' % resp)
            return None
          print (str(bytes[1])+"...")
      return title, filename
    else:
        return None 
##file1 = drive.CreateFile({'title': 'Hello.txt'})
##file1.SetContentString('Hello')
##file1.Upload() # Files.insert()
##
##file1['title'] = 'HelloWorld.txt'  # Change title of the file
##file1.Upload() # Files.patch()
##
##print('title: %s, id: %s' % (file1['title'], file1['id']))

##file_list = drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
##for folder in file_list:
##    if folder['title'] == 'SangoshthiData' :
##        folder_id = folder['id']
##        print ('title: %s, id: %s' % (folder['title'], folder['id']))

folder_id = '0B2rV9xjC8b9VTFZXYzdwS2JRWjg'

##file1 = drive.CreateFile({'title': 'hello.txt' , 'parents': [{'kind': 'drive#fileLink' , 'id': folder_id}]})
##file1['title'] = 'HelloWorld.txt'
##file1.SetContentString('Hello')
##file1.Upload() # Files.insert()

file_list = drive.ListFile({'q': "'%s' in parents and trashed=false" % folder_id}).GetList()
  
for file1 in file_list:
    print('title: %s, id: %s' % (file1['title'], file1['id']))
    if file1['title'] == "V1.avi":
        FILE_ID = file1['id']
    #file1.GetContentFile(file1)

    
# Change title of the file
#file1.Upload() # Files.patch()

#print('title: %s, id: %s' % (file1['title'], file1['id']))

GD_download_file(service, FILE_ID) 

