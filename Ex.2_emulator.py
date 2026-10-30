import sys
import os

def execute_command(user_input, vfs_name):
    """
    Функция обработки команд. 
    Берет строку команды, разбивает её и проверяет.
    Если возвращает False — эмулятор должен завершить работу.
    """
    user_input = user_input.strip()
    if not user_input:
        return True
        
    input_parts = user_input.split()
    command = input_parts[0] 
    arguments = input_parts[1:]
    
    if command == "exit":
        print("Выход из эмулятора.")
        return False
    elif command == "ls":
        print(f"[Заглушка] Вызвана команда: {command}")
        print(f"[Заглушка] Переданные аргументы: {arguments}")
    elif command == "cd":
        print(f"[Заглушка] Вызвана команда: {command}")
        print(f"[Заглушка] Переданные аргументы: {arguments}")
    else:
        print(f"{command}: команда не найдена")
        
    return True

def main():
    # Проверка кол-во аргументов командной строки в sys.argv.
    # 3 элемента: [0] имя скрипта, [1] путь к vfs, [2] путь к скрипту
    if len(sys.argv) < 3:
        print("Ошибка: Недостаточно аргументов при запуске!")
        print("Использование: python3 emulator.py <путь_к_vfs.csv> <путь_к_стартовому_скрипту.txt>")
        return

    # Запись переданных параметров в переменные
    vfs_path = sys.argv[1]
    script_path = sys.argv[2]
    
    # Берем только финальное имя файла из пути
    vfs_name = os.path.basename(vfs_path)

    print(f"Эмулятор запущен. Настройки:")
    print(f" -> Путь к VFS: {vfs_path}")
    print(f" -> Стартовый скрипт: {script_path}\n")

    # Чтение и автоматическое выполнение команд
    if os.path.exists(script_path):
        print("--- Выполнение стартового скрипта ---")
        with open(script_path, "r", encoding="utf-8") as f:
            for line in f.readlines():
                # .rstrip("\n") убирает скрытый перенос строки в конце текстового файла
                clean_line = line.rstrip("\n")
                
                # Показываем строку, как будто пользователь вводит её сам
                print(f"{vfs_name}> {clean_line}")
                
                # Передаем команду на выполнение
                if not execute_command(clean_line, vfs_name):
                    return
        print("--- Стартовый скрипт успешно выполнен ---\n")
    else:
        print(f"Ошибка: Стартовый скрипт по пути '{script_path}' не найден.\n")

    # Переход в интерактивный режим REPL для пользователя
    while True:
        try:
            user_input = input(f"{vfs_name}> ")
            if not execute_command(user_input, vfs_name):
                break
        except (KeyboardInterrupt, EOFError):
            print("\nВыход из эмулятора.")
            break

if __name__ == "__main__":
    main()
  
