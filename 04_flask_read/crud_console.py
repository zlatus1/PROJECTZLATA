
from db import DEFAULT_DB_PATH, delete_task, fetch_all_tasks, initialize_database, insert_task, toggle_task_status


def show_tasks() -> None:
    tasks = fetch_all_tasks()
    if not tasks:
        print("Список пока пуст.")
        return
    for task in tasks:
        state = "выполнена" if task["status"] == "done" else "новая"
        print(f"#{task['id']} [{state}] {task['title']}")


def main() -> None:
    initialize_database(DEFAULT_DB_PATH)
    actions = {
        "1": "Показать задачи",
        "2": "Добавить задачу",
        "3": "Переключить статус",
        "4": "Удалить задачу",
        "0": "Выход",
    }
    while True:
        print("\n" + " | ".join(f"{key} — {value}" for key, value in actions.items()))
        choice = input("Выбери действие: ").strip()
        try:
            if choice == "1":
                show_tasks()
            elif choice == "2":
                title = input("Название задачи: ").strip()
                if not title or len(title) > 160:
                    print("Название должно содержать от 1 до 160 символов.")
                else:
                    print(f"Добавлена задача #{insert_task(title)}.")
            elif choice == "3":
                task_id = int(input("ID задачи: "))
                print("Статус изменён." if toggle_task_status(task_id) else "Задача не найдена.")
            elif choice == "4":
                task_id = int(input("ID задачи: "))
                if input(f"Точно удалить задачу #{task_id}? (y/n): ").strip().lower() != "y":
                    print("Удаление отменено.")
                else:
                    print("Задача удалена." if delete_task(task_id) else "Задача не найдена.")
            elif choice == "0":
                break
            else:
                print("Нет такого пункта меню.")
        except ValueError:
            print("ID должен быть целым числом.")
        except Exception:
            print("Операция не выполнена из-за ошибки базы. Подробности записаны в консольный журнал.")


if __name__ == "__main__":
    main()
