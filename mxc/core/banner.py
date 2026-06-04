from mxc.core.color import Colors

def show_banner():
    banner = f"""
{Colors.CYAN}    .----------------.     {Colors.WHITE}_   _          _     _____{Colors.CYAN}
   | .--------------. |   {Colors.WHITE}| \\ | |   ___  | |_  | ____| __  __   ___    ___{Colors.CYAN}
   | |   .------.   | |   {Colors.WHITE}|  \\| |  / _ \\ | __| |  _|   \\ \\/ /  / _ \\  / __|{Colors.CYAN}
   | |  |  ()() |   | |   {Colors.WHITE}| |\\  | |  __/ | |_  | |___   >  <  |  __/ | (__{Colors.CYAN}
   | |  |  (__) |   | |   {Colors.WHITE}|_| \\_|  \\___|  \\__| |_____| /_/\\_\\ \\___|  \\___|{Colors.CYAN}
   | |  '------'   | |
   | '--------------' |
   '----------------'
{Colors.GREEN}          .--.
         /    \\
         |oo  |
         |_<  |
         \\____/
          '  '{Colors.RESET}

{Colors.BOLD}{Colors.MAGENTA}    🐢 Mxtexec (mxc) - v0.1 - Caparazón letal 🐢{Colors.RESET}
{Colors.YELLOW}    >>> Rápido, sigiloso y con todo el poder de una tortuga ninja <<<{Colors.RESET}
"""
    print(banner)
