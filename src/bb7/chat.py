import os
from datetime import datetime

import ollama
import pygame
import tomlkit
from gtts import gTTS
from platformdirs import user_data_dir
from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.history import FileHistory
from prompt_toolkit.shortcuts import radiolist_dialog, yes_no_dialog
from rich.console import Console
from rich.prompt import Prompt
from rich.text import Text
from tomlkit import document, parse

from .rag import (
    Collection,
    ask,
    create_index,
    init_db,
    load_markdown_documents,
    update_index,
)
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


def set_lang(conf_file: str, lang: str):
    with open(conf_file, "r") as f:
        doc = parse(f.read())

    doc["voice_language"] = lang

    with open(conf_file, "w") as f:
        f.write(tomlkit.dumps(doc))


def get_lang(conf_file: str):
    with open(conf_file, "r") as f:
        doc = parse(f.read())

    return doc["voice_language"]


def select_language(conf_file: str):
    # 定義語言選項
    languages = [
        ("中文 (Chinese)", "Chinese"),
        ("英文 (English)", "English"),
        ("日文 (Japanese)", "Japanese"),
        ("韓文 (Korean)", "Korean"),
        ("法文 (French)", "French"),
        ("西班牙文 (Spanish)", "Spanish"),
        ("其他 (Other)", "Other"),
    ]

    # 使用 radiolist_dialog 顯示選單
    result = radiolist_dialog(
        title="語言選單",
        text="Please select a language for /voice command:",
        values=languages,
    ).run()

    # 如果選擇「其他」，讓使用者輸入自訂語言名稱
    if result == "其他 (Other)":
        session = PromptSession()
        custom_language = session.prompt("請輸入自訂語言名稱：")
        print(f"You selected: {custom_language}")
        set_lang(conf_file=conf_file, lang=custom_language)

    else:
        print(f"You selected: {result}")
        if result == "中文 (Chinese)":
            set_lang(conf_file=conf_file, lang="zh-tw")

        elif result == "英文 (English)":
            set_lang(conf_file=conf_file, lang="en")

        elif result == "日文 (Japanese)":
            set_lang(conf_file=conf_file, lang="ja")

        elif result == "韓文 (Korean)":
            set_lang(conf_file=conf_file, lang="ko")

        elif result == "法文 (French)":
            set_lang(conf_file=conf_file, lang="fr")

        elif result == "西班牙文 (Spanish)":
            set_lang(conf_file=conf_file, lang="es")

        elif result is None:
            print("You canceled the selection.")
            print("Current language:", get_lang(conf_file=conf_file))

        else:
            raise ValueError(f"Invalid language selection: {result}")


def load_document():  
    """
    Load documents from a given path into the database, and create an index
    for the collection. If the collection already exists, update the index
    instead.

    Prompts the user to input the document path and collection name.

    Returns the collection name.
    """
    session = PromptSession()
    doc_path = session.prompt("Enter the document path：")
    doc_collection_name = session.prompt("Enter the collection name：")

    collection = Collection.get_or_none(Collection.name == doc_collection_name)
    if collection is None:
        collection = Collection(name=doc_collection_name, path=doc_path)
        collection.save()
        create_index(
            collection_name=doc_collection_name,
            documents=load_markdown_documents(doc_path),
        )
    else:
        collection.path = doc_path
        collection.updated = datetime.now()
        collection.save()
        update_index(
            collection_name=doc_collection_name,
            documents=load_markdown_documents(doc_path),
        )

    return doc_collection_name


def choose_collection():
    collections = Collection.select(Collection.name).order_by(Collection.updated.desc())

    choices = [(collection.name, collection.name) for collection in collections]
    if len(choices) == 0:
        print("No collections found.")
        return

    result = radiolist_dialog(
        title="Select a Collection", text="Please choose a collection:", values=choices
    ).run()
    print(f"You activated: {result}")
    return result


def normal_chat(chat_history):
    try:
        response = ollama.chat(
            # model="llama3.1",
            # model="llama3.2:1b",
            model="llama3.2",
            messages=chat_history,
        )
        bot_reply = response["message"]["content"]
    except Exception as e:
        console.print(f"[bold red]Error: {str(e)}[/bold red]")

    return bot_reply


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
    bb7_dir = user_data_dir(appname="bb7", appauthor="drunkwcodes")
    history_file = bb7_dir + "/chat_history.txt"

    conf_file = bb7_dir + "/bb7_config.toml"
    os.makedirs(bb7_dir, exist_ok=True)
    # Write default config file if it doesn't exist
    if os.path.exists(conf_file) is False:
        doc = document()
        doc.add("voice_language", "ja")
        with open(conf_file, "w") as f:
            tomlkit.dump(doc, f)

    session = PromptSession(history=FileHistory(history_file))
    activated = ""
    while True:
        try:
            # 使用 Prompt 讓用戶輸入訊息
            # user_input = Prompt.ask("[bold blue]>>[/bold blue]")
            lang = get_lang(conf_file)
            user_input = session.prompt(
                activated + ">> ", auto_suggest=AutoSuggestFromHistory()
            )

            # 檢查是否使用命令
            if user_input.startswith("/"):
                if user_input.lower() in ["/exit", "/quit", "/q"]:
                    console.print("[bold red]Exiting chat...[/bold red]")
                    break
                elif "/activate" in user_input.lower() or "/a" in user_input.lower():
                    doc_name = choose_collection()
                    if doc_name is not None:
                        activated = f"({doc_name})"
                    continue

                elif "/deactivate" in user_input.lower() or "/d" in user_input.lower():
                    activated = ""
                    continue

                elif "/load" in user_input.lower() or "/l" in user_input.lower():
                    doc_name = load_document()
                    # 創建 y/n 提示框
                    want_to_activate = yes_no_dialog(
                        title="Confirmation",
                        text="Do you want to activate the document?",
                    ).run()
                    if want_to_activate:
                        activated = f"({doc_name})"
                    continue

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
                    tts(bot_reply, lang=lang)
                    continue

                elif "/select" in user_input.lower() or "/s" in user_input.lower():
                    select_language(conf_file=conf_file)
                    continue
                else:
                    console.print("[bold red]Invalid command[/bold red]")
                    continue

            # start to chat
            history.append({"role": "user", "content": user_input})

            # 聊天機器人的回覆
            if activated != "":  # if activated documents
                bot_reply = ask(user_input, collection_name=doc_name)
            else:
                bot_reply = normal_chat(history)

            history.append({"role": "assistant", "content": bot_reply})
            console.print(Text(bot_reply, style="bold yellow"))
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
