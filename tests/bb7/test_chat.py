from unittest.mock import patch

from bb7.chat import show_help


def test_chat_terminal():
    pass


def test_tts():
    pass


def test_show_help():
    with patch("bb7.chat.console.print") as mock_print:
        show_help()

        # 驗證 console.print 被調用的次數
        assert mock_print.call_count == 5

        # 驗證每次調用的參數
        mock_print.assert_any_call("[bold green]Available commands:[/bold green]")
        mock_print.assert_any_call("/exit, /quit, /q - Exit the chat")
        mock_print.assert_any_call("/clear - Clear the screen")
        mock_print.assert_any_call("/voice - Voice output last message")
        mock_print.assert_any_call("/help - Show this help message")
