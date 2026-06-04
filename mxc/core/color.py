class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    MAGENTA = '\033[95m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_success(msg): print(f"{Colors.GREEN}[+]{Colors.RESET} {msg}")
def print_error(msg): print(f"{Colors.RED}[-]{Colors.RESET} {msg}")
def print_info(msg): print(f"{Colors.BLUE}[*]{Colors.RESET} {msg}")
def print_warning(msg): print(f"{Colors.YELLOW}[!]{Colors.RESET} {msg}")
