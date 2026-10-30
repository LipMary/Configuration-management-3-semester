import sys

def main():
    vfs_name = "my_virtual_vfs"
    print("Эмулятор командной строки запущен. Для выхода введите 'exit'.")
    
    while True:
        try:
            user_input = input(f"{vfs_name}> ").strip()
            if not user_input:
                continue
                
            input_parts = user_input.split()
            command = input_parts[0]
            arguments = input_parts[1:]
            
            if command == "exit":
                print("Выход из эмулятора.")
                break
            elif command == "ls":
                print(f"[Заглушка] Вызвана команда: {command}")
                print(f"[Заглушка] Переданные аргументы: {arguments}")
            elif command == "cd":
                print(f"[Заглушка] Вызвана команда: {command}")
                print(f"[Заглушка] Переданные аргументы: {arguments}")
            else:
                print(f"{command}: команда не найдена")
                
        except (KeyboardInterrupt, EOFError):
            print("\nВыход из эмулятора.")
            break

if __name__ == "__main__":
    main()
