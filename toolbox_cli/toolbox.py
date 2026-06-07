import os
import sys

# Ensure parent directory is in path to import package
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from toolbox_cli import (
    clear_screen,
    print_error,
    print_info,
    print_summary,
    check_system_dependencies,
    get_converter_by_id,
    CONVERTERS,
    get_text,
    get_matching_files,
    HAS_RICH
)

# Conditionally import rich components if available
if HAS_RICH:
    from rich.console import Console
    from rich.panel import Panel
    from rich.table import Table
    from rich.prompt import IntPrompt
    from rich.text import Text
    console = Console()

def main():
    while True:
        clear_screen()
        
        # Real-time scan of files to show counts dynamically in the menu
        counts = {}
        for c in CONVERTERS:
            counts[c.id] = len(get_matching_files(c.input_extensions))

        # Run system diagnostics
        ffmpeg_ok, office_ok, python_deps = check_system_dependencies()

        if HAS_RICH:
            # Main Banner
            console.print(Panel(
                Text(get_text("menu_title"), style="bold white", justify="center"),
                style="bold blue",
                subtitle=f"{get_text('menu_subtitle')}: {os.getcwd()}"
            ))
            
            # Diagnostics Panel
            diag_parts = []
            diag_parts.append(f"[bold green]{get_text('diag_ffmpeg')}[/bold green]: {get_text('diag_ok')}" if ffmpeg_ok else f"[bold red]{get_text('diag_ffmpeg')}[/bold red]: {get_text('diag_missing')}")
            
            if sys.platform.startswith('win'):
                diag_parts.append(f"[bold green]{get_text('diag_office')}[/bold green]: {get_text('diag_ok')}" if office_ok else f"[bold red]{get_text('diag_office')}[/bold red]: {get_text('diag_missing')}")
            else:
                diag_parts.append(f"[bold green]{get_text('diag_libre')}[/bold green]: {get_text('diag_ok')}" if office_ok else f"[bold red]{get_text('diag_libre')}[/bold red]: {get_text('diag_missing')}")
                
            missing_python = [name for name, ok in python_deps.items() if not ok]
            if not missing_python:
                diag_parts.append(f"[bold green]{get_text('diag_python')}[/bold green]: {get_text('diag_ok')}")
            else:
                diag_parts.append(f"[bold yellow]{get_text('diag_missing_libs')}[/bold yellow]: {', '.join(missing_python)}")
                
            console.print(Panel(" | ".join(diag_parts), title=f"[bold yellow]{get_text('sys_diag')}[/bold yellow]", border_style="dim yellow"))
            
            # Interactive Options Table
            table = Table(show_header=True, header_style="bold magenta", expand=True)
            table.add_column(get_text("option"), style="bold cyan", width=8, justify="center")
            table.add_column(get_text("tool_name"), style="bold white")
            table.add_column(get_text("input_format"), style="bold yellow")
            table.add_column(get_text("output_format"), style="bold green")
            table.add_column(get_text("files_detected"), style="bold magenta", justify="center")
            
            # Map tools to rows
            for c in CONVERTERS:
                # Add highlighting to compression utilities
                name_display = c.name
                if c.id == 10:
                    name_display = f"[bold yellow]{c.name}[/bold yellow]"
                elif c.id == 11:
                    name_display = f"[bold green]{c.name}[/bold green]"
                    
                table.add_row(
                    str(c.id),
                    name_display,
                    ", ".join(ext.upper().replace(".", "") for ext in c.input_extensions),
                    c.output_extension_desc,
                    str(counts[c.id])
                )
                
            table.add_row("0", f"[bold red]{get_text('exit_opt')}[/bold red]", "-", "-", "-")
            
            console.print(table)
            
            try:
                choice = IntPrompt.ask(get_text("select_menu_prompt"), choices=[str(i) for i in range(len(CONVERTERS) + 1)])
            except KeyboardInterrupt:
                choice = 0
        else:
            # Fallback plain text UI
            print("==========================================================================")
            print(f"  {get_text('menu_title')}")
            print(f"  {get_text('menu_subtitle')}: {os.getcwd()}")
            print("==========================================================================")
            diag_str = f"FFmpeg: {get_text('diag_ok') if ffmpeg_ok else get_text('diag_missing')} | Office/Word COM: {get_text('diag_ok') if office_ok else get_text('diag_missing')}"
            missing_python = [name for name, ok in python_deps.items() if not ok]
            if missing_python:
                diag_str += f" | {get_text('diag_missing_libs')}: {', '.join(missing_python)}"
            else:
                diag_str += f" | Python: {get_text('diag_ok')}"
            print(f" [{get_text('sys_diag')}]: {diag_str}")
            print("==========================================================================")
            
            for c in CONVERTERS:
                print(f" [{c.id}] {c.name:<30} | Input: {', '.join(c.input_extensions).upper():<15} -> {c.output_extension_desc:<20} ({counts[c.id]} files)")
            print(f" [0] {get_text('exit_opt')}")
            print("==========================================================================")
            
            try:
                choice_str = input(f"{get_text('select_menu_prompt')} (0-{len(CONVERTERS)}): ").strip()
                choice = int(choice_str) if choice_str.isdigit() else -1
            except KeyboardInterrupt:
                choice = 0
                
        if choice == 0:
            exit_msg = "\nGoodbye! Exiting toolbox..." if get_text("exit_opt") == "Exit" else "\n¡Hasta luego! Saliendo de la caja de herramientas..."
            print(exit_msg + "\n")
            break
            
        converter = get_converter_by_id(choice)
        if converter:
            files = get_matching_files(converter.input_extensions)
            if not files:
                print_error(get_text("err_no_files"))
            else:
                success, fail = converter.convert(files)
                if success > 0 or fail > 0:
                    print_summary(success, fail)
        else:
            print_error(get_text("invalid_opt"))
            
        # Wait for enter key to clear menu and return
        try:
            if HAS_RICH:
                from rich.prompt import Prompt
                Prompt.ask(f"\n{get_text('press_enter')}")
            else:
                input(f"\n{get_text('press_enter')}")
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    main()
