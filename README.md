# Mxtexec (mxc)

![Banner](https://raw.githubusercontent.com/Falconmx1/Mxtexec/main/docs/banner.png)

**Mxtexec (mxc)** - Herramienta de ejecución en red para explotación y post-explotación. Automatiza la evaluación de seguridad en grandes redes. Como NetExec pero con caparazón de tortuga. Rápido, sigiloso y letal. 🐢⚡

## Instalación

```bash
git clone https://github.com/Falconmx1/Mxtexec.git
cd Mxtexec
pip install -e .

Uso básico
# Enumerar shares SMB
mxc smb 192.168.1.10 -u admin -p Pass123 --shares

# Próximamente: ejecutar comandos por WinRM
# mxc winrm 192.168.1.10 -u admin -p Pass123 --command "whoami"

