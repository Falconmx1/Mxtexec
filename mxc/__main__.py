import argparse
from mxc.core.banner import show_banner
from mxc.protocols.smb import enum_shares

def main():
    show_banner()
    parser = argparse.ArgumentParser(description="Mxtexec - Network execution tool")
    parser.add_argument("protocol", choices=["smb", "winrm"], help="Protocol to use")
    parser.add_argument("target", help="Target IP or range")
    parser.add_argument("-u", "--username", help="Username")
    parser.add_argument("-p", "--password", help="Password")
    parser.add_argument("--shares", action="store_true", help="Enumerate SMB shares")

    args = parser.parse_args()

    if args.protocol == "smb" and args.shares:
        enum_shares(args.target, args.username, args.password)

if __name__ == "__main__":
    main()
