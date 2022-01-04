import time
from rich.console import Console

console = Console()

# Dragon's Castle: 440134996984856577
# Winter Company: 404814305872183296
# Dragon's Laboratory: 414052037580554251

servers = {440134996984856577: "chat_logs_1.txt", 404814305872183296: "chat_logs_2.txt",
           414052037580554251: "chat_logs_3.txt"}
ids = (440134996984856577, 414052037580554251, 404814305872183296)


def message_log(author, content, channel, guild, different_channel):
    log = ""

    if different_channel:
        console.log(
            f"[underline][bold][yellow]{channel}:[/yellow][/bold][/underline]")
        log += f"#{channel}\n"
    console.log(f"[bold][green]{author}:[/green][/bold] {content}")
    log += f"{author}: {content}\n"

    server_log_file = servers[guild] if guild in ids else "chat_logs_4.txt"
    with open(f"data/{server_log_file}", "a") as file:
        file.write(log)


def message_edit_log(author, after, before, channel, guild, different_channel):
    log = ""

    if different_channel:
        console.log(
            f"[underline][bold][yellow]{channel}:[/yellow][/bold][/underline]")
        log += f"#{channel}\n"

    console.log(f"""[bold][green]{author}[/green][red] (Edit Event)[/red]:[/bold]
[cyan]Orginal Message:[/cyan] {before}
[red]Edited Message:[/red] {after}""")
    log += f"""{author}: (Edit Event)
Original Message: {before}
Edited Message: {after}
"""

    server_log_file = servers[guild] if guild in ids else "chat_logs_4.txt"
    with open(f"data/{server_log_file}", "a") as file:
        file.write(log)
