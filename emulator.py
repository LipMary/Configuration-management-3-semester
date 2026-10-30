import sys
import os
import csv  # Подключение модуля для работы с CSV-таблицами

# Главные переменные для хранения состояния виртуальной системы
vfs_tree = {}      # Словарь, будет хранить дерево папок в памяти
current_dir = "/"  # Строка, где хранится папка, где сейчас «находится» пользователь

def load_vfs(csv_path):
    """Функция для считывания CSV-файла и построения дерева папок в оперативной памяти."""
    global vfs_tree
    
    if not os.path.exists(csv_path):
        print(f"Ошибка: Файл VFS по пути '{csv_path}' не найден.")
        sys.exit(1)
        
    with open(csv_path, mode="r", encoding="utf-8") as f:
        # csv.DictReader читает строки и делает из них словари по заголовкам (path и name)
        reader = csv.DictReader(f)
        for row in reader:
            path = row["path"].strip()
            name = row["name"].strip()
            
            # Для папки, котопрой нет создаем пустой список элементов
            if path not in vfs_tree:
                vfs_tree[path] = []
            # Добавляем файл-подпапку в список этой папки
            vfs_tree[path].append(name)

def execute_command(user_input, vfs_name):
    """Функция для разбора строки ввода и выполнения реальных команд ls и cd."""
    global current_dir, vfs_tree
    
    user_input = user_input.strip()
    if not user_input:
        return True
        
    input_parts = user_input.split()
    command = input_parts[0]
    arguments = input_parts[1:]
    
    # КОМАНДА EXIT
    if command == "exit":
        print("Выход из эмулятора.")
        return False
        
    # КОМАНДА LS (Настоящая реализация)
    elif command == "ls":
        # Проверка, есть ли текущая директория в виртуальном дереве
        if current_dir in vfs_tree:
            # Склеиваю все элементы папки через два пробела и выводятся на экран
            print("  ".join(vfs_tree[current_dir]))
        else:
            # Если папка пустая или в ней ничего нет
            print("")
            
    # КОМАНДА CD (Настоящая реализация)
    elif command == "cd":
        # Если аргументов нет, возвращаемся в корень "/" (по правилам Linux)
        if not arguments:
            current_dir = "/"
            return True
            
        target = arguments[0] # Имя папки, куда нужно перейти
        
        # Переход в корень
        if target == "/":
            current_dir = "/"
        # Переход на уровень вверх (назад)
        elif target == "..":
            if current_dir != "/":
                current_dir = os.path.dirname(current_dir)
                if not current_dir:
                    current_dir = "/"
        else:
            # Формируется предполагаемый новый путь
            if current_dir == "/":
                potential_dir = f"/{target}"
            else:
                potential_dir = f"{current_dir}/{target}"
                
            # Проверяка, существует ли такая подпапка в системе
            if potential_dir in vfs_tree or (current_dir in vfs_tree and target in vfs_tree[current_dir]):
                current_dir = potential_dir
            else:
                print(f"cd: {target}: Нет такого файла или каталога")
                
    else:
        print(f"{command}: команда не найдена")
        
    return True

def main():
    if len(sys.argv) < 3:
        print("Ошибка: Недостаточно аргументов при запуске!")
        print("Использование: python3 emulator.py <путь_к_vfs.csv> <путь_к_стартовому_скрипту.txt>")
        return

    vfs_path = sys.argv[1]
    script_path = sys.argv[2]
    vfs_name = os.path.basename(vfs_path)

    # Загрузка структуры папок из созданной таблицы vfs.csv
    load_vfs(vfs_path)

    print(f"Эмулятор запущен. Настройки:")
    print(f" -> Путь к VFS: {vfs_path}")
    print(f" -> Стартовый скрипт: {script_path}\n")

    # Выполнение стартового скрипта
    if os.path.exists(script_path):
        print("--- Выполнение стартового скрипта ---")
        with open(script_path, "r", encoding="utf-8") as f:
            for line in f.readlines():
                clean_line = line.rstrip("\n")
                # Реальная текущая папка: vfs.csv:/папка>
                print(f"{vfs_name}:{current_dir}> {clean_line}")
                if not execute_command(clean_line, vfs_name):
                    return
        print("--- Стартовый скрипт успешно выполнен ---\n")
    else:
        print(f"Ошибка: Стартовый скрипт по пути '{script_path}' не найден.\n")

    # Интерактивный режим REPL
    while True:
        try:
            user_input = input(f"{vfs_name}:{current_dir}> ")
            if not execute_command(user_input, vfs_name):
                break
        except (KeyboardInterrupt, EOFError):
            print("\nВыход из эмулятора.")
            break

if __name__ == "__main__":
    main()
