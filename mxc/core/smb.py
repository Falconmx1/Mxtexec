from mxc.core.connection import MxcConnection
from mxc.core.color import print_success, print_error, print_info, print_warning

def enum_shares(target, username, password, domain=""):
    """Enumerar shares SMB"""
    conn = MxcConnection(target, username, password, domain)
    if not conn.smb_connect():
        return
    
    try:
        shares = conn.conn.listShares()
        print_info(f"Shares encontradas en {target}:")
        print("─" * 50)
        for share in shares:
            name = share['shi1_netname']
            remark = share['shi1_remark']
            if name.endswith('$'):
                print(f"  🔒 {name} - {remark}")  # Hidden share
            else:
                print(f"  📁 {name} - {remark}")
        print("─" * 50)
        print_success(f"Total: {len(shares)} shares encontradas")
    except Exception as e:
        print_error(f"Error enumerando shares: {e}")

def exec_command(target, username, password, command, domain=""):
    """Ejecutar comando por SMB"""
    conn = MxcConnection(target, username, password, domain)
    if not conn.smb_connect():
        return
    
    print_info(f"Ejecutando: {command}")
    conn.smb_exec(command)

def check_null_session(target):
    """Probar null session (sin credenciales)"""
    print_info(f"Probando null session en {target}")
    conn = MxcConnection(target, "", "")
    if conn.smb_connect():
        print_success(f"NULL SESSION permitida en {target} - VULNERABLE!")
        return True
    else:
        print_warning("Null session no permitida")
        return False
