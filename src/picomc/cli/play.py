import click
import asyncio
import getpass

from picomc.cli.utils import coro, pass_account_manager, pass_instance_manager, pass_launcher
from picomc.logging import logger
from picomc.errors import AccountError
from picomc.account import OnlineAccount, OfflineAccount

@click.command()
@click.argument("version", required=False)
@click.option("-a", "--account", "account_name")
@click.option("--verify", is_flag=True, default=False)
@click.option("--java", default=None, help="Custom Java directory")
@pass_instance_manager
@pass_account_manager
@pass_launcher
@coro
async def play(launcher, am, im, version, account_name, verify, java):
    """Play Minecraft without having to deal with stuff"""

    if account_name:
        account = am.get(account_name)
    else:
        try:
            account = am.get_default()
        except AccountError:
            username = input("Choose your account name:\n> ")
            email = input(
                "\nIf you have a Mojang account with a Minecraft license,\n"
                "enter your email. Leave blank if you want to play offline:\n> "
            )
            if email:
                account = OnlineAccount.new(am, username, email)
            else:
                account = OfflineAccount.new(am, username)
            am.add(account)
            if email:
                password = getpass.getpass("\nPassword:\n> ")
                await account.authenticate(password)
    
    if not im.exists("default"):
        im.create("default", "latest")
    
    inst = im.get("default")
    await inst.launch(account, version, verify_hashes=verify, custom_java=java)

def register_play_cli(picomc_cli):
    picomc_cli.add_command(play)