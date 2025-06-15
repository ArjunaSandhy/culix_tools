import sys
import time
import os
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.panel import Panel
from rich.text import Text
from pyfiglet import Figlet
from colorama import Fore, Style, init

# Initialize colorama
init()
console = Console(color_system="truecolor")
THEME_COLOR = "rgb(0,255,70)"  # Bright green for visibility

class Display:
    _last_progress = ""

    @staticmethod
    def print_banner():
        """Display application banner"""
        console.clear()
        
        # Create banner
        f = Figlet(font='bulbhead')
        banner = f.renderText('CULIX-TOOLS')
        
        # Get terminal width with fallback
        try:
            terminal_width = os.get_terminal_size().columns
        except OSError:
            terminal_width = 80  # Default fallback width
        
        # Split banner into lines and center each line
        banner_lines = banner.split('\n')
        centered_banner = '\n'.join(line.center(terminal_width) for line in banner_lines if line.strip())
        console.print(f"[{THEME_COLOR}]{centered_banner}[/]")
        
        # Application description
        console.print(f"[{THEME_COLOR}][ TELEGRAM MEMBER SCRAPER & ADDER ][/]", justify="center")
        console.print(f"[{THEME_COLOR}]╚══[ AUTHOR - ARXADEV ]══╝[/]", justify="center")
        print("\n")

    @staticmethod
    def create_progress():
        """Create a progress bar"""
        return Progress(
            TextColumn(f"[{THEME_COLOR}]{{task.description}}"),
            BarColumn(complete_style=THEME_COLOR),
            TextColumn(f"[{THEME_COLOR}]{{task.percentage:>3.0f}}%"),
            console=console,
            expand=True
        )

    @staticmethod
    def create_spinner(text):
        """Create a loading spinner"""
        return Progress(
            SpinnerColumn("line", style=THEME_COLOR),
            TextColumn(f"[{THEME_COLOR}]{text}"),
            transient=True
        )

    @staticmethod
    def print_success(message):
        """Print success message"""
        Display.clear_line()
        console.print(f"[{THEME_COLOR}]→ {message}[/]")

    @staticmethod
    def print_error(message):
        """Print error message"""
        Display.clear_line()
        console.print(f"[red]→ {message}[/]")

    @staticmethod
    def print_info(message):
        """Print info message"""
        Display.clear_line()
        console.print(f"[{THEME_COLOR}]→ {message}[/]")

    @staticmethod
    def print_warning(message):
        """Print warning message"""
        Display.clear_line()
        console.print(f"[yellow]→ {message}[/]")

    @staticmethod
    def print_stats(title, stats):
        """Print statistics"""
        Display.clear_line()
        console.print(f"\n[{THEME_COLOR}]┌──[ {title} ]")
        console.print(f"[{THEME_COLOR}]├" + "─" * 48)
        for key, value in stats.items():
            console.print(f"[{THEME_COLOR}]├──→ {key}:[/] {value}")
        console.print(f"[{THEME_COLOR}]└" + "─" * 48)
        print()

    @staticmethod
    def print_progress(current, total, message):
        """Print progress information"""
        Display.clear_line()
        percentage = (current / total * 100) if total > 0 else 0
        progress = f"→ {message} → {current}/{total} → {percentage:.1f}%"
        console.print(f"[{THEME_COLOR}]{progress}[/]")

    @staticmethod
    def clear_line():
        """Clear current line and move cursor to start"""
        if Display._last_progress:
            sys.stdout.write('\r' + ' ' * len(Display._last_progress) + '\r')
            sys.stdout.flush()
            Display._last_progress = "" 