from .WorkingDirectory import Directory

class CommandParser:

    args = None
    command = None
    drive_handler = None

    def __init__(self, cmd, drive_handler):

        self.args = cmd[1:]
        self.command = cmd[0]
        self.commands = {
            'ls': self.ls,
            'cd': self.cd,
            'du': self.du,
            'cp': self.cp,
            'mv': self.mv,
            'up': self.up,
            'cat': self.cat,
            'find': self.find,
            'down': self.down,
            'mkdir': self.mkdir,
            'touch': self.touch,
        }
        self.drive_handler = drive_handler

    def handle_args(self):

        try:
            self.commands[self.command](self.args)
        except KeyError:
            print("Command not found")

    def ls(self, args):

        current_directory = Directory.current_directory['dir_key']
        Directory.current_directory['objects'] = self.drive_handler.list_folder_content(current_directory)

        for object_directory in Directory.current_directory['objects']:

            print(object_directory['object_title'], object_directory['object_id'])

    def cd(self, args):

        if args[0] == '..':
            
            Directory.current_directory['dir_key'] = Directory.prev_directory
            return

        if args[0] == '/':

            Directory.current_directory['dir_key'] = 'root'
            return
        
        #VERIFICAR SE TEM NO CACHE, SE NÃO PROCURA LÁ
        Directory.prev_directory = Directory.current_directory['dir_key']
        Directory.current_directory['dir_key'] = args[0]

    def du(self, args):

        bytes_length = self.drive_handler.get_folder_size(args[0])
        print('%d bytes' % bytes_length)

    def mkdir(self, args):

        self.drive_handler.create_folder(args[0],  Directory.current_directory['dir_key'])

    def cat(self, args):

        # Commented because there's an error while get file content
        
        # print(self.drive_handler.get_file_content(args[0]))
        pass

    def find(self, args):

        # Search for files
        pass

    def touch(self, args):

        # Create files
        pass

    def cp(self, args):

        # Copying files and folders
        pass

    def mv(self, args):

        # Moving files and folders
        pass

    def down(self, args):

        # Commented because there's a error when setting download path
        
        #self.drive_handler.download_file(args[0], args[1])
        pass

    def up(self, args):

        # Commented because I need to find a way to set the local file path uma vez que estamos in a virtual console

        # import os
        # arquivo = os.path.abspath(args[0])
        # self.drive_handler.upload_file(arquivo, Directory.current_directory['dir_key'])
        pass

    def share(self, args):

        # Handle all stuff's related to share option in Google Drive
        pass
    
