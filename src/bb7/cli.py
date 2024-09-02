import click

from .chat import chat_terminal
from .examine import examine_folders, run_tests
from .utils import cd, find_project_root
from .write import write_all_tests, write_code, write_test_file

MAX_RETRIES = 10


@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option("-c", "--chat", is_flag=True)
def main(chat):
    if chat:
        chat_terminal()
    else:
        print("bb7 is a TDD coding bot. It can recognize the Python project structure,")
        print("find the tests folder, and run tests. It can also chat with a chatbot.")

        proot = None
        if examine_folders() is False:
            proot = find_project_root()
        else:
            proot = "."

        if proot is None:
            print("The current directory is not in a Python project.")
            return

        with cd(proot):
            # 1. start to write tests
            write_test_file()
            write_all_tests()
            # 2. run pytest, check if all tests pass.
            result = run_tests()
            # 3. write code
            retries = 0
            while result != 0 and retries < MAX_RETRIES:
                retries += 1
                print(f"Test failed. Retrying ({retries}/{MAX_RETRIES})...")
                write_code()
                result = run_tests()

            # loop 2.


if __name__ == "__main__":
    main()
