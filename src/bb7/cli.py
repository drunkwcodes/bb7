import click

from .chat import chat_terminal
from .examine import run_tests
from .write import write_code, write_test_file

MAX_RETIES = 10


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option("-c", "--chat", is_flag=True)
def main(chat):
    if chat:
        chat_terminal()
    else:
        print("bb7 is a TDD coding bot. It can recognize the Python project structure,")
        print("find the tests folder, and run tests. It can also chat with a chatbot.")

        # 1. start to write tests
        write_test_file()
        # 2. run pytest, check if all tests pass.
        result = run_tests()
        # 3. write code
        retries = 0
        while result != 0 and retries < MAX_RETIES:
            retries += 1
            print(f"Test failed. Retrying ({retries}/{MAX_RETIES})...")
            write_code()

        # loop 2.


if __name__ == "__main__":
    main()
