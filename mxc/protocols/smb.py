from mxc.core.connection import MxcConnection

def enum_shares(target, username, password, domain=""):
    conn = MxcConnection(target, username, password, domain)
    if not conn.smb_connect():
        return
    try:
        shares = conn.conn.listShares()
        print(f"\n[+] Shares on {target}:")
        for share in shares:
            print(f"  📁 {share['shi1_netname']} - {share['shi1_remark']}")
    except Exception as e:
        print(f"[-] Error enumerating shares: {e}")
