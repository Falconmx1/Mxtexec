from impacket.smbconnection import SMBConnection

class MxcConnection:
    def __init__(self, target, username, password, domain=""):
        self.target = target
        self.username = username
        self.password = password
        self.domain = domain
        self.conn = None

    def smb_connect(self):
        try:
            self.conn = SMBConnection(self.target, self.target)
            self.conn.login(self.username, self.password, self.domain)
            print(f"[+] SMB login successful on {self.target}")
            return True
        except Exception as e:
            print(f"[-] SMB failed on {self.target}: {e}")
            return False
