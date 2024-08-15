import click

from .chat import chat_terminal


@click.command(context_settings=dict(help_option_names=['-h', '--help']))
@click.option("-c","--chat", is_flag=True)
def main(chat):
    if chat:
        chat_terminal()


if __name__ == "__main__":
    main()
