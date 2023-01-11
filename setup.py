"""     Проект: Текстовый редактор Notebook          Файл: setup.py
   Здесь содержится код создания компилируемого приложения, для возможности
   открытия текстового редактора как exe-файл. Также, этот файл используется
   для создания msi-установщика программы для её же распространения
   """

# Импорт модулей:
# Импорт функции setup и класса Executable из библиотеки cx_Freeze для создания компилируемого приложения,
# переменной platform из модуля sys для определения платформы системы,
# класса Application из модуля main для работы с данными приложения:
from cx_Freeze import setup, Executable
from sys import platform
from main import Application

# Определение платформы системы (Если платформа - win32, то присваиваем переменной для хранения платформы отдельное значение):
base = None
if platform == "win32":
    base = "Win32GUI"

# Словарь подключаемых файлов (опций):
opts = {"build_exe": {"include_files": ["logo.ico", "serialize.ini", "logotype.png"], "packages": ["tkinter"]}}

# Создание установщика:
setup(name="ТекстPad",
      version=str(Application.version),
      description="Text Editor for saving data into text files",
      author="ArtProGG, JustPythonист Software Ltd.",
      options=opts,
      executables=[Executable("main.py", base=base)],
      icon="logo.ico",
      shortcutDir="ТекстPad",
      shortcutName="ТекстPad")
