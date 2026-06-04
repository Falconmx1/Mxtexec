#!/usr/bin/env python3
import argparse
import sys
from mxc.core.banner import show_banner
from mxc.core.scanner import Scanner
from mxc.core.proxy import SocksProxy
from mxc.protocols.smb import enum_shares, exec_command, check_null_session
from mxc.protocols.winrm import WinRMClient
from mxc.modules.dumper import HashDumper
from mxc.modules.postexploit import PostExploit
from mxc.core.color import print_error, print_info, print_success

def main():
    show_banner()
    
    parser = argparse.ArgumentParser(
        description="Mxtexec - Herramienta de explotación de redes con caparazón de tortuga",
        epilog="""
Ejemplos:
  mxc smb 192.168.1.0/24 -u admin -p pass123 --shares              # Escaneo CIDR masivo
  mxc smb 192.168.1.100 -u admin -p pass123 --exec "whoami"       # Ejecutar comando
  mxc winrm 192.168.1.100 -u admin -p pass123 --interactive       # Shell interactivo
  mxc smb 192.168.1.100 -u admin -p pass123 --dump-hashes         # Dumpear hashes
  mxc proxy --start --port 1080                                    # SOCKS proxy
  mxc winrm 192.168.1.100 -u admin -p pass123 --post-exploit      # Módulos post-explotación
        """
    )
    
    parser.add_argument("protocol", choices=["smb", "winrm", "proxy"], help="Protocolo a usar")
    parser.add_argument("target", nargs="?", help="IP, rango CIDR o none para proxy")
    parser.add_argument("-u", "--username", help="Nombre de usuario")
    parser.add_argument("-p", "--password", help="Contraseña")
    parser.add_argument("-d", "--domain", default="", help="Dominio (opcional)")
    parser.add_argument("-t", "--threads", type=int, default=20, help="Hilos para escaneo masivo")
    
    # Modos SMB
    parser.add_argument("--shares", action="store_true", help="Enumerar shares")
    parser.add_argument("--exec", "-x", help="Ejecutar comando en el target")
    parser.add_argument("--null-session", action="store_true", help="Probar null session")
    parser.add_argument("--dump-hashes", action="store_true", help="Dumpear hashes (secretsdump)")
    
    # Modos WinRM
    parser.add_argument("--interactive", action="store_true", help="Shell interactivo por WinRM")
    parser.add_argument("--script", help="Ejecutar script PowerShell remoto")
    parser.add_argument("--post-exploit", action="store_true", help="Ejecutar módulos de post-explotación")
    parser.add_argument("--upload", nargs=2, metavar=("LOCAL", "REMOTE"), help="Subir archivo")
    parser.add_argument("--download", nargs=2, metavar=("REMOTE", "LOCAL"), help="Descargar archivo")
    parser.add_argument("--add-admin", nargs=2, metavar=("USER", "PASS"), help="Agregar usuario admin")
    parser.add_argument("--enable-rdp", action="store_true", help="Habilitar RDP")
    parser.add_argument("--dump-wifi", action="store_true", help="Dumpear contraseñas WiFi")
    
    # Modo Proxy
    parser.add_argument("--start", action="store_true", help="Iniciar servidor SOCKS proxy")
    parser.add_argument("--port", type=int, default=1080, help="Puerto para proxy SOCKS")
    parser.add_argument("--remote-host", default="127.0.0.1", help="Host remoto para proxy")
    parser.add_argument("--remote-port", type=int, default=1080, help="Puerto remoto para proxy")
    
    args = parser.parse_args()
    
    # Modo Proxy
    if args.protocol == "proxy" and args.start:
        proxy = SocksProxy(args.port, args.remote_host, args.remote_port)
        try:
            proxy.start()
        except KeyboardInterrupt:
            proxy.stop()
        return
    
    if not args.target:
        print_error("Se requiere target (IP o rango CIDR)")
        sys.exit(1)
    
    # Escaneo con CIDR y multithreading
    if '/' in args.target and (args.shares or args.null_session):
        scanner = Scanner(threads=args.threads)
        
        if args.null_session:
            results = scanner.scan([args.target], check_null_session)
            for ip, result in results:
                if result:
                    print_success(f"{ip}: Null session permitida")
        
        elif args.shares:
            if not args.username or not args.password:
                print_error("Se requieren -u y -p para enumerar shares")
                sys.exit(1)
            results = scanner.scan([args.target], enum_shares, args.username, args.password, args.domain)
        
        return
    
    # Modo SMB
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
        elif args.dump_hashes:
            if not args.username or not args.password:
                print_error("Se requieren -u y -p para dumpear hashes")
                sys.exit(1)
            dumper = HashDumper(args.target, args.username, args.password, args.domain)
            dumper.dump_ntds()
        else:
            parser.print_help()
    
    # Modo WinRM
    elif args.protocol == "winrm":
        if args.interactive:
            client = WinRMClient(args.target, args.username, args.password, args.domain)
            client.interactive_shell()
        elif args.script:
            client = WinRMClient(args.target, args.username, args.password, args.domain)
            if client.connect():
                output = client.run_script(args.script)
                if output:
                    print(output)
        elif args.post_exploit:
            if not args.username or not args.password:
                print_error("Se requieren -u y -p para post-explotación")
                sys.exit(1)
            post = PostExploit(args.target, args.username, args.password, "winrm")
            post.get_system_info()
        elif args.upload:
            if not args.username or not args.password:
                print_error("Se requieren -u y -p para subir archivos")
                sys.exit(1)
            post = PostExploit(args.target, args.username, args.password, "winrm")
            post.upload_file(args.upload[0], args.upload[1])
        elif args.download:
            if not args.username or not args.password:
                print_error("Se requieren -u y -p para descargar archivos")
                sys.exit(1)
            post = PostExploit(args.target, args.username, args.password, "winrm")
            post.download_file(args.download[0], args.download[1])
        elif args.add_admin:
            if not args.username or not args.password:
                print_error("Se requieren credenciales actuales")
                sys.exit(1)
            post = PostExploit(args.target, args.username, args.password, "winrm")
            post.add_admin_user(args.add_admin[0], args.add_admin[1])
        elif args.enable_rdp:
            if not args.username or not args.password:
                print_error("Se requieren credenciales")
                sys.exit(1)
            post = PostExploit(args.target, args.username, args.password, "winrm")
            post.enable_rdp()
        elif args.dump_wifi:
            if not args.username or not args.password:
                print_error("Se requieren credenciales")
                sys.exit(1)
            post = PostExploit(args.target, args.username, args.password, "winrm")
            post.dump_wifi_passwords()
        else:
            parser.print_help()

if __name__ == "__main__":
    main()
