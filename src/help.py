import sys

def show_help():
    if (len(sys.argv) == 1 or (len(sys.argv) == 2 and sys.argv[1] == "help" or sys.argv[1] == "-h")):
        print("USAGE")
        print("\t./channel_download {link_to_channel}")
        sys.exit(0)
