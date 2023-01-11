"""Основной код текстового редактора"""

# ======================================================================================================================
# Импорт модулей:
# Импорт классов Frame (виджета панели), Label (виджета метки), Menu (виджета главного меню), PhotoImage (для работы с изображениями в окне), TclError (для обработки ошибок GUI), Text (виджет поля для ввода текста), Tk(главного окна), Toplevel (дополнительного окна) и полей DISABLED (заблокированного состояния виджета), END (обозначения конца в текстовом виджете), HORIZONTAL (для обозначения горизонтали), GROOVE (стиля обводки), INSERT (позиции курсора в текстовом виджете), NORMAL (нормального состояния виджета) из модуля tkinter для работы с GUI, VERTICAL (для обозначения вертикали),
# Методов askopenfilename и asksaveasfilename из подпакета tkinter.filedialog для открытия проводника для открытия и сохранения файла соответственно,
# Метода families из подпакета tkinter.font для работы со шрифтами системы,
# Классов Button, Combobox, Scrollbar из подпакета tkinter.ttk для работы с кнопками, раскрывающимися списками и полосами прокрутки,
# Методов askyesno, askyesnocancel, showerror и showinfo из пакета tkinter.messagebox для отображения диалоговых и всплывающих окон,
# Классов ImageTk и Image из модуля PIL для работы с изображениями,
# Словаря windows_locale из модуля locale для получения ID всех локалей,
# Свойства windll модуля ctypes для уточнения локали,
# модуля webbrowser для работы с веб-сайтами,
# модуля os для непосредственной работы с ОС,
# модуля pickle для сериализации объектов,
from tkinter import Frame, Label, Menu, PhotoImage, TclError, Text, Tk, Toplevel, DISABLED, END, HORIZONTAL, GROOVE, INSERT, NORMAL, VERTICAL
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.font import families
from tkinter.ttk import Button, Combobox, Scrollbar
from tkinter.messagebox import askyesno, askyesnocancel, showerror, showinfo
from PIL import Image, ImageTk
from locale import windows_locale
from ctypes import windll
import webbrowser
import os
import pickle


# Создание класса:
class Application(Tk):
    """Главный класс текстового редактора. Весь код текстового редактора распологается здесь"""

    # Шрифты редактора:
    programFont: "Программный шрифт" = ("Arial", 10)
    textFont: "Стандартный шрифт" = ("Arial", 13)
    infoTitleFont: "Шрифт для заголовка окна информации о программе" = ("Arial", 20)
    supportTitleFont: "Шрифт для заголовка окна поддержки" = ("Arial", 20, "bold")
    supportFont: "Шрифт для окна поддержки" = ("Arial", 12)
    referenceTitleFont: "Шрифт для заголовка окна справки" = ("Arial", 15, "bold")
    referenceDescriptionFont: "Шрифт для основной части окна справки" = ("Arial", 13)
    referencePageFont: "Шрифт для номера открытой страницы справки" = ("Arial", 11)
    # P.S. Стандартный шрифт нужен, если вдруг с файлом pickle с сериализованным шрифтом, выбранным пользователем,
    # произойдут технические неполадки!
    # Поддерживаемые языки:
    RUS: "Русский язык" = "Русский"
    ENG: "Английский язык" = "English"
    # Выбранный язык:
    selectLanguage: "Выбранный язык" = None
    # Команды выбранного языка:
    selectedLangComands: "Команды выбранного языка" = None
    # Комманды на разных языках:
    RUScommands: "Команды на русском языке" = (("Файл", "Изменить", "О программе"), ("Создать", "Открыть", "Сохранить", "Сохранить как", "Печать", "Выйти", "Отменить", "Вернуть", "Копировать", "Копировать всё", "Вырезать", "Вставить", "Шрифт", "Кодировка", "Справка", "О программе", "Поддержка", "Закрыть"), ("Текстовый редактор ТекстPad", ), ("Изменить шрифт", "Шрифт", "Размер шрифта", "Цвет шрифта", "ОК", "Отмена", "Применить", "Выбрать цвет", "Размер шрифта не должен превышать 256", "Пример текста:"), ("Название:", "Создатель проекта:", "Дата создания:", "Последнее обновление:", "Версия:", "Текстовый редактор ТекстPad", "ArtProGG, JustPythonист Ltd.", "17 Октября 2022", "6 Января 2023", "1.0", "Закрыть"), ("ОКНО ТЕХПОДДЕРЖКИ", "Большое спасибо за использование моего \nтекстового редактора! Данный редактор был создан\nрусским разработчиком ArtProGG от имени\nкомпании JustPythonист Ltd. Надеемся, что вам\nпонравился мой текстовый редактор\nи вы найдёте решение своей проблемы!", "Вконтакте разработчика", "Email-почта разработчика", "Перейти по ссылке", "Скопировать", "Оценить приложение", "Закрыть", "В связи с несуществованием сервиса оценки данного приложения, оценить приложение невозможно!"), ("Сохранить файл", "Ошибка!", "Неверная кодировка файла или неподдерживаемый файл! Попробуйте открыть другой файл!", "Сохранение файла", "Файл Без имени", "Файл", "Строка. {}   Столбец. {}"), ("Подтверждение выхода", "Вы точно хотите выйти?"), ("Ой!", "К сожалению, печать ещё не реализована!"), ("Ошибка!", "Невозможно получить шрифт после предыдущего сеанса, поэтому он был заменён на Arial 13!"), (("Текстовые файлы", "*.txt*"), ("Все файлы", "*.*")), ("Справка по программе NoteBook", "Назад", "Дальше", "Здесь содержится вся\nосновная информация по использованию\nданного текстового редактора.\nЗа дополнительной информацией\nобращайтесь в техподдержку!", "Записывайте всё нужное в текстовую область\nпрограммы для сохранения, используйте\nсамые стандартные методы работы,\nтакие как копирование, вставку, вырезку.\nВы можете скопировать весь написанный\nвами текст, используя \"Копировать всё\" во\nвкладке меню \"Изменить\", либо\nнажав сочетание клавиш Control+B", "Нажмите \"Сохранить\"/\"Сохранить как\"\nво вкладке меню \"Файл\", либо\nсочетание клавиш Control+S/Control+d,\nчтобы сохранить вашу информацию в файл.\nВы можете сами выбрать\nместо сохранения файла.\nПоздравляю, теперь вашы данные сохранены!", "Теперь, когда ваши данные сохранены в\nфайле, вы можете его открыть и просмотреть,\nлибо же отредактировать ваши записи.\nДля открытия файла, необходимо нажать\n\"Открыть\" во вкладке меню \"Файл\",\nлибо сочетание клавиш Control+U. Далее,\nвы должны выбрать ваш файл в каталоге.", "Для более комфортной работы над файлом,\nвы можете изменить рабочий шрифт,\nнажав \"Шрифт\" во вкладке меню \"Изменить\",\nлибо клавишу \"F5\".\nВы сможете поменять шрифт,\nего размер, для большего комфорта глаз.\nБольше 256, в качестве размера шрифта,\nпоставить нельзя!", "За дополнительной помощью, вы можете\nобратиться напрямую к разработчику.\nНапишите в техподдержку, и мы вам ответим.\nДля просмотра техподдержки, вы можете\nнажать \"Поддержка\" во вкладке меню\n\"О программе\", либо клавишу \"F3\".\nНадеемся, вы найдёте решение\nсвоего вопроса!"), ("Станица {} из {}", "Справка по программе ТекстPad", "Основа работы", "Сохранение в файл", "Открытие файла", "Изменение шрифта", "Дополнительная информация"))
    ENGcommands: "Команды на английском языке" = (("File", "Edit", "About"), ("Create", "Open", "Save", "Save As", "Print", "Exit", "Undo", "Redo", "Copy", "Copy All", "Cut", "Paste", "Font", "Encoding", "Reference", "About", "Support", "Close"), ("Text Editor ТекстPad", ), ("Change Font", "Font", "Font size", "Font color", "OK", "Cancel", "Apply", "Select color", "Font size should not exceed 256", "Text example:"), ("Name:", "Project's Creator:", "Creation Date:", "Last Update:", "Version:", "Text Editor ТекстPad", "ArtProGG, JustPythonист, Ltd.", "17 October 2022", "6 January 2023", "1.0", "Close"), ("SUPPORT WINDOW", "Thank you so much for using my text editor!\nThis editor was created by the Russian developer\nArtProGG on behalf of Justpythonист Software Ltd.\nWe hope that you liked my text editor and\nyou will find a solution to your problem!", "Developer's VKontakte", "Developer's Email", "Follow the Link", "Copy", "Rate the App", "Close", "Due to the non-existence of the rate service of this application, it is impossible to rate the application!"), ("Save file", "Error!", "Wrong file encoding or unsupported file! Try opening another file!", "Saving file", "File Undefined", "File", "Ln. {} Col. {}"), ("Confirm Exit", "Do you want to quit?"), ("Oops!", "Unfortunately, but printing is not realised now!"), ("Error!", "Unable to get font after previous session, so it was changed to Arial 13!"), (("Text files", "*.txt*"), ("All files", "*.*")), ("NoteBook Reference", "Previous", "Next", "It contains all the basic information\non using this text editor.\nFor more information contact technical support", "Write down everything you need\nin the text area of the program for saving,\nuse the most standart methods of work,\nsuch as copying, pasting, cutting.\nYou can copy all the text you have written\nusing \"Copy All\" in the \"Edit\"\nmenu tab, or by pressing\nthe keyboard shortcut Control+B", "Click \"Save\"/\"Save As\" in the \"File\"\nmenu tab, or the keyboard shortcut\nControl+S/Control+D to save\nyour information to a file.\nYou can choose where to save\nthe file. Congratulations,\nnow your data is saved!", "Now that your data has beed saved to a file,\nyou can open it and view or edit your entries.\nTo open a file, you must click \"Open\" in the\n\"File\" menu tab, or use\nthe key combination Control+U.\nNext you have to select yor file in the directory.", "For more comfortable work on the file,\nyou can change the working font by clicking \"Font\"\nin the \"Edit\" menu tab, or by pressing F5.\nyou can change the font, its size,\nfor greater eye comfort.\nMore than 256, as a font size, you can not put!", "For additional help, you can contact the developer\ndirectly, write to technical support, and\nwe will answer you. To view technical support,\nyou can click \"Support\" in the \"About\"\nmenu tab, or press F3. We hope\nyou find a solution to your issue!"), ("Page {} of {}", "ТекстPad Reference", "Basis of work", "Saving into file", "Opening file", "Changing font", "Additional information"))
    # Кортежи для изменения шрифта:
    allFonts: "Кортеж со всеми шрифтами системы" = None
    allSizes: "Кортеж со стандартными размерами шрифта" = (7, 8, 9, 10, 11, 12, 13, 14, 16, 18, 20, 23, 27, 36, 41, 54, 67, 75, 82, 96)
    # Контакты разработчика:
    devEmail: "Email-почта разработчика" = "artprogg_developer@mail.ru"
    # Кортеж с доступными расширениями файлов по умолчанию:
    expancionNames: "Кортеж с расширениями файлов по умолчанию" = (".txt", ".py")
    # Путь к файлам по умолчанию:
    userLogin: "Логин пользователя" = os.path.expanduser("~")
    fileCatalogue: "Путь к файлам по умолчанию" = userLogin + "\\Documents\\"
    # Полное имя данного рабочего файла:
    fileFullName: "Полное имя данного открытого файла" = ""
    # Поле для хранения булева значения: открыт ли файл или нет:
    isOpened: "Булево значение, открыт ли файл или нет" = False
    # Текстовые поля для строки состояния:
    statusbarFileName: "Название файла для строки состояния" = ""
    statusbarLineColumn: "Активные строка и столбец для строки состояния" = ""
    statusbarFont: "Название шрифта для строки состояния" = ""
    statusbarFullText: "Полный текст для строки состояния" = f"  {statusbarFileName:<100s}{statusbarLineColumn:<30s}{statusbarFont:>40s}"
    # Версии программы:
    version: "Версия проекта" = 1.0
    releaseVersion: "Номер релиза проекта" = 1
    # ----------------------------------------------------------
    # Специальные (дополнительные) методы для возврата информации о классе:
    # (Работают только через консоль)

    def __str__(self):
        """Метод для вывода информации о проекте всём"""

        # Вывод информации о проекте:
        return self.__doc__

    def __repr__(self):
        """Метод для вывода всех док-стрингов (строк документации) и аннотаций"""

        # Переменная для хранения информации:
        info = ""
        # Чтение комментария документирования:
        info += "Короткая информация о проекте:\n"
        info += "--- " + self.__doc__ + "\n"
        # Чтение аттрибутов:
        info += "\nСистемные и пользовательские атрибуты:\n"
        for attr in dir(self):
            info += f"--- {attr}\n"
        info += "\nЗначения пользовательских атрибутов:\n"
        for key, val in self.__dict__.items():
            info += f"--- {key}:\t\t\t\t{val}\n"
        # Чтение аннотаций:
        info += "\nАннотации:\n"
        for key, anno in self.__annotations__.items():
            info += f"--- {key}:\t\t\t\t{anno}\n"

        # Возврат информации о классе:
        return info

    def __float__(self):
        """Метод для возврата версии проекта"""

        # Возврат версии проекта:
        return self.version

    def __int__(self):
        """Метод для возврата первой цифры версии (номера оффициального релиза)"""

        # Возврат номера релиза проекта:
        return self.releaseVersion
    # ----------------------------------------------------------
    # Главный конструктор (инициализатор) класса:

    def __init__(self, selectedLang: "Выбранный язык" = None, *args, **kwargs):
        """Инициализатор класса текстового редактора"""

        # Интернационализация программы:
        # (При выборе языка (например, русского), определённая заранее переменная начинает ссылаться на кортеж
        # команд на выбранном языке, и, для некоторых случаев, в заранее определённую переменную заносится название
        # Выбранного языка)
        if selectedLang == self.RUS:
            # Если был выбран русский язык:
            self.selectLanguage = self.RUS
            self.selectedLangComands = self.RUScommands
        elif selectedLang == self.ENG:
            # Если был выбран английский язык:
            self.selectLanguage = self.ENG
            self.selectedLangComands = self.ENGcommands
        # Пользователь не сможет сам изменить язык, т.к. настройки ещё не созданы, а через консоль вряд ли получится, поэтому язык выставляется в соответствии с настройками локали:
        elif selectedLang == None:
            if windows_locale[windll.kernel32.GetUserDefaultUILanguage()].startswith("ru"):
                # Если основной язык системы - русский:
                self.selectLanguage = self.RUS
                self.selectedLangComands = self.RUScommands
            elif windows_locale[windll.kernel32.GetUserDefaultUILanguage()].startswith("en"):
                # Если основной язык системы - русский:
                self.selectLanguage = self.ENG
                self.selectedLangComands = self.ENGcommands

        # Инициализация базового класса:
        super().__init__(*args, **kwargs)
        # Инициализация GUI:
        self.__initGUI()
        # Получение данных о шрифте после предыдущего сеанса:
        self.__getFontPickle()
        # Установка слотов (обработчиков событий):
        self._setSlots()
    # ----------------------------------------------------------
    # Методы для инициализации главного окна и установки слотов:

    def __initGUI(self):
        """Инициализатор главного окна"""

        # Размеры приложения зависят от разрешения монитора:
        widthRelation: "Отношение ширины моего монитора к ширине приложения на моём мониторе" = 1.7075
        heightRelation: "Отношение высоты моего монитора к высоте приложения на моём мониторе" = 1.536
        width: "Ширина окна" = int(windll.user32.GetSystemMetrics(0) / widthRelation)
        height: "Высота окна" = int(windll.user32.GetSystemMetrics(1) / heightRelation)
        moveX: "Смещение по ширине" = int((windll.user32.GetSystemMetrics(0) - width) / 2)
        moveY: "Смещение по ширине" = int((windll.user32.GetSystemMetrics(1) - height) / 2)

        # Настройка главного окна:
        self.geometry(f"{width}x{height}+{moveX}+{moveY}")
        # self.geometry("800x500+283+134")
        self.title(self.selectedLangComands[2][0])
        self.resizable(True, True)
        self.iconphoto(True, PhotoImage(file="logo.ico"))
        # Создание виджетов:
        # --- Виджет поля для ввода текста:
        self.text: "Поле для ввода текста" = Text(self, font=self.textFont, height=232, undo=True, wrap="none")
        # P.S. Высота поля для ввода текста подобрана так, что при размере шрифта 1, высота этого поля менятся не будет!
        # --- --- Фокусировка на поле для ввода текста:
        self.text.focus_set()
        # --- Полосы прокрутки для поля Text по координатам X и Y:
        self.xscroll: "Полоса прокрутки по координате X" = Scrollbar(self, orient=HORIZONTAL)
        self.yscroll: "Полоса прокрутки по координате Y" = Scrollbar(self, orient=VERTICAL)
        # --- Виджет строки состояния:
        self.statusbar: "Строка состояния" = Label(self, bg="white", anchor="center", font=self.programFont, text=self.statusbarFullText)
        # Создание главного меню:
        # --- Создание строки главного меню:
        self.menu: "Строка главного меню" = Menu(self, tearoff=0, font=self.programFont)
        # --- Создание секций главного меню:
        self.file_sectionMenu: "Секция меню для работы с файлом" = Menu(self, tearoff=0, font=self.programFont)
        self.refactor_sectionMenu: "Секция меню для рефакторинга файла" = Menu(self, tearoff=0, font=self.programFont)
        self.about_sectionMenu: "Секция меню для информации о программе" = Menu(self, tearoff=0, font=self.programFont)
        # --- Заполнение секций меню и их добавление в строку меню:
        self._fillMainMenu()
        # Создание контекстного меню:
        self.contextMenu = Menu(self, tearoff=0, font=self.programFont)
        # --- Заполнение контекстного меню:
        self._fillContextMenu()

        # Применение новых данных в связи с выбором языка:
        self.statusbarFileName = self.selectedLangComands[6][4]
        self.statusbarLineColumn = self.selectedLangComands[6][6].format(1, 0)
        self.statusbarFullText = f"  {self.statusbarFileName:<100s}{self.statusbarLineColumn:<30s}{self.statusbarFont:>40s}"
        self.statusbar.configure(text=self.statusbarFullText)

        # Размещение объектов в окне:
        self.statusbar.pack(side="bottom", fill="x")
        self.yscroll.pack(side="right", fill="y")
        self.xscroll.pack(side="bottom", fill="x")
        self.text.pack(fill="both", padx=5, pady=5)
        self.config(menu=self.menu)

        # Установка протоколов для окна:
        self.protocol("WM_DELETE_WINDOW", self.__exit)

    def _fillMainMenu(self):
        """Метод, заполняющий секции меню"""

        # Заполнение секции меню для работы с файлом:
        self.file_sectionMenu.add_command(label=self.selectedLangComands[1][0], command=self.__createFile, font=self.programFont, accelerator="Ctrl + T")
        self.file_sectionMenu.add_command(label=self.selectedLangComands[1][1], command=self.__openFile, font=self.programFont, accelerator="Ctrl + U")
        self.file_sectionMenu.add_separator()
        self.file_sectionMenu.add_command(label=self.selectedLangComands[1][2], command=self.__saveFile, font=self.programFont, accelerator="Ctrl + S")
        self.file_sectionMenu.add_command(label=self.selectedLangComands[1][3], command=self.__saveAsFile, font=self.programFont, accelerator="Ctrl + D")
        self.file_sectionMenu.add_separator()
        self.file_sectionMenu.add_command(label=self.selectedLangComands[1][4], command=self.__printText, font=self.programFont, accelerator="Ctrl + P")
        self.file_sectionMenu.add_separator()
        self.file_sectionMenu.add_command(label=self.selectedLangComands[1][5], command=self.__exit, font=self.programFont, accelerator="Escape")
        # Заполнение секции меню для рефакторинга файла:
        self.refactor_sectionMenu.add_command(label=self.selectedLangComands[1][6], command=self._undo, font=self.programFont, accelerator="Ctrl + Z")
        self.refactor_sectionMenu.add_command(label=self.selectedLangComands[1][7], command=self._redo, font=self.programFont, accelerator="Ctrl + A")
        self.refactor_sectionMenu.add_separator()
        self.refactor_sectionMenu.add_command(label=self.selectedLangComands[1][8], command=self._copy, font=self.programFont, accelerator="Ctrl + C")
        self.refactor_sectionMenu.add_command(label=self.selectedLangComands[1][9], command=self._copyAll, font=self.programFont, accelerator="Ctrl + B")
        self.refactor_sectionMenu.add_command(label=self.selectedLangComands[1][10], command=self._cut, font=self.programFont, accelerator="Ctrl + X")
        self.refactor_sectionMenu.add_command(label=self.selectedLangComands[1][11], command=self._paste, font=self.programFont, accelerator="Ctrl + V")
        self.refactor_sectionMenu.add_separator()
        self.refactor_sectionMenu.add_command(label=self.selectedLangComands[1][12], command=self._fontChangeWindow, font=self.programFont, accelerator="F5")
        # В данный момент, сменить кодировку невозможно:
        # self.refactor_sectionMenu.add_separator()
        # self.refactor_sectionMenu.add_command(label=self.selectedLangComands[1][13], command=None, font=self.programFont, accelerator="F6")
        # Заполнение секции меню для информации о программе:
        self.about_sectionMenu.add_command(label=self.selectedLangComands[1][14], command=self._referenceWindow, font=self.programFont, accelerator="F1")
        self.about_sectionMenu.add_command(label=self.selectedLangComands[1][15], command=self._infoWindow, font=self.programFont, accelerator="F2")
        self.about_sectionMenu.add_command(label=self.selectedLangComands[1][16], command=self._supportWindow, font=self.programFont, accelerator="F3")
        self.about_sectionMenu.add_separator()
        self.about_sectionMenu.add_command(label=self.selectedLangComands[1][17], command=self.__exit, font=self.programFont, accelerator="F4")
        # Добавление секций меню в строку меню:
        self.menu.add_cascade(label=self.selectedLangComands[0][0], menu=self.file_sectionMenu, font=self.programFont)
        self.menu.add_cascade(label=self.selectedLangComands[0][1], menu=self.refactor_sectionMenu, font=self.programFont)
        self.menu.add_cascade(label=self.selectedLangComands[0][2], menu=self.about_sectionMenu, font=self.programFont)

    def _fillContextMenu(self):
        """Метод для заполнения контекстного меню"""

        # Заполнение командами контекстное меню:
        self.contextMenu.add_command(label=self.selectedLangComands[1][6], command=self._undo, font=self.programFont, accelerator="Ctrl + Z")
        self.contextMenu.add_command(label=self.selectedLangComands[1][7], command=self._redo, font=self.programFont, accelerator="Ctrl + A")
        self.contextMenu.add_separator()
        self.contextMenu.add_command(label=self.selectedLangComands[1][8], command=self._copy, font=self.programFont, accelerator="Ctrl + C")
        self.contextMenu.add_command(label=self.selectedLangComands[1][9], command=self._copyAll, font=self.programFont, accelerator="Ctrl + B")
        self.contextMenu.add_command(label=self.selectedLangComands[1][10], command=self._cut, font=self.programFont, accelerator="Ctrl + X")
        self.contextMenu.add_command(label=self.selectedLangComands[1][11], command=self._paste, font=self.programFont, accelerator="Ctrl + V")
        self.contextMenu.add_separator()
        self.contextMenu.add_command(label=self.selectedLangComands[1][12], command=self._fontChangeWindow, font=self.programFont, accelerator="F5")
        # В данный момент, сменить кодировку невозможно:
        # self.contextMenu.add_separator()
        # self.contextMenu.add_command(label=self.selectedLanguageComands[1][13], command=None, font=self.programFont, accelerator="F6")

    def _contextMenuEvent(self, event):
        """Слот (Обработчик события) на нажатие и отпускание ЛКМ - вызов контекстного меню"""

        # Установка меню как контекстного:
        self.contextMenu.tk_popup(event.x_root, event.y_root)

    def _setSlots(self):
        """Установщик слотов (обработчиков событий)"""

        # Настройка слотов (обработчиков событий) на сигналы от клавиатуры:
        self.bind("<Control-KeyPress>", self.__keyPressEvent)
        self.bind("<Control-c>", lambda e: 'break')
        self.bind("<Control-v>", lambda e: 'break')
        # ----------------------------------------
        self.bind("<F5>", self._fontChangeWindow)
        # ----------------------------------------
        self.bind("<F1>", self._referenceWindow)
        self.bind("<F2>", self._infoWindow)
        self.bind("<F3>", self._supportWindow)
        self.bind("<F4>", self.__escapeExit)
        # ----------------------------------------
        self.bind("<Key>", self._statusbarUpdate)
        self.bind("<Button-1>", self._statusbarUpdate)

        # Настройка слотов (обработчиков событий) на сигналы от мыши:
        self.text.bind("<Button-3><ButtonRelease-3>", self._contextMenuEvent)

        # Настройка полос прокрутки для поля ввода текста:
        self.xscroll.configure(command=self.text.xview)
        self.yscroll.configure(command=self.text.yview)
        self.text["xscrollcommand"] = self.xscroll.set
        self.text["yscrollcommand"] = self.yscroll.set
    # -----------------------------------------------
    # Методы для работы с файлом:

    def __checkUpFile(self) -> bool:
        """Проверка содержимого файла на соответствие содержимому виджета текстового многострочного поля"""

        # Открытие файла:
        with open(self.fileFullName, "r+t") as file:
            # Получение содержимое текстового поля ввода и файла:
            textGet: "Содержимое текстовой области" = self.text.get(1.0, "end-1c")
            fileGet: "Содержимое файла" = file.read()
            # Сравнение результата и возврат:
            return True if textGet == fileGet else False

    def __checkForOtherFile(self):
        """Метод для проверки данного (открытого) файла при попытке открытия нового файла,
           при попытке выхода из программы с несохранённым файлом/информацией и
           возврата состояния файла (если существует) как результата
           (Используется в методах создания и открытия нового файла)"""

        # Переменная для возврата результата о состоянии файла:
        doSave: "Сохранить файл или нет" = False

        # Проверка, открыт ли в это время другой файл:
        if self.isOpened:
            # Проверка, не был ли сохранён этот файл:
            if not self.__checkUpFile():
                # Если открыт и не сохранён, то в диалоговом окне указываем имя файла:
                doSave = askyesnocancel(self.selectedLangComands[6][3], f"{self.selectedLangComands[6][0]} {self.fileFullName}?")
        # Если другого открытого файла нет, то осуществляется проверка на содержимое виджета:
        elif self.text.get(1.0, "end-1c") != "":
            # Если другого файла нет, и текстовая область чем-то заполнена, то выводится простое диалоговое окно:
            doSave = askyesnocancel(self.selectedLangComands[6][3], f"{self.selectedLangComands[6][0]}?")

        # Возврат результата:
        return doSave

    def __differentFileSaving(self) -> bool:
        """Метод, сохраняющий файл/информацию в файл перед различной операцией
           (открытием другого файла или созданием нового)"""

        # Результат сохранения файла зависит от пользователя:
        doSave = self.__checkForOtherFile()

        if doSave == None:
            # Если пользователь отменил операцию, то осуществляется выход из метода:
            return False
        elif doSave:
            # Если пользователь решил сохранить файл, то производится проверка, открыт ли он или нет:
            if self.isOpened:
                # Если открыт, то происходит его сохранение:
                self.__saveFile()
            else:
                # Если нет открытого файла, то производится сохранение засчёт создания нового файла:
                self.__saveAsFile()

        return True

    def __createFile(self, *args, **kwargs):
        """Метод создания файла"""

        # Результат создания файла - сохранение файла (если он существует/не сохранён) и очистка виджета текста!
        # Сохранение предыдущего файла:
        if self.__differentFileSaving():
            # В случае сохранения/несохранения файла, происходит очиска содержимого виджета текста, обновление поля значений
            # файла и заголовок окна:
            self.text.replace(1.0, END, "")
            self.isOpened = False
            self.fileFullName = ""
            self.title(self.selectedLangComands[2][0])
            # Применение данных для строки состояния:
            self.statusbarFileName = self.selectedLangComands[6][4]
            self.statusbarFullText = f"  {self.statusbarFileName:<100s}{self.statusbarLineColumn:<30s}{self.statusbarFont:>40s}"
            self.statusbar.configure(text=self.statusbarFullText)

    def __openFile(self, *args, **kwargs):
        """Метод открытия файла"""

        # Сохранение предыдущего файла:
        if self.__differentFileSaving():
            # Контролируемый ход:
            try:
                # С самого начала происходит очистка значений полей открытого файла и изменение заголовка окна:
                self.isOpened = False
                self.fileFullName = ""
                self.title(self.selectedLangComands[2][0])
                # Очистка текстовой области:
                self.text.delete(1.0, END)
                # Открытие проводника:
                fileBrowser: "Проводник файлов" = askopenfilename(initialdir=self.fileCatalogue, title=self.selectedLangComands[1][1], filetypes=(self.selectedLangComands[10][0], self.selectedLangComands[10][1]))
                # Открытие файла:
                with open(fileBrowser, "r+t") as file:
                    # "Распаковка" содержимого файла в текстовую область:
                    for line in file:
                        self.text.insert(END, line)
                # Если файл открыт успешно, то происходит изменение значения полей открытого файла вместе с заголовком окна:
                self.isOpened = True
                self.fileFullName = fileBrowser
                self.title(self.fileFullName + " - " + self.selectedLangComands[2][0])
                # Применение данных для строки состояния:
                self.statusbarFileName = self.selectedLangComands[6][5] + " " + fileBrowser.split("/")[-1]
                self.statusbarFullText = f"  {self.statusbarFileName:<100s}{self.statusbarLineColumn:<30s}{self.statusbarFont:>40s}"
                self.statusbar.configure(text=self.statusbarFullText)
            # FileNotFoundError - возникает при попытке обращения к несуществующему файлу:
            except FileNotFoundError:
                # Здесь ничего не происходит:
                pass
            # UnicodeDecodeError - возникает при попытке чтения непонятной интерпретатору кодировки файла:
            except UnicodeDecodeError:
                # Здесь сообщается пользователю об ошибке:
                showerror(self.selectedLangComands[6][2], self.selectedLangComands[6][3])

    def __saveFile(self, *args, **kwargs):
        """Метод сохранения файла"""

        # Проверка, открыт ли файл:
        if self.isOpened:
            # Открытие и перезапись файла:
            with open(self.fileFullName, "r+t") as file:
                file.write(self.text.get(1.0, "end-1c"))
        # Если файл не открыт, то производится сохранение файла как нового:
        else:
            self.__saveAsFile(args, kwargs)

    def __saveAsFile(self, *args, **kwargs):
        """Метод сохранения в новый файл"""

        # Контролируемый ход:
        try:
            # Открытие проводника:
            fileBrowser = asksaveasfilename(initialdir=self.fileCatalogue, title=self.selectedLangComands[1][3], filetypes=(self.selectedLangComands[10][0], self.selectedLangComands[10][1]), defaultextension=".txt")
            # Открытие файла:
            with open(fileBrowser, "w") as file:
                # Запись содержимого виджета текста в файл:
                file.write(self.text.get(1.0, "end-1c"))
                # Если файл открыт успешно, то происводится изменение значения полей открытого файла вместе с заголовком окна:
                self.fileFullName = fileBrowser
                self.title(self.fileFullName + " - " + self.selectedLangComands[2][0])
                # Применение данных для строки состояния:
                self.statusbarFileName = self.selectedLangComands[6][5] + " " + fileBrowser.split("/")[-1]
                self.statusbarFullText = f"  {self.statusbarFileName:<100s}{self.statusbarLineColumn:<30s}{self.statusbarFont:>40s}"
                self.statusbar.configure(text=self.statusbarFullText)
        # FileNotFoundError - возникает при попытке обращения к несуществующему файлу:
        except FileNotFoundError:
            # Здесь ничего не происходит:
            pass

    # -----------------------------------------------
    # Методы для рефакторинга и редактирования кода:

    def _undo(self, *args, **kwargs):
        """Метод для отмены предыдущего действия"""

        # Контролируемый ход:
        try:
            # Возврат текста в предыдущее состояние:
            self.text.edit_undo()
        # _tkinter.TclError - Происходит, если отменить нечего:
        except TclError:
            # Здесь ничего не происходит:
            pass

    def _redo(self, *args, **kwargs):
        """Метод для возврата предыдущего действия"""

        # Контролируемый ход:
        try:
            # Возврат текста в предыдущее состояние:
            self.text.edit_redo()
        # _tkinter.TclError - Происходит, если вернуть нечего:
        except TclError:
            # Здесь ничего не происходит:
            pass

    def _copy(self, *args, **kwargs):
        """Метод для копирования выделенного текста"""

        # Контролируемый ход:
        try:
            # Копирование в буфер обмена выделенного текста:
            os.system(f"echo {self.text.selection_get()}| clip")
        # _tkinter.TclError - происходит, если выделенного текста нет:
        except TclError:
            # Здесь ничего не происходит:
            pass

    def _copyAll(self, *args, **kwargs):
        """Метод для копирования всего текста"""

        # Копирование в буфер обмена текста из виджета:
        stringNew: "Символ перевода строки" = "\n"
        os.system(f"echo {self.text.get(1.0, 'end-1c').replace(stringNew, '')}| clip")

    def _cut(self, *args, **kwargs):
        """Метод для вырезки выделенного текста"""

        # Генерация события вырезки:
        self.text.event_generate("<<Cut>>")

    def _paste(self, *args, **kwargs):
        """Метод для вставки скопированного текста"""

        # Генерация встроенного событие вставки:
        self.text.insert(INSERT, self.clipboard_get())
    # -----------------------------------------------
    # Методы для работы со шрифтом текстовой области:

    def __setFontPickle(self, *args, **kwargs):
        """Метод, сериализующий шрифт программы в файл serialize.ini (pickle)"""

        # Открытие файла для загрузки параметров шрифта:
        with open("serialize.ini", "wb") as file:
            # Загрузка данных о шрифте в файл:
            pickle.dump(self.textFont, file, pickle.HIGHEST_PROTOCOL)

    def __getFontPickle(self, *args, **kwargs):
        """Метод, получающий шрифт программы из сериализованного объекта файла serialize.ini (pickle)"""

        # Открытие файла для выгрузки параметров шрифта с обработкой ошибок:
        try:
            with open("serialize.ini", "rb") as file:
                # Получение данных о шрифте и объявление его как стандартного:
                font: "Выгруженный шрифт с предыдущего сеанса"
                size: "Выгруженный размер шрифта с предыдушего сеанса"
                font, size = pickle.load(file)
                self.textFont = (font, int(size))
                self.text.configure(font=self.textFont)
                # Применение данных для строки состояния:
                self.statusbarFont = self.textFont[0] + " " + str(self.textFont[1])
                self.statusbarFullText = f"  {self.statusbarFileName:<100s}{self.statusbarLineColumn:<30s}{self.statusbarFont:>40s}"
                self.statusbar.configure(text=self.statusbarFullText)
        # _pickle.UnpicklingError - возникает при повреждении закодированного файла pickle:
        except pickle.UnpicklingError as error:
            # Вывод информации об ошибке в информационном окне и применение стандартного шрифта:
            showerror(self.selectedLangComands[9][0], self.selectedLangComands[9][1])
            self.text.configure(font=self.textFont)
        # FileNotFoundError - возникает при попытке открыть несуществующий файл:
        except FileNotFoundError as error:
            # Вывод информации об ошибке в информационном окне и применение стандартного шрифта:
            showerror(self.selectedLangComands[9][0], self.selectedLangComands[9][1])
            self.text.configure(font=self.textFont)
        # EOFError - возникает, при попытке загрузки по индексу несуществующей информации (информация вышла "за рамки")
        # P.S. Вряд ли возникнет, так как все данные загружаются вручную, установленное количество раз:
        except EOFError as error:
            # Вывод информации об ошибке в информационном окне:
            showerror(self.selectedLangComands[9][0], self.selectedLangComands[9][1])

    def _fontChangeWindow(self, *args, **kwargs):
        """Метод, вызывающий окно для изменения шрифта"""

        # Дополнительные функции:
        # --- Функция для закрытия окна (дополнительно прописана явно):
        def _closeWindow(*args, **kwargs):
            """Функция для закрытия окна для изменения шрифта"""

            # Её можно было не прописывать, но на всякий случай я сделал это явно:
            fontWindow.destroy()

        # --- Функция для блокировки кнопки "Применить" в нужный момент:
        def _updateWindow(*args, **kwargs):
            """Функция для блокировки кнопки 'Применить' при совпадении настроек шрифта и обновлении текстовой метки"""

            # Контролируемый ход:
            try:
                # Обновление шрифта текстовой метки:
                testLabel.configure(font=(fontList.get(), int(sizeList.get())))
                # Проверка шрифта:
                if ((fontList.get(), int(sizeList.get())) == self.textFont) or ((fontList.get(), sizeList.get()) == self.textFont):
                    # Если шрифт, выбранный в окне изменения, совпадает с основным шрифтом, то кнопка применения блокируется:
                    APPLYButton.configure(state=DISABLED)
                else:
                    # Если шрифты отличаются, то кнопка применения разблокируется:
                    APPLYButton.configure(state=NORMAL)
                # Предупреждение о том, что размер шрифта не должен превышать 256:
                if int(sizeList.get()) > 256:
                    # Если размер шрифта больше, то мы показываем текст на предупреждающей метке:
                    warningLabel.configure(text=self.selectedLangComands[3][8])
                else:
                    # Если же меньше, то скрываем текст предупреждащей метки:
                    warningLabel.configure(text="")
            # TclError (_tkinter.TclError) - может возникнуть, если в качестве размера шрифта было введено
            # слишком большое число:
            except TclError:
                # Здесь ничего не происходит:
                pass
            # ValueError - может возникнуть, если в поле ввода раскрывающегося списка в качестве параметра
            # для размера шрифта будет введён не целочисленный тип данных:
            except ValueError:
                # Здесь ничего не происходит:
                pass

        # Слоты (Обработчики событий):
        # --- Слот на кнопку применения шрифта:
        def _applyFont(*args, **kwargs):
            """Слот на кнопку применения шрифта и обработки того же"""

            # Контролируемый ход событий:
            try:
                # Применение настроек на данный сеанс:
                # P.S. Размер шрифта должен быть меньше 256, это делается с соображением эстетики:
                if int(sizeList.get()) > 256:
                    # Если размер шрифта больше 256, то мы размер шрифта просто не меняем:
                    self.textFont = (fontList.get(), self.textFont[1])
                else:
                    # Если размер шрифта меньше или равен 256, то размер шрифта можно изменить:
                    self.textFont = (fontList.get(), sizeList.get())
                self.text.configure(font=self.textFont)
                # Сериализация шрифта в байт-файл:
                self.__setFontPickle()
                # Блокировка кнопки применения:
                APPLYButton.configure(state=DISABLED)
                # Применение данных для строки состояния:
                self.statusbarFont = self.textFont[0] + " " + self.textFont[1]
                self.statusbarFullText = f"  {self.statusbarFileName:<100s}{self.statusbarLineColumn:<30s}{self.statusbarFont:>40s}"
                self.statusbar.configure(text=self.statusbarFullText)
            # ValueError - может возникнуть, если в качестве размера шрифта будет получен нецелочисленный тип данных:
            except ValueError:
                # Здесь ничего не происходит:
                pass

        # --- Слот для применения шрифта и автоматического выхода:
        def _applyFont_andExit(*args, **kwargs):
            """Слот на кнопку 'Enter' для применения шрифта и автоматического выхода из окна"""

            # Вызов основного метода и закрытие окна:
            _applyFont(args, kwargs)
            _closeWindow(args, kwargs)

        # Объявление кортежа шрифтов (до объявления стандартного окна, будет выводится ошибка):
        self.allFonts = families(self)

        # Размеры приложения зависят от разрешения монитора:
        widthRelation: "Отношение ширины моего монитора к ширине окна на моём мониторе" = 4.553
        heightRelation: "Отношение высоты моего монитора к высоте окна на моём мониторе" = 2.194
        width: "Ширина окна" = int(windll.user32.GetSystemMetrics(0) / widthRelation)
        height: "Высота окна" = int(windll.user32.GetSystemMetrics(1) / heightRelation)
        moveX: "Смещение по ширине" = int((windll.user32.GetSystemMetrics(0) - width) / 2)
        moveY: "Смещение по ширине" = int((windll.user32.GetSystemMetrics(1) - height) / 2)
        # P.S. Размеры для приложения не устанавливаются, т.к. они бы противоречили размерам виджетов!

        # Создание и настройка дополнительного окна:
        fontWindow: "Дополнительное окно для изменения шрифта" = Toplevel()
        fontWindow.geometry(f"300x350+{moveX}+{moveY}")
        fontWindow.resizable(False, False)
        fontWindow.title(self.selectedLangComands[3][0])

        # Создание и настройка виджетов окна:
        # --- Создание панелей:
        fontFrame: "Панель для раскрывающегося списка шрифтов" = Frame(fontWindow, relief=GROOVE, bd=3)
        sizeFrame: "Панель для раскрывающегося списка размеров" = Frame(fontWindow, relief=GROOVE, bd=3)
        # colorFrame: "Панель для инструментов изменения цвета шрифта" = Frame(fontWindow, relief=GROOVE, bd=3, width=250, height=110)
        # --- Создание раскрывающихся списков:
        fontList: "Раскрывающийся список шрифтов" = Combobox(fontWindow, state="readonly", values=self.allFonts, font=self.programFont)
        sizeList: "Раскрывающийся список размеров" = Combobox(fontWindow, values=self.allSizes, font=self.programFont)
        # --- --- Установка значений шрифта с предыдущего сеанса:
        fontList.current(self.allFonts.index(self.textFont[0]))
        sizeList.set(int(self.textFont[1]))
        # --- Создание меток:
        fontLabel: "Метка для списка шрифтов" = Label(fontWindow, text=self.selectedLangComands[3][1], font=self.programFont)
        sizeLabel: "Метка для списка размеров" = Label(fontWindow, text=self.selectedLangComands[3][2], font=self.programFont)
        warningLabel: "Предупреждающая метка (появляется, если установить размер шрифта больше 256)" = Label(fontWindow, text=None, fg="red", font=self.programFont)
        # colorLabel: "Метка для кнопки изменения цвета шрифта" = Label(fontWindow, text=self.selectedLangComands[3][3], font=self.programFont, height=25)
        testLabel: "Метка для предварительного просмотра шрифта" = Label(fontWindow, text="Привет Everybody!", font=self.textFont)
        infoLabel: "Метка с текстом о тестовой метке (пример текста)" = Label(fontWindow, text=self.selectedLangComands[3][9], font=self.programFont)
        # --- Создание кнопок:
        OKButton: "Кнопка ОК" = Button(fontWindow, text=self.selectedLangComands[3][4])
        CANCELButton: "Кнопка Отмена" = Button(fontWindow, text=self.selectedLangComands[3][5])
        APPLYButton: "Кнопка Применить" = Button(fontWindow, text=self.selectedLangComands[3][6], state=DISABLED)
        # select_colorButton: "Кнопка выбора цвета" = tkinter.ttk.Button(fontWindow, text="Выбрать цвет")

        # Установка обработчиков событий:
        fontWindow.bind("<F5>", _closeWindow)
        # --------------------------------------------------
        fontWindow.bind("<Return>", _applyFont_andExit)
        fontList.bind("<<ComboboxSelected>>", _updateWindow)
        sizeList.bind("<<ComboboxSelected>>", _updateWindow)
        sizeList.bind("<KeyRelease>", _updateWindow)
        OKButton.configure(command=_closeWindow)
        CANCELButton.configure(command=_closeWindow)
        APPLYButton.configure(command=_applyFont)

        # Размешение виджетов на окне:
        fontFrame.place(x=5, y=10, width=250, height=65)
        sizeFrame.place(x=5, y=80, width=250, height=90)
        # colorFrame.place(x=5, y=150)
        # -----------------------------------------------
        fontLabel.place(x=15, y=15, height=25)
        sizeLabel.place(x=15, y=85, height=25)
        # colorLabel.place(x=15, y=155)
        # -----------------------------------------------
        fontList.place(x=15, y=40, width=230, height=25)
        sizeList.place(x=15, y=110, width=230, height=25)
        # -----------------------------------------------
        infoLabel.place(x=5, y=175)
        testLabel.place(x=5, y=200, width=290, height=100)
        warningLabel.place(x=15, y=140)
        # -----------------------------------------------
        # select_colorButton(x=10, y=220, width=125, height=30)
        OKButton.place(x=40, y=315, width=80, height=25)
        CANCELButton.place(x=125, y=315, width=80, height=25)
        APPLYButton.place(x=210, y=315, width=80, height=25)

        # Фокусировка на окно и захват на него:
        fontWindow.focus_set()
        fontWindow.grab_set()
        # Отображение окна:
        fontWindow.mainloop()
    # -----------------------------------------------
    # Методы, связанные с поддержкой программы:

    def _infoWindow(self, *args, **kwargs):
        """Метод, вызывающий окно с информацией о программе"""

        # Слот для закрытия окна:
        def _closeWindow(*args, **kwargs):
            """Слот для закрытия окна"""

            # Закрытие окна (на всякий случай, данный метод прописан отдельно):
            infoWindow.destroy()

        # Размеры приложения зависят от разрешения монитора:
        widthRelation: "Отношение ширины моего монитора к ширине окна на моём мониторе" = 3.415
        heightRelation: "Отношение высоты моего монитора к высоте окна на моём мониторе" = 1.92
        width: "Ширина окна" = int(windll.user32.GetSystemMetrics(0) / widthRelation)
        height: "Высота окна" = int(windll.user32.GetSystemMetrics(1) / heightRelation)
        moveX: "Смещение по ширине" = int((windll.user32.GetSystemMetrics(0) - width) / 2)
        moveY: "Смещение по ширине" = int((windll.user32.GetSystemMetrics(1) - height) / 2)
        # P.S. Размеры для приложения не устанавливаются, т.к. они бы противоречили размерам виджетов!

        # Создание и настройка дополнительного окна с информацией о программе:
        infoWindow: "Дополнительное окно с информацией о программе" = Toplevel()
        infoWindow.geometry(f"400x400+{moveX}+{moveY}")
        infoWindow.resizable(False, False)
        infoWindow.title("О программе")

        # Создание и настройка виджетов окна:
        imageObject: "Объект изображения-логотипа" = ImageTk.PhotoImage(Image.open("logotype.png"))
        logoImage: "Логотип программы" = Label(infoWindow, image=imageObject)
        logoTitle: "Заголовок логотипа" = Label(infoWindow, text=self.selectedLangComands[2][0], font=self.infoTitleFont)
        # ---------------------------------------------------------------------------------------------------------------------------
        nameLabel: "Метка названия проекта" = Label(infoWindow, text=self.selectedLangComands[4][0], font=self.programFont)
        authorLabel: "Метка автора проекта" = Label(infoWindow, text=self.selectedLangComands[4][1], font=self.programFont)
        birthLabel: "Метка даты создания проекта" = Label(infoWindow, text=self.selectedLangComands[4][2], font=self.programFont)
        lastUpdateLabel: "Метка даты последнего обновления" = Label(infoWindow, text=self.selectedLangComands[4][3], font=self.programFont)
        versionLabel: "Метка нынешней версия" = Label(infoWindow, text=self.selectedLangComands[4][4], font=self.programFont)
        # ---------------------------------------------------------------------------------------------------------------------------
        nameLabel2: "Название проекта" = Label(infoWindow, text=self.selectedLangComands[4][5], font=self.programFont)
        authorLabel2: "Автор проекта" = Label(infoWindow, text=self.selectedLangComands[4][6], font=self.programFont)
        birthLabel2: "Дата создания проекта" = Label(infoWindow, text=self.selectedLangComands[4][7], font=self.programFont)
        lastUpdateLabel2: "Дата последнего обновления" = Label(infoWindow, text=self.selectedLangComands[4][8], font=self.programFont)
        versionLabel2: "Нынешняя версия" = Label(infoWindow, text=self.selectedLangComands[4][9], font=self.programFont)
        # ---------------------------------------------------------------------------------------------------------------------------
        closeButton: "Конпка закрытия окна" = Button(infoWindow, text=self.selectedLangComands[4][10])

        # Настройка слотов:
        infoWindow.bind("<F2>", _closeWindow)
        # -----------------------------------
        closeButton.configure(command=_closeWindow)

        # Размещение виджетов:
        logoImage.place(x=125, y=15)
        # ----------------------------------------------------------
        # Размещение заголовка логотипа зависит от выбранного языка:
        if self.selectLanguage == self.RUS:
            logoTitle.place(x=10, y=180)
        elif self.selectLanguage == self.ENG:
            logoTitle.place(x=50, y=180)
        # ----------------------------------------------------------
        nameLabel.place(x=20, y=240)
        authorLabel.place(x=20, y=260)
        birthLabel.place(x=20, y=280)
        lastUpdateLabel.place(x=20, y=300)
        versionLabel.place(x=20, y=320)
        # ----------------------------------------------------------
        nameLabel2.place(x=200, y=240)
        authorLabel2.place(x=200, y=260)
        birthLabel2.place(x=200, y=280)
        lastUpdateLabel2.place(x=200, y=300)
        versionLabel2.place(x=200, y=320)
        # ----------------------------------------------------------
        closeButton.place(x=15, y=350, width=370, height=40)

        # Фокусировка и захват окна:
        infoWindow.focus_set()
        infoWindow.grab_set()

        # Отображение окна:
        infoWindow.mainloop()

    def _supportWindow(self, *args, **kwargs):
        """Метод, вызывающий окно с техподдержкой"""

        # Слот для закрытия окна (на всякий случай прописан самостоятельно):
        def _closeWindow(*args, **kwargs):
            """Слот для закрытия окна техподдержки"""

            # Закрытие окна:
            supportWindow.destroy()

        # Слот для копирования email-почты:
        def _copyDevEmail(*args, **kwargs):
            """Слот для копирования email-почты"""

            # Копирование почты разработчика:
            os.system(f"echo {self.devEmail}| clip")

        # Слот для оценки приложения:
        def _rateApp(*args, **kwargs):
            """Слот для оценки приложения"""

            # На данный момент я не имею собственного веб-сайта, либо базы данных, а приложение лне имеет
            # собственной страницы в каком-либо магазине:
            showinfo(self.selectedLangComands[5][6], self.selectedLangComands[5][8])

        # Размеры приложения зависят от разрешения монитора:
        widthRelation: "Отношение ширины моего монитора к ширине окна на моём мониторе" = 3.415
        heightRelation: "Отношение высоты моего монитора к высоте окна на моём мониторе" = 1.92
        width: "Ширина окна" = int(windll.user32.GetSystemMetrics(0) / widthRelation)
        height: "Высота окна" = int(windll.user32.GetSystemMetrics(1) / heightRelation)
        moveX: "Смещение по ширине" = int((windll.user32.GetSystemMetrics(0) - width) / 2)
        moveY: "Смещение по ширине" = int((windll.user32.GetSystemMetrics(1) - height) / 2)
        # P.S. Размеры для приложения не устанавливаются, т.к. они бы противоречили размерам виджетов!

        # Создание и настройка дополнительного окна техподдержки:
        supportWindow: "Дополнительное окно техподдержки" = Toplevel()
        supportWindow.geometry(f"400x400+{moveX}+{moveY}")
        supportWindow.resizable(False, False)
        supportWindow.title()

        # Создание виджетов окна:
        titleLabel: "Метка с заголовком" = Label(supportWindow, text=self.selectedLangComands[5][0], font=self.supportTitleFont)
        infoLabel: "Метка с сообщением" = Label(supportWindow, text=self.selectedLangComands[5][1], font=self.supportFont)
        EmailLabel: "Метка к кнопке копирования email-почты разработчика" = Label(supportWindow, text=self.selectedLangComands[5][3], font=self.supportFont)
        # ---------------------------------------------------------------------------------------------------------------------------
        closeButton: "Кнопка для закрытия окна" = Button(supportWindow, text=self.selectedLangComands[5][7])
        rateButton: "Кнопка для оценки приложения" = Button(supportWindow, text=self.selectedLangComands[5][6])
        copyEmailButton: "Кнопка для копирования email-почты разработчика" = Button(supportWindow, text=self.selectedLangComands[5][5])

        # Настройка слотов:
        supportWindow.bind("<F3>", _closeWindow)
        # ----------------------------------------------
        closeButton.configure(command=_closeWindow)
        rateButton.configure(command=_rateApp)
        copyEmailButton.configure(command=_copyDevEmail)

        # Расположение виджетов:
        titleLabel.pack(pady=20)
        infoLabel.pack(pady=0)
        EmailLabel.place(x=10, y=250, height=30)
        # ------------------------------------------
        closeButton.place(x=205, y=345, width=190, height=50)
        rateButton.place(x=5, y=345, width=190, height=50)
        copyEmailButton.place(x=225, y=250, width=150, height=30)

        # Фокусировка и захват окна:
        supportWindow.focus_set()
        supportWindow.grab_set()

        # Отображение окна:
        supportWindow.mainloop()

    def _referenceWindow(self, *args, **kwargs):
        """Метод, вызывающий окно со справкой"""

        # Слот для закрытия справки:
        def _closeWindow(*args, **kwargs):
            """Слот для закрытия окна со справкой"""

            # Закрытие окна (На всякий случай данный метод прописан отдельно):
            referenceWindow.destroy()

        # Слот для перематывания на новую страницу:
        def _nextPage(*args, **kwargs):
            """Слот для открытия новой страницы"""

            # Объявление переменных верхнего метода:
            nonlocal pageNumber
            nonlocal pageCount
            # Увеличение переменной-счётчика:
            pageNumber += 1
            if pageNumber >= pageCount:
                # Проверка, если переменная-счётчик достигла максимума, то кнопка блокируется:
                nextButton.configure(state=DISABLED)
            # Если пользователь решил перейти на следующую страницу, то по логике
            # переменная-счётчик больше минимума, значит можно разблокировать кнопку для перехода на предыдущую страницу:
            previousButton.configure(state=NORMAL)
            # Изменение меток:
            titleLabel.configure(text=self.selectedLangComands[12][0 + pageNumber])
            descriptionLabel.configure(text=self.selectedLangComands[11][2 + pageNumber])
            pageLabel.configure(text=self.selectedLangComands[12][0].format(pageNumber, pageCount))

        # Слот для перематывания на предыдущую страницу:
        def _previousPage(*args, **kwargs):
            """Слот для открытия предыдущей страницы"""

            # Объявление переменных верхнего метода:
            nonlocal pageNumber
            nonlocal pageCount
            # Уменьшение переменной-счётчика:
            pageNumber -= 1
            if pageNumber <= 1:
                # Проверка, если переменная-счётчик достигла минимума, то кнопка блокируется:
                previousButton.configure(state=DISABLED)
            # Если пользователь решил перейти на предыдущую страницу, то по логике
            # переменная-счётчик меншье максимума, значит можно разблокировать кнопку для перехода на следующую страницу:
            nextButton.configure(state=NORMAL)
            # Изменение меток:
            titleLabel.configure(text=self.selectedLangComands[12][0 + pageNumber])
            descriptionLabel.configure(text=self.selectedLangComands[11][2 + pageNumber])
            pageLabel.configure(text=self.selectedLangComands[12][0].format(pageNumber, pageCount))

        # Смещение приложения зависят от разрешения монитора:
        widthRelation: "Отношение ширины моего монитора к ширине окна на моём мониторе" = 3.415
        heightRelation: "Отношение высоты моего монитора к высоте окна на моём мониторе" = 1.92
        width: "Ширина окна" = int(windll.user32.GetSystemMetrics(0) / widthRelation)
        height: "Высота окна" = int(windll.user32.GetSystemMetrics(1) / heightRelation)
        moveX: "Смещение по ширине" = int((windll.user32.GetSystemMetrics(0) - width) / 2)
        moveY: "Смещение по ширине" = int((windll.user32.GetSystemMetrics(1) - height) / 2)
        # P.S. Размеры для приложения не устанавливаются, т.к. они бы противоречили размерам виджетов!

        # Создание и настройка дополнительного окна справки:
        referenceWindow: "Дополнительное окно справки" = Toplevel()
        referenceWindow.geometry(f"400x400+{moveX}+{moveY}")
        referenceWindow.resizable(False, False)
        referenceWindow.title(self.selectedLangComands[11][0])

        # Создание специальных переменных:
        pageNumber: "Номер страницы" = 1
        pageCount: "Количество страниц" = 6

        # Создание виджетов окна:
        grooveFrame: "Рамка-обводка для справки" = Frame(referenceWindow, relief=GROOVE, bd=5)
        # --------------------------------------------------------------------------------------------------------
        titleLabel: "Заголовок/название справки" = Label(referenceWindow, text=self.selectedLangComands[12][1], font=self.referenceTitleFont)
        descriptionLabel: "Основная часть справки" = Label(referenceWindow, text=self.selectedLangComands[11][3], font=self.referenceDescriptionFont)
        pageLabel: "Метка для отображения номера страницы" = Label(referenceWindow, text=self.selectedLangComands[12][0].format(pageNumber, pageCount), font=self.referencePageFont)
        # --------------------------------------------------------------------------------------------------------
        closeButton: "Кнопка для выхода из окна" = Button(referenceWindow, text=self.selectedLangComands[5][7])
        previousButton: "Кнопка для перехода на предыдущую страницу" = Button(referenceWindow, text=self.selectedLangComands[11][1], state=DISABLED)
        nextButton: "Кнопка для перехода на следующую страницу" = Button(referenceWindow, text=self.selectedLangComands[11][2])

        # Настройка слотов:
        referenceWindow.bind("<F1>", _closeWindow)
        # --------------------------------------------
        closeButton.configure(command=_closeWindow)
        previousButton.configure(command=_previousPage)
        nextButton.configure(command=_nextPage)

        # Расположение виджетов:
        grooveFrame.place(x=5, y=5, width=390, height=340)
        # ------------------------------------------------
        titleLabel.pack(pady=10)
        descriptionLabel.place(x=15, y=50, width=370)
        pageLabel.place(x=260, y=310)
        # ------------------------------------------------
        closeButton.place(x=115, y=355, width=90, height=30)
        previousButton.place(x=210, y=355, width=90, height=30)
        nextButton.place(x=305, y=355, width=90, height=30)

        # Фокусировка окна:
        referenceWindow.focus_set()

        # Отображение окна:
        referenceWindow.mainloop()
    # -----------------------------------------------
    # Дополнительные методы, связанные с приложением:

    def __printText(self, *args, **kwargs):
        """Метод для печати текста"""

        # В данной версии, печать не реализована!
        showinfo(self.selectedLangComands[8][0], self.selectedLangComands[8][1])

    def _statusbarUpdate(self, *args, **kwargs):
        """Метод для обновления строки состояния
           (в частности, номеров строки и столбца)"""

        # Применение данных для строки состояния
        self.statusbarLineColumn = self.selectedLangComands[6][6].format(self.text.index(INSERT).split(".")[0], self.text.index(INSERT).split(".")[1])
        self.statusbarFullText = f"  {self.statusbarFileName:<100s}{self.statusbarLineColumn:<30s}{self.statusbarFont:>40s}"
        self.statusbar.configure(text=self.statusbarFullText)
    # -----------------------------------------------
    # Методы, связанные с работой приложения:

    def __keyPressEvent(self, args):
        """Слот для сигналов клавиатуры (нужен в ситуациях, когда
           может быть нажата буква в русской раскладке)"""

        # Проверка по коду нажатой клавиши:
        if args.keycode == 65:
            # Если нажата клавиша A (Ф), то вызывается слот для возврата действия текстового поля:
            self._redo()
        elif args.keycode == 66:
            # Если нажата клавиша B (И), то вызывается слот для копирования всего текста текстового поля:
            self._copyAll()
        elif args.keycode == 67:
            # Если нажата клавиша C (С), то вызывается слот для копирования выделенного текста:
            self._copy()
        elif args.keycode == 68:
            # Если нажата клавиша D (В), то вызывается слот для сохранения файла как нового:
            self.__saveAsFile()
        elif args.keycode == 80:
            # Если нажата клавиша P (З), то вызывается слот для печати текста:
            self.__printText()
        elif args.keycode == 83:
            # Если нажата клавиша S (Ы), то вызывается слот для сохранения файла:
            self.__saveFile()
        elif args.keycode == 84:
            # Если нажата клавиша T (Е), то вызывается слот для создания нового файла:
            self.__createFile()
        elif args.keycode == 85:
            # Если нажата клавиша U (Г), то вызывается слот для открытия файла:
            self.__openFile()
        elif args.keycode == 86:
            # Если нажата клавиша V (М), то вызывается слот для вставки текста:
            self._paste()
        elif args.keycode == 88:
            # Если нажата клавиша X (Ч), то вызывается слот для вставки текста:
            self._cut()
        elif args.keycode == 90:
            # Если нажата клавиша Z (Я), то вызывается слот для отмены действия текстового поля:
            self._undo()

    def __exit(self, *args, **kwargs):
        """Метод-протокол для выхода из приложения"""

        # Сохранение предыдущего файла:
        if self.__differentFileSaving():
            # Обновление приложения и закрытие главного окна:
            self.update()
            self.destroy()

    def __escapeExit(self, *args, **kwargs):
        """Метод для выхода из программы через кнопки Escape и F4"""

        # Открытие диалогового окна:
        toQuit = askyesno(self.selectedLangComands[7][0], self.selectedLangComands[7][1])
        if toQuit:
            # Если пользователь хочет выйти из программы, то вызывается основной метод закрытия окна:
            self.__exit()

    def show(self, *args, **kwargs):
        """Метод для отображения приложения"""

        # Обновление приложения и его отображение:
        self.update()
        self.mainloop()


# Отображение главного окна текстового редактора:
if __name__ == '__main__':
    # Создание объекта класса приложения и отображение его главного окна:
    app = Application()
    app.show()
