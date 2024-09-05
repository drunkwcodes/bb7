from click.testing import CliRunner

from bb7.cli import main


def test_main():
    pass
    # runner = CliRunner()
    # result = runner.invoke(main)
    # assert result.exit_code == 0
    # assert "bb7 is a TDD coding bot" in result.output

    # # 測試 chat 選項
    # result = runner.invoke(main, ['-c'])
    # assert result.exit_code == 0
    # assert "Welcome to the bb7 Chat Terminal!" in result.output
