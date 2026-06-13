import tkinter as tk
from tkinter import ttk, messagebox
from game_engine import GameEngine
from persistence import save_game


class AnimalGameGUI:
    """главный класс gui, управляет отображением экранов и взаимодействием с движком"""

    def __init__(self, root: tk.Tk, engine: GameEngine, save_file: str):
        """конструктор gui"""
        self.root = root
        self.engine = engine
        self.save_file = save_file

        # настройка главного окна
        self.root.title("Максим и Артем: Угадай домашнее животное")
        self.root.geometry("600x550")
        self.root.configure(bg="#F4F6F7")
        self.root.resizable(False, False)

        # перехват закрытия окна для автосохранения
        self.root.protocol("WM_DELETE_WINDOW", self._on_closing)

        # стилизация компонентов (ttk)
        self.style = ttk.Style()
        self.style.theme_use("clam")

        styles = [
            ("TLabel", {"font": ("Helvetica", 12), "background": "#F4F6F7", "foreground": "#2C3E50"}),
            ("Header.TLabel", {"font": ("Helvetica", 16, "bold"), "background": "#F4F6F7", "foreground": "#2C3E50"}),
            ("Question.TLabel", {"font": ("Helvetica", 14, "bold"), "background": "#FFFFFF", "foreground": "#34495E"}),
            ("Fact.TLabel", {"font": ("Helvetica", 11, "italic"), "background": "#EAECEE", "foreground": "#5D6D7E"}),
            ("TButton", {"font": ("Helvetica", 11), "padding": 8, "background": "#3498DB", "foreground": "white"}),
            ("Action.TButton", {"font": ("Helvetica", 11, "bold"), "background": "#2ECC71", "foreground": "white"}),
            ("TRadiobutton", {"font": ("Helvetica", 11), "background": "#F4F6F7"}),
        ]
        for style_name, params in styles:
            self.style.configure(style_name, **params)

        self.style.map("TButton", background=[("active", "#2980B9")])
        self.style.map("Action.TButton", background=[("active", "#27AE60")])

        # главный контейнер (рамка, которая будет перерисовываться)
        self.main_frame = tk.Frame(self.root, bg="#F4F6F7")
        self.main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # запуск главного меню
        self._show_welcome_screen()

    # вспомогательные методы
    def _clear_frame(self):
        """удаляет все виджеты из main_frame (очищает экран)"""
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def _create_answer_buttons(self, on_yes_callback, on_no_callback):
        """создаёт пару кнопок да и нет с заданными обработчиками"""
        btn_frame = tk.Frame(self.main_frame, bg="#F4F6F7")
        btn_frame.pack(pady=20)
        ttk.Button(btn_frame, text="Да", width=12, command=on_yes_callback).grid(row=0, column=0, padx=20)
        ttk.Button(btn_frame, text="Нет", width=12, command=on_no_callback).grid(row=0, column=1, padx=20)

    def _add_input_field(self, parent, label_text, entry_font=("Helvetica", 11), pady=(2, 12)):
        """добавляет подпись и поле ввода, возвращает поле"""
        ttk.Label(parent, text=label_text).pack(anchor="w")
        entry = ttk.Entry(parent, font=entry_font)
        entry.pack(fill="x", pady=pady)
        return entry

    # --- экраны ---
    def _show_welcome_screen(self):
        """отображает главное меню (приветствие, кнопки "начать" и "выход")"""
        self._clear_frame()
        ttk.Label(self.main_frame, text="М А К С И М   И   А Р Т Е М", style="Header.TLabel", justify="center").pack(
            pady=(40, 20))
        ttk.Label(self.main_frame,
                  text="Загадай домашнее животное, а мы попробуем его отгадать.\nОтвечай на вопросы честно!",
                  justify="center").pack(pady=10)

        ttk.Button(self.main_frame, text="Начать игру", style="Action.TButton", width=25,
                   command=self._start_game).pack(pady=10)
        ttk.Button(self.main_frame, text="Выход", width=25, command=self._on_closing).pack(pady=10)

    def _start_game(self):
        """запускает новую игру"""
        self.engine.start()
        self._refresh_game_state()

    def _refresh_game_state(self):
        """обновляет интерфейс в зависимости от состояния движка"""
        self._clear_frame()
        question = self.engine.get_question()
        if question:
            self._draw_question_screen(question)
        else:
            guess = self.engine.get_guess()
            if guess:
                self._draw_guess_screen(guess[0], guess[1])

    def _draw_question_screen(self, question_text: str):
        """рисует экран с вопросом"""
        ttk.Label(self.main_frame, text="Вопрос:", style="Header.TLabel").pack(pady=(20, 10))

        card = tk.Frame(self.main_frame, bg="#FFFFFF", highlightbackground="#BDC3C7", highlightthickness=1, bd=0)
        card.pack(fill="x", ipady=20, pady=10)
        ttk.Label(card, text=question_text, style="Question.TLabel", wraplength=500, justify="center").pack(expand=True,
                                                                                                            padx=20,
                                                                                                            pady=20)

        self._create_answer_buttons(lambda: self._handle_answer("yes"), lambda: self._handle_answer("no"))
        ttk.Button(self.main_frame, text="Вернуться назад", width=42, command=self._handle_back).pack(pady=20)

    def _draw_guess_screen(self, animal: str, fact: str):
        """рисует экран с предположением бота"""
        ttk.Label(self.main_frame, text="Наше предположение...", style="Header.TLabel").pack(pady=(20, 10))
        ttk.Label(self.main_frame, text=animal.upper(), font=("Helvetica", 22, "bold"), foreground="#27AE60").pack(
            pady=10)

        if fact:
            fact_frame = tk.Frame(self.main_frame, bg="#EAECEE", bd=0)
            fact_frame.pack(fill="x", ipady=10, pady=10)
            ttk.Label(fact_frame, text=f"Факт: {fact}", style="Fact.TLabel", wraplength=500, justify="center").pack(
                expand=True, padx=15, pady=10)

        ttk.Label(self.main_frame, text="Мы угадали?", font=("Helvetica", 12, "bold")).pack(pady=(15, 10))

        btn_frame = tk.Frame(self.main_frame, bg="#F4F6F7")
        btn_frame.pack(pady=10)
        buttons = [("Да, всё верно!", self._handle_success), ("Нет, не угадали", self._draw_learning_screen)]
        for col, (text, cmd) in enumerate(buttons):
            ttk.Button(btn_frame, text=text, width=18, command=cmd).grid(row=0, column=col, padx=10)

        ttk.Button(self.main_frame, text="Вернуться назад", width=42, command=self._handle_back).pack(pady=20)

    def _draw_learning_screen(self):
        """отображает форму обучения: ввод животного, вопроса, ответа и факта"""
        self._clear_frame()
        ttk.Label(self.main_frame, text="Обучение Максима и Артема", style="Header.TLabel").pack(pady=10)
        ttk.Label(self.main_frame, text="Мы сдаемся. Помоги нам стать умнее!").pack(pady=(0, 20))

        form_frame = tk.Frame(self.main_frame, bg="#F4F6F7")
        form_frame.pack(fill="x", padx=10)

        entry_animal = self._add_input_field(form_frame, "Какое животное ты загадал?")
        entry_question = self._add_input_field(form_frame, "Задай вопрос, который отличает твоё животное от нашего:")

        ttk.Label(form_frame, text="Какой правильный ответ на этот вопрос для ТВОЕГО животного?").pack(anchor="w")
        ans_var = tk.StringVar(value="yes")
        rb_frame = tk.Frame(form_frame, bg="#F4F6F7")
        rb_frame.pack(anchor="w", pady=(2, 12))
        ttk.Radiobutton(rb_frame, text="Да", variable=ans_var, value="yes").pack(side="left", padx=(0, 15))
        ttk.Radiobutton(rb_frame, text="Нет", variable=ans_var, value="no").pack(side="left")

        entry_fact = self._add_input_field(form_frame, "Напиши интересный факт об этом животном:", pady=(2, 15))

        def submit_learning():
            """обработчик нажатия кнопки 'сохранить'"""
            animal = entry_animal.get().strip()
            q = entry_question.get().strip()
            fact_input = entry_fact.get().strip()
            ans = ans_var.get()

            if not animal or not q:
                messagebox.showwarning("Внимание", "Пожалуйста, заполните обязательные поля (животное и вопрос)")
                return

            existing = self.engine.find_animal(animal)
            if existing:
                fact = existing.fact
                if fact_input:
                    messagebox.showinfo("Информация", "Это животное уже есть в базе. Будет использован известный факт.")
            else:
                if not fact_input:
                    messagebox.showwarning("Внимание", "Факт не может быть пустым для нового животного!")
                    return
                fact = fact_input

            self.engine.learn_new_animal(animal, q, ans, fact)
            messagebox.showinfo("Успех!", f"Спасибо! Теперь мы знаем, кто такой {animal}!")
            self._show_welcome_screen()

        ttk.Button(self.main_frame, text="Сохранить и вернуться в меню", style="Action.TButton",
                   command=submit_learning).pack(pady=15)

    # --- обработчики действий ---
    def _handle_answer(self, response: str):
        """обрабатывает ответ на вопрос (да/нет) и обновляет состояние"""
        self.engine.answer(response)
        self._refresh_game_state()

    def _handle_back(self):
        """возврат на предыдущий вопрос"""
        if not self.engine.go_back():
            messagebox.showinfo("Максим и Артем", "Вы находитесь в самом начале игры!")
        self._refresh_game_state()

    def _handle_success(self):
        """подтверждение угадывания - возврат в меню"""
        messagebox.showinfo("Победа!", "Отлично! Ещё одна победа в копилку Максима и Артема!")
        self._show_welcome_screen()

    def _on_closing(self):
        """сохраняет дерево и завершает программу"""
        try:
            save_game(self.engine.root, self.save_file)
        except Exception as e:
            messagebox.showerror("Ошибка сохранения", f"Не удалось сохранить прогресс: {e}")
        self.root.destroy()