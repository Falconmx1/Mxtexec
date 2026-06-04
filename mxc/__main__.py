#!/usr/bin/env python3
import argparse
import sys
from mxc.core.banner import show_banner
from mxc.protocols.smb import enum_shares, exec_command, check_null_session
from mxc.core.color import print_error, print_info

def main():
    show_banner()
    
    parser = argparse.ArgumentParser(
        description="Mxtexec - Herramienta de explotación de redes",
        epilog="Ejemplo: mxc smb 192.168.1.100 -u admin -p pass123 --shares"
    )
    
    parser.add_argument("protocol", choices=["smb", "winrm"], help="Protocolo a usar")
    parser.add_argument("target", help="IP o rango (ej: 192.168.1.1 o 192.168.1.0/24)")
    parser.add_argument("-u", "--username", help="Nombre de usuario")
    parser.add_argument("-p", "--password", help="Contraseña")
    parser.add_argument("-d", "--domain", default="", help="Dominio (opcional)")
    parser.add_argument("-t", "--timeout", type=int, default=5, help="Timeout en segundos")
    
    # Modos SMB
    parser.add_argument("--shares", action="store_true", help="Enumerar shares")
    parser.add_argument("--exec", "-x", help="Ejecutar comando en el target")
    parser.add_argument("--null-session", action="store_true", help="Probar null session")
    
    args = parser.parse_args()
    
    if args.protocol == "smb":
        if args.null_session:
            check_null_session(args.target)
        elif args.shares:
            if not args.username or not args.password:
                print_error("Se requieren -u y -p para enumerar shares")
                sys.exit(1)
            enum_shares(args.target, args.username, args.password, args.domain)
        elif args.exec:
            if not args.username or not args.password:
                print_error("Se requieren -u y -p para ejecutar comandos")
                sys.exit(1)
            exec_command(args.target, args.username, args.password, args.exec, args.domain)
        else:
            parser.print_help()
    elif args.protocol == "winrm":
        print_info("WinRM - Próximamente en la siguiente versión 🚀")

if __name__ == "__main__":
    main()
