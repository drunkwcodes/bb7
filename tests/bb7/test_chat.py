from unittest.mock import patch

from bb7.chat import show_help, chat_terminal

from io import StringIO


def test_chat_terminal():
    # 模擬用戶輸入
    user_input = StringIO("/exit\n")
    
    # 捕獲標準輸出
    captured_output = StringIO()
    
    # 使用 patch 來模擬 input 函數、sys.stdout 和其他必要的函數
    with patch('builtins.input', return_value="/exit"), \
         patch('sys.stdout', new=captured_output):
        
        
        # 調用 chat_terminal 函數
        chat_terminal()
    
    # 獲取捕獲的輸出
    output = captured_output.getvalue()
    
    # 驗證輸出中包含預期的內容
    assert "Welcome to the bb7 Chat Terminal!" in output
    assert "Exiting chat..." in output


def test_tts():
    pass


def test_show_help():
    with patch("bb7.chat.console.print") as mock_print:
        show_help()

        # 驗證 console.print 被調用的次數
        assert mock_print.call_count == 10

        # 驗證每次調用的參數
        mock_print.assert_any_call("[bold green]Available commands:[/bold green]")
        mock_print.assert_any_call("/exit, /quit, /q - Exit the chat")
        mock_print.assert_any_call("/clear - Clear the screen")
        mock_print.assert_any_call("/voice [ja] - Voice output last message")
        mock_print.assert_any_call("/select - Select voice language")
        mock_print.assert_any_call("/activate - Activate a document")
        mock_print.assert_any_call("/deactivate - Deactivate a document")
        mock_print.assert_any_call("/load - Load a document")
        mock_print.assert_any_call("/model [llama3.2] - Select model")
        mock_print.assert_any_call("/help - Show this help message")
