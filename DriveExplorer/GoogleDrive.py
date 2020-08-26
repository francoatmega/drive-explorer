import os
import time

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive
from pydrive.files import ApiRequestError


class GoogleDriveWrapper:

    drive = None

    def __init__(self, creds_path):

        try:

            gauth = GoogleAuth()

            gauth.LoadCredentialsFile(creds_path)

            if gauth.credentials is None:

                gauth.LocalWebserverAuth()

            if gauth.access_token_expired:
                
                gauth.Refresh()
    
            gauth.Authorize()
            gauth.SaveCredentialsFile(creds_path)

            self.drive = GoogleDrive(gauth)

        except Exception as e:

            print(str(e))

    def list_folder_content(self, folderId):

        content = []

        try:
            
            obj_list = self.drive.ListFile({'q': f"'{folderId}' in parents and trashed=false"}).GetList()

            for obj in obj_list:

                if 'fileSize' in obj:

                    content.append({
                        'object_id': obj['id'], 
                        'object_title': obj['title'], 
                        'object_size': obj['fileSize']
                    })
                    continue

                content.append({
                    'object_id': obj['id'], 
                    'object_title': obj['title'], 
                    'object_size': None
                })

            return content

        except Exception as e:

            print(str(e))

    def get_folder_size(self, folder):

        try:

            total = 0

            objects = self.drive.ListFile({'q': f"'{folder}' in parents and trashed=false"}).GetList()

            for obj in objects:

                if 'fileSize' in obj:

                    total += int(obj['fileSize'])
                    print(obj['title'], obj['fileSize'])
                    continue
                
                total += self.get_folder_size(obj['id'])

            return total

        except Exception as e:

            print(e)

    def create_folder(self, folder_name, parent):

        try:

            folder_metadata = {
                'title': folder_name, 
                'mimeType': 'application/vnd.google-apps.folder',
                'parents': [
                    {
                        'id':parent
                    }
                ]
            }

            folder = self.drive.CreateFile(folder_metadata)
            folder.Upload()

        except Exception as e:

            print(e)

    def get_file_content(self, file_id):

        try:

            current_file = self.drive.CreateFile({'id': file_id})
            return current_file.GetContentString()

        except Exception as e:

            print(e)

    def download_file(self, file_id, local_file):

        try:

            current_file = self.drive.CreateFile({'id': file_id})
            current_file.GetContentFile(local_file)

        except Exception as e:

            print(e)

    def upload_file(self, local_file, parent):

        try:

            fname = local_file.split("/")

            current_file = self.drive.CreateFile({
                'title': fname[len(fname) - 1], 
                'parents': [
                    {
                        'id': parent
                    }
                ]
            })

            current_file.SetContentFile(local_file)
            current_file.Upload()

        except Exception as e:

            print(e)