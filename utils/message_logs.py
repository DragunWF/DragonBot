import random
from rich.console import Console

console = Console()

# Dragon's Castle: 440134996984856577
# Winter Company: 404814305872183296
# Dragon's Laboratory: 414052037580554251

servers = {440134996984856577: "chat_logs_1.txt", 404814305872183296: "chat_logs_2.txt",
           414052037580554251: "chat_logs_3.txt"}
ids = tuple([x for x in servers])

# Global variables for message sniping
last_deleted_msg, deleted_msg_author = "", ""
last_edited_msg, edited_msg_author = "", ""
no_snipe_responses = ("There isn't anything to snipe!",
                      "Sorry, but there's nothing to snipe.",
                      "No message to snipe unfortunately.")


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


def deleted_message_log(author, content, channel, guild):
    log = f"""Message Delete Event:
Guild: {guild}
Channel: #{channel}
{author}: {content}
"""
    console.log(f"""[red][bold]Message Delete Event:[/bold][/red]
[blue][bold]Guild: {guild}[/bold][/blue]
[yellow][bold]Channel: [underline]#{channel}[/underline][/bold][/yellow]
{author}: {content}
""")
    with open("data/deleted_msgs.txt", "a") as file:
        file.write(log)


def message_snipe():
    if last_deleted_msg:
        return f">>> `Deleted Message:\n{deleted_msg_author}: {last_deleted_msg}`"
    else:
        return random.choice(no_snipe_responses)


def edited_message_snipe():
    if last_edited_msg:
        return f">>> `Edited Message:\n{edited_msg_author}: {last_edited_msg}`"
    else:
        return random.choice(no_snipe_responses)
