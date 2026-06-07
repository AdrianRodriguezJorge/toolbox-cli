import os
import sys
from abc import ABC, abstractmethod
from .i18n import get_text
from .config import load_config

# Configure console encoding for Windows
if sys.platform.startswith('win'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Try to import Rich library
try:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.prompt import Prompt, IntPrompt
    from rich.text import Text
    HAS_RICH = True
    console = Console()
except ImportError:
    HAS_RICH = False
    console = None

def clear_screen():
    """Clear console screen compatibly."""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_success(message):
    if HAS_RICH:
        console.print(f"[bold green]✔[/bold green] {message}")
    else:
        print(f"✔ {message}")

def print_error(message):
    if HAS_RICH:
        console.print(f"[bold red]✘[/bold red] {message}")
    else:
        print(f"✘ {message}")

def print_info(message):
    if HAS_RICH:
        console.print(f"[bold cyan]ℹ[/bold cyan] {message}")
    else:
        print(f"ℹ {message}")

def print_summary(success_count, fail_count):
    msg = get_text("summary_msg", success=success_count, fail=fail_count)
    if success_count > 0 and fail_count == 0:
        if HAS_RICH:
            console.print(Panel(Text(msg, style="bold green"), title=f"[bold green]{get_text('success_title')}[/bold green]", border_style="green"))
        else:
            print(f"\n=== {get_text('success_title').upper()} ===")
            print(msg)
            print("================\n")
    else:
        if HAS_RICH:
            console.print(Panel(Text(msg, style="bold yellow"), title=f"[bold yellow]{get_text('sys_diag')}[/bold yellow]", border_style="yellow"))
        else:
            print(f"\n=== {get_text('sys_diag').upper()} ===")
            print(msg)
            print("================\n")

def get_matching_files(extensions):
    """Scan and list all matching files in the current folder, ignoring temporary lockfiles."""
    cwd = "."
    files = []
    try:
        for f in os.listdir(cwd):
            if os.path.isfile(os.path.join(cwd, f)):
                # Ignore temporary/lock files from Office/OS
                if f.startswith("~$") or f.startswith("._") or f.startswith(".~lock."):
                    continue
                _, ext = os.path.splitext(f)
                if ext.lower() in extensions:
                    files.append(f)
    except Exception as e:
        print_error(f"Error scanning files: {e}")
    return sorted(files)

def get_unique_output_path(original_filename, target_extension):
    """Generate a unique file path adding incremental suffixes if a collision exists."""
    name, _ = os.path.splitext(original_filename)
    counter = 1
    new_filename = f"{name}{target_extension}"
    while os.path.exists(new_filename):
        new_filename = f"{name}_{counter}{target_extension}"
        counter += 1
    return new_filename

def select_files_to_convert(files, tool_name=""):
    """
    Shows a selective list for the user to choose to convert all files or a single one.
    Bypasses in non-interactive environment or test mode.
    """
    if not files:
        return []
    # If running in a non-interactive environment, convert all by default
    if not sys.stdin.isatty():
        return files

    clear_screen()
    print_info(get_text("found_files", count=len(files), exts=", ".join(set(os.path.splitext(f)[1] for f in files)), tool=tool_name))
    print()

    if HAS_RICH:
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column(get_text("option"), style="bold cyan", justify="center")
        table.add_column("Filename", style="bold white")
        
        table.add_row("0", f"[bold yellow]{get_text('select_all')}[/bold yellow]")
        for idx, f in enumerate(files, 1):
            table.add_row(str(idx), f)
            
        console.print(table)
        
        try:
            choice = IntPrompt.ask(get_text("select_file_prompt"), choices=[str(i) for i in range(len(files) + 1)])
        except KeyboardInterrupt:
            return []
    else:
        print("========================================")
        print(f" 0 | {get_text('select_all')}")
        for idx, f in enumerate(files, 1):
            print(f" {idx} | {f}")
        print("========================================")
        
        try:
            choice_str = input(f"{get_text('select_file_prompt')} (0-{len(files)}): ").strip()
            choice = int(choice_str) if choice_str.isdigit() else -1
        except KeyboardInterrupt:
            return []

    if choice == 0:
        print_info(get_text("converting_all"))
        return files
    elif 1 <= choice <= len(files):
        selected_file = files[choice - 1]
        print_info(f"{get_text('converting_single')}: {selected_file}")
        return [selected_file]
    else:
        return []


class BaseConverter(ABC):
    """Abstract Strategy interface for all modular converters."""

    @property
    @abstractmethod
    def id(self) -> int:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """The English name of the tool (for diagnostics and menus)."""
        pass

    @property
    @abstractmethod
    def input_extensions(self) -> list:
        """Supported input formats, e.g. ['.docx', '.doc']."""
        pass

    @property
    @abstractmethod
    def output_extension_desc(self) -> str:
        """Output extension label, e.g. 'PDF'."""
        pass

    @abstractmethod
    def convert(self, files: list) -> tuple:
        """
        Runs the converter on the selected file list.
        Returns a tuple: (success_count, fail_count).
        """
        pass
