import winrm
from mxc.core.color import print_success, print_error, print_info

class WinRMClient:
    def __init__(self, target, username, password, domain=""):
        self.target = target
        self.username = username
        self.password = password
        self.domain = domain
        self.session = None
    
    def connect(self):
        """Establecer conexión WinRM"""
        try:
            endpoint = f"http://{self.target}:5985/wsman"
            if self.domain:
                username = f"{self.domain}\\{self.username}"
            else:
                username = self.username
            
            self.session = winrm.Session(
                endpoint,
                auth=(username, self.password),
                transport='ntlm',
                server_cert_validation='ignore'
            )
            # Probar conexión
            result = self.session.run_cmd("whoami")
            if result.status_code == 0:
                print_success(f"WinRM conectado a {self.target} como {username}")
                return True
            else:
                print_error(f"Error de autenticación WinRM: {result.std_err.decode()}")
                return False
        except Exception as e:
            print_error(f"Error conectando a WinRM: {e}")
            return False
    
    def run_command(self, command):
        """Ejecutar comando y retornar output"""
        try:
            result = self.session.run_cmd(command)
            if result.status_code == 0:
                return result.std_out.decode()
            else:
                return f"Error: {result.std_err.decode()}"
        except Exception as e:
            return f"Error ejecutando comando: {e}"
    
    def interactive_shell(self):
        """Shell interactivo por WinRM"""
        if not self.connect():
            return
        
        print_success("Shell interactivo WinRM iniciado (escribe 'exit' para salir)")
        print_info(f"Comandos disponibles: whoami, ipconfig, dir, etc.")
        print("─" * 50)
        
        while True:
            try:
                cmd = input(f"\n{self.target}> ").strip()
                if cmd.lower() == 'exit':
                    break
                if not cmd:
                    continue
                
                output = self.run_command(cmd)
                print(output)
            except KeyboardInterrupt:
                print("\n[!] Saliendo...")
                break
            except Exception as e:
                print_error(f"Error: {e}")
    
    def run_script(self, script_path):
        """Ejecutar script PowerShell remoto"""
        try:
            with open(script_path, 'r') as f:
                script = f.read()
            
            result = self.session.run_ps(script)
            if result.status_code == 0:
                print_success(f"Script ejecutado exitosamente")
                return result.std_out.decode()
            else:
                print_error(f"Error ejecutando script: {result.std_err.decode()}")
                return None
        except Exception as e:
            print_error(f"Error: {e}")
            return None
