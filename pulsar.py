import psutil
import time
from rich.console import Console
from rich.table import Table
from rich.live import Live
from rich.panel import Panel
from rich import box
from rich.text import Text
from rich.console import Group
from rich.align import Align

console = Console()

SKIP_DIRS = {'/proc', '/dev', '/sys', '/run', '/snap', '/tmp'}

def get_top_dirs():
    import os
    dirs = []
    for entry in os.scandir('/'):
        if entry.path in SKIP_DIRS:
            continue
        try:
            size = sum(
                f.stat().st_size
                for f in os.scandir(entry.path)
                if f.is_file()
            )
            dirs.append((entry.path, size))
        except:
            pass
    dirs.sort(key=lambda x: x[1], reverse=True)
    return dirs[:5]

def make_bar(percent):
    filled = int(percent / 5)
    empty = 20 - filled
    if percent >= 80:
        color = "red"
    elif percent >= 50:
        color = "yellow"
    else:
        color = "green"
    bar = f"[{color}]{'█' * filled}[/{color}]{'░' * empty}"
    return bar

def build_table():
    table = Table(box=box.ROUNDED, style="bold", expand=True)
    table.add_column("Disk", style="cyan")
    table.add_column("Total", style="white")
    table.add_column("Used", style="white")
    table.add_column("Free", style="white")
    table.add_column("Usage %", style="white")
    table.add_column("Bar", style="white", min_width=22)

    for p in psutil.disk_partitions():
        try:
            usage = psutil.disk_usage(p.mountpoint)
            total = f"{usage.total // (1024**3)} GB"
            used = f"{usage.used // (1024**3)} GB"
            free = f"{usage.free // (1024**3)} GB"
            percent = usage.percent

            if percent >= 80:
                pct_text = f"[red]{percent}%[/red]"
            elif percent >= 50:
                pct_text = f"[yellow]{percent}%[/yellow]"
            else:
                pct_text = f"[green]{percent}%[/green]"

            bar = make_bar(percent)
            table.add_row(p.mountpoint, total, used, free, pct_text, bar)
        except:
            pass

    return table

def build_stats():
    cpu = psutil.cpu_percent(interval=0.1)
    ram = psutil.virtual_memory()

    cpu_bar = make_bar(cpu)
    ram_bar = make_bar(ram.percent)

    stats = Table(box=box.ROUNDED, style="bold", expand=True)
    stats.add_column("Resource", style="cyan")
    stats.add_column("Usage %", style="white")
    stats.add_column("Bar", style="white", min_width=22)

    stats.add_row("CPU", f"[{'red' if cpu >= 80 else 'yellow' if cpu >= 50 else 'green'}]{cpu}%[/]", cpu_bar)
    stats.add_row("RAM", f"[{'red' if ram.percent >= 80 else 'yellow' if ram.percent >= 50 else 'green'}]{ram.percent}%[/]", ram_bar)

    return stats

def build_top_dirs():
    table = Table(box=box.ROUNDED, style="bold", expand=True)
    table.add_column("Directory", style="cyan")
    table.add_column("Size", style="yellow")

    for path, size in get_top_dirs():
        if size >= 1024**3:
            size_str = f"{size / (1024**3):.1f} GB"
        else:
            size_str = f"{size / (1024**2):.1f} MB"
        table.add_row(path, size_str)

    return table

def build_layout():
    logo = Text(justify="center")
    logo.append("██████╗ ██╗   ██╗██╗     ███████╗ █████╗ ██████╗\n", style="bold red")
    logo.append("██╔══██╗██║   ██║██║     ██╔════╝██╔══██╗██╔══██╗\n", style="bold white")
    logo.append("██████╔╝██║   ██║██║     ███████╗███████║██████╔╝\n", style="bold red")
    logo.append("██╔═══╝ ██║   ██║██║     ╚════██║██╔══██║██╔══██╗\n", style="bold white")
    logo.append("██║     ╚██████╔╝███████╗███████║██║  ██║██║  ██║\n", style="bold red")
    logo.append("╚═╝      ╚═════╝ ╚══════╝╚══════╝╚═╝  ╚═╝╚═╝  ╚═╝\n", style="bold white")

    footer = Align.center(Text("Press Ctrl+C to exit", style="dim white"))

    return Group(
        Align.center(logo),
        Panel(build_stats(), title="[bold red]System[/bold red]"),
        Panel(build_table(), title="[bold red]Disk Usage[/bold red]"),
        Panel(build_top_dirs(), title="[bold red]Top Directories[/bold red]"),
        footer,
    )

with Live(build_layout(), refresh_per_second=1, screen=True) as live:
    while True:
        live.update(build_layout())
        time.sleep(2)
