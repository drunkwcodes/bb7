import os

import ollama
import pygame
from gtts import gTTS
from rich.console import Console
from rich.prompt import Prompt
from rich.text import Text

from .utils import random_mp3_fname

# 初始化 console 對象
console = Console()


def tts(text: str, lang="zh-tw", slow=False, file_name: str | None = None):
    file_name = file_name or random_mp3_fname()
    file_path = f"/tmp/{file_name}"

    tts = gTTS(text=text, lang=lang, slow=slow)
    tts.save(file_path)

    # 初始化 pygame mixer
    pygame.mixer.init()
    # 加載 MP3 文件
    pygame.mixer.music.load(file_path)
    # 播放音頻
    pygame.mixer.music.play()
    # 等待音頻播放完畢
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    # 停止播放器
    pygame.mixer.music.stop()
    # 刪除臨時文件
    os.remove(file_path)


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
                elif "/voice" in user_input.lower() or "/v" in user_input.lower():
                    inputs = user_input.split(" ")
                    if len(inputs) > 1:
                        lang = inputs[1]
                    else:
                        lang = "ja"
                    tts(bot_reply, lang=lang)
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
    console.print("/voice [ja] - Voice output last message")
    console.print("/help - Show this help message")


if __name__ == "__main__":
    chat_terminal()
