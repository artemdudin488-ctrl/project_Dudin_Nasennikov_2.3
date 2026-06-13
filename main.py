import sys
import os
import tkinter as tk
from game_engine import GameEngine
from persistence import load_game, save_game
from gui_ui import AnimalGameGUI

def main():
    """
    главная функция: загружает сохранённое дерево, создаёт движок и запускает gui
    """
    save_file = "savegame.json"                   # имя файла сохранения
    tree = load_game(save_file)                   # загружает только дерево
    engine = GameEngine(tree)              # создаёт движок с загруженным деревом

    root = tk.Tk()                                # создаёт корневое окно
    app = AnimalGameGUI(root, engine, save_file)  # создаёт gui
    root.mainloop()                               # запускает цикл обработки событий

if __name__ == "__main__":
    main()                                        # запускает главную функцию