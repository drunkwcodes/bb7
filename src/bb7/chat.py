import ollama
from rich.console import Console
from rich.prompt import Prompt
from rich.text import Text

from bark import SAMPLE_RATE, generate_audio, preload_models
from scipy.io.wavfile import write as write_wav
import random
from pydub import AudioSegment
from pydub.playback import play
import os

# 初始化 console 對象
console = Console()



def rand_str():
    return "".join(
        [
            chr(ord("a") + random.randint(0, 25)),
            chr(ord("a") + random.randint(0, 25)),
            chr(ord("a") + random.randint(0, 25)),
            chr(ord("a") + random.randint(0, 25)),
            chr(ord("a") + random.randint(0, 25)),
            chr(ord("a") + random.randint(0, 25)),
            chr(ord("a") + random.randint(0, 25)),
            chr(ord("a") + random.randint(0, 25)),
        ]
    )

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
    console.print("[bold green]Welcome to the Chat Terminal![/bold green]")

    try:
        bot_reply = ""
        while True:
            # 使用 Prompt 讓用戶輸入訊息
            user_input = Prompt.ask("[bold blue]>>[/bold blue]")

            # 檢查是否是退出命令
            if user_input.lower() in ["/exit", "/quit", "/q"]:
                console.print("[bold red]Exiting chat...[/bold red]")
                break

            elif user_input.lower() in ["/help", "/h", "/?"]:
                console.print("[bold yellow]Available commands: [/bold yellow]")
                console.print("/help, /h, /?")
                console.print("/exit, /quit, /q")
                console.print("/vocal")
                
            elif user_input.lower() in ["/vocal"]:

                # download and load all bark models
                preload_models(text_use_gpu=False, coarse_use_gpu=False, fine_use_gpu=False, codec_use_gpu=False)

                audio_array = generate_audio(bot_reply)
                afilename = rand_str() + ".wav"

                os.removedirs("/tmp/bb7")
                os.makedirs("/tmp/bb7/", exist_ok=True)


                afpath = f"/tmp/bb7/{afilename}"
                write_wav(afpath, SAMPLE_RATE, audio_array)
                speech = AudioSegment.from_wav(afpath)
                play(speech)

            else:
                # 聊天機器人的回覆
                response = ollama.chat(
                    model="llama3.1",
                    messages=[
                        {
                            "role": "user",
                            "content": user_input,
                        },
                    ],
                )

                # bot_reply = f"ChatBot: You said '{user_input}'"
                bot_reply = response["message"]["content"]
                console.print(Text(bot_reply, style="bold yellow"))
    except KeyboardInterrupt:
        console.print()
        console.print("[bold red]Exiting chat...[/bold red]")


# 執行聊天終端


if __name__ == "__main__":

    # response = litellm.completion(
    #     model="ollama/llama3.1",
    #     messages=[{ "content": "respond in 20 words. who are you?","role": "user"}],
    #     api_base="http://localhost:11434"
    # )
    # print(response)
    # response.choices[0].message.content

    chat_terminal()
