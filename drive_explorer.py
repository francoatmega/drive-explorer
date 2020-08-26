import sys
import getopt
from DriveExplorer import GoogleDriveWrapper
from DriveExplorer import CommandParser

def main():

    try:

        drive = GoogleDriveWrapper("creds")

        while True:

            # Look if 
            command_input = input('>>>  ')

            cmd = command_input.split(' ')
            CommandParser(cmd, drive).handle_args()

    except KeyboardInterrupt:

        sys.exit(0)

if __name__ == "__main__":

    main()