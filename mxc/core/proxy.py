import socket
import threading
import socks
from mxc.core.color import print_success, print_error, print_info

class SocksProxy:
    def __init__(self, listen_port=1080, remote_host="127.0.0.1", remote_port=1080):
        self.listen_port = listen_port
        self.remote_host = remote_host
        self.remote_port = remote_port
        self.server = None
        self.running = False
    
    def handle_client(self, client_socket):
        """Manejar conexión de cliente"""
        try:
            # Conectar al destino remoto
            remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            remote_socket.connect((self.remote_host, self.remote_port))
            
            # Reenviar tráfico bidireccionalmente
            threads = []
            
            # Cliente -> Remoto
            t1 = threading.Thread(target=self.forward, args=(client_socket, remote_socket))
            t1.start()
            threads.append(t1)
            
            # Remoto -> Cliente
            t2 = threading.Thread(target=self.forward, args=(remote_socket, client_socket))
            t2.start()
            threads.append(t2)
            
            # Esperar a que terminen
            for t in threads:
                t.join()
                
        except Exception as e:
            print_error(f"Error manejando cliente: {e}")
        finally:
            client_socket.close()
    
    def forward(self, source, destination):
        """Reenviar datos de source a destination"""
        try:
            while True:
                data = source.recv(4096)
                if not data:
                    break
                destination.send(data)
        except:
            pass
        finally:
            source.close()
            destination.close()
    
    def start(self):
        """Iniciar servidor SOCKS proxy"""
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server.bind(('0.0.0.0', self.listen_port))
            self.server.listen(5)
            self.running = True
            
            print_success(f"SOCKS5 proxy escuchando en 0.0.0.0:{self.listen_port}")
            print_info("Configura tu herramienta para usar este proxy")
            print_info("Ejemplo: proxychains nmap -sT -Pn target")
            
            while self.running:
                client, addr = self.server.accept()
                print_info(f"Nueva conexión desde {addr[0]}:{addr[1]}")
                handler = threading.Thread(target=self.handle_client, args=(client,))
                handler.start()
                
        except Exception as e:
            print_error(f"Error iniciando proxy: {e}")
    
    def stop(self):
        """Detener proxy"""
        self.running = False
        if self.server:
            self.server.close()
        print_info("Proxy SOCKS detenido")
