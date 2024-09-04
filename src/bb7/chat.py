import ollama
from rich.console import Console
from rich.prompt import Prompt
from rich.text import Text

# 初始化 console 對象
console = Console()


def chat_terminal():
    """
    Runs a chat terminal where the user can interact with a simulated chatbot.

    This function uses the `console` object from the `rich.console` module to display a welcome message and prompt the user for input. It continuously reads user input and checks if it matches any of the exit commands ("/exit", "/quit", "/q"). If an exit command is entered, the function prints a message and exits the loop.

    For each user input, the function simulates a chatbot's response by calling the `litellm.completion` function from the `litellm` module. The `litellm.completion` function takes the user input as a message and sends it to the chatbot. The response from the chatbot is then printed in a formatted style using the `console.print` function.

    The function also handles keyboard interrupts by printing a message and exiting the loop.

    Parameters:
        None

    Returns:
        None
    """
    console.print("[bold green]Welcome to the bb7 Chat Terminal![/bold green]")

    history = []

    while True:
        try:
            # 使用 Prompt 讓用戶輸入訊息
            user_input = Prompt.ask("[bold blue]>>[/bold blue]")

            # 檢查是否是退出命令
            if user_input.startswith("/"):
                if user_input.lower() in ["/exit", "/quit", "/q"]:
                    console.print("[bold red]Exiting chat...[/bold red]")
                    break
                elif user_input.lower() == "/clear":
                    console.clear()
                    continue
                elif user_input.lower() == "/help":
                    show_help()
                    continue
                else:
                    console.print("[bold red]Invalid command[/bold red]")
                    continue

            history.append({"role": "user", "content": user_input})

            # 聊天機器人的回覆
            try:
                response = ollama.chat(
                    model="llama3.1",
                    messages=history,
                )
                bot_reply = response["message"]["content"]
                history.append({"role": "assistant", "content": bot_reply})
                console.print(Text(bot_reply, style="bold yellow"))
            except Exception as e:
                console.print(f"[bold red]Error: {str(e)}[/bold red]")

        except KeyboardInterrupt:
            console.print("[bold red]Keyboard interrupt[/bold red]")
        except EOFError:
            console.print("[bold red]Exiting chat...[/bold red]")
            break


# 執行聊天終端


def show_help():
    console.print("[bold green]Available commands:[/bold green]")
    console.print("/exit, /quit, /q - Exit the chat")
    console.print("/clear - Clear the screen")
    console.print("/help - Show this help message")


if __name__ == "__main__":
    chat_terminal()
