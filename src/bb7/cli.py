import click

@click.command()
@click.option("--chat", is_flag=True)
def main(chat):
    pass

if __name__ == "__main__":
    main()