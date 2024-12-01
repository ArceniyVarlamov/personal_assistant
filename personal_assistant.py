import os
import json
import csv
from datetime import datetime

# Установка пути для хранения данных
BASE_DIR = "personal_assistant"
os.makedirs(BASE_DIR, exist_ok=True)


class BaseManager:
    # Базовый класс для работы с JSON
    def __init__(self, file_name):
        self.file_path = os.path.join(BASE_DIR, file_name)
        self.data = self.load_data()

    def load_data(self):
        # Загрузка данных из файла
        if os.path.exists(self.file_path):
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_data(self):
        # Сохранение данных в файл
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(self.data, f, ensure_ascii=False, indent=4)


class NotesManager(BaseManager):
    # Управление заметками
    def __init__(self):
        super().__init__("notes.json")

    def add_note(self, title, content):
        note = {
            "id": int(datetime.now().timestamp()),
            "title": title,
            "content": content,
            "timestamp": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        }
        self.data.append(note)
        self.save_data()

    def view_notes(self):
        for note in self.data:
            print(f"{note['id']} | {note['title']} | {note['timestamp']}")

    def view_note_details(self, note_id):
        for note in self.data:
            if note["id"] == note_id:
                print(f"Заголовок: {note['title']}")
                print(f"Содержание: {note['content']}")
                print(f"Дата: {note['timestamp']}")

    def edit_note(self, note_id, title=None, content=None):
        for note in self.data:
            if note["id"] == note_id:
                if title:
                    note["title"] = title
                if content:
                    note["content"] = content
                note["timestamp"] = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.save_data()

    def delete_note(self, note_id):
        self.data = [note for note in self.data if note["id"] != note_id]
        self.save_data()

    def export_to_csv(self):
        with open(os.path.join(BASE_DIR, "notes_export.csv"), "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Title", "Content", "Timestamp"])
            for note in self.data:
                writer.writerow([note["id"], note["title"], note["content"], note["timestamp"]])

    def import_from_csv(self, file_name):
        with open(file_name, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.data.append({
                    "id": int(row["ID"]),
                    "title": row["Title"],
                    "content": row["Content"],
                    "timestamp": row["Timestamp"]
                })
        self.save_data()


class TaskManager(BaseManager):
    # Управление задачами
    def __init__(self):
        super().__init__("tasks.json")

    def add_task(self, title, description, priority, due_date):
        task = {
            "id": int(datetime.now().timestamp()),
            "title": title,
            "description": description,
            "done": False,
            "priority": priority,
            "due_date": due_date
        }
        self.data.append(task)
        self.save_data()

    def view_tasks(self):
        for task in self.data:
            status = "✔" if task["done"] else "✘"
            print(f"{task['id']} | {task['title']} | {status} | {task['priority']} | {task['due_date']}")

    def mark_done(self, task_id):
        for task in self.data:
            if task["id"] == task_id:
                task["done"] = True
                break
        self.save_data()

    def edit_task(self, task_id, title=None, description=None, priority=None, due_date=None):
        for task in self.data:
            if task["id"] == task_id:
                if title:
                    task["title"] = title
                if description:
                    task["description"] = description
                if priority:
                    task["priority"] = priority
                if due_date:
                    task["due_date"] = due_date
        self.save_data()

    def delete_task(self, task_id):
        self.data = [task for task in self.data if task["id"] != task_id]
        self.save_data()

    def export_to_csv(self):
        with open(os.path.join(BASE_DIR, "tasks_export.csv"), "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Title", "Description", "Done", "Priority", "DueDate"])
            for task in self.data:
                writer.writerow([task["id"], task["title"], task["description"], task["done"], task["priority"], task["due_date"]])

    def import_from_csv(self, file_name):
        with open(file_name, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.data.append({
                    "id": int(row["ID"]),
                    "title": row["Title"],
                    "description": row["Description"],
                    "done": row["Done"].lower() == "true",
                    "priority": row["Priority"],
                    "due_date": row["DueDate"]
                })
        self.save_data()


class ContactsManager(BaseManager):
    # Управление контактами
    def __init__(self):
        super().__init__("contacts.json")

    def add_contact(self, name, phone, email):
        contact = {
            "id": int(datetime.now().timestamp()),
            "name": name,
            "phone": phone,
            "email": email
        }
        self.data.append(contact)
        self.save_data()

    def view_contacts(self):
        for contact in self.data:
            print(f"{contact['id']} | {contact['name']} | {contact['phone']} | {contact['email']}")

    def search_contact(self, query):
        for contact in self.data:
            if query in contact["name"] or query in contact["phone"]:
                print(f"{contact['id']} | {contact['name']} | {contact['phone']} | {contact['email']}")

    def edit_contact(self, contact_id, name=None, phone=None, email=None):
        for contact in self.data:
            if contact["id"] == contact_id:
                if name:
                    contact["name"] = name
                if phone:
                    contact["phone"] = phone
                if email:
                    contact["email"] = email
        self.save_data()

    def delete_contact(self, contact_id):
        self.data = [contact for contact in self.data if contact["id"] != contact_id]
        self.save_data()

    def export_to_csv(self):
        with open(os.path.join(BASE_DIR, "contacts_export.csv"), "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Name", "Phone", "Email"])
            for contact in self.data:
                writer.writerow([contact["id"], contact["name"], contact["phone"], contact["email"]])

    def import_from_csv(self, file_name):
        with open(file_name, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.data.append({
                    "id": int(row["ID"]),
                    "name": row["Name"],
                    "phone": row["Phone"],
                    "email": row["Email"]
                })
        self.save_data()


class FinanceManager(BaseManager):
    # Управление финансами
    def __init__(self):
        super().__init__("finance.json")

    def add_record(self, amount, category, date, description):
        record = {
            "id": int(datetime.now().timestamp()),
            "amount": amount,
            "category": category,
            "date": date,
            "description": description
        }
        self.data.append(record)
        self.save_data()

    def view_records(self):
        for record in self.data:
            print(f"{record['id']} | {record['amount']} | {record['category']} | {record['date']} | {record['description']}")

    def filter_records(self, start_date, end_date=None, category=None):
        filtered = [rec for rec in self.data if rec["date"] >= start_date]
        if end_date:
            filtered = [rec for rec in filtered if rec["date"] <= end_date]
        if category:
            filtered = [rec for rec in filtered if rec["category"] == category]
        for record in filtered:
            print(f"{record['id']} | {record['amount']} | {record['category']} | {record['date']} | {record['description']}")

    def generate_report(self, start_date, end_date):
        report = [rec for rec in self.data if start_date <= rec["date"] <= end_date]
        income = sum(rec["amount"] for rec in report if rec["amount"] > 0)
        expense = sum(abs(rec["amount"]) for rec in report if rec["amount"] < 0)
        print(f"Доход: {income}, Расход: {expense}, Баланс: {income - expense}")

    def export_to_csv(self):
        with open(os.path.join(BASE_DIR, "finance_export.csv"), "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["ID", "Amount", "Category", "Date", "Description"])
            for record in self.data:
                writer.writerow([record["id"], record["amount"], record["category"], record["date"], record["description"]])

    def import_from_csv(self, file_name):
        with open(file_name, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                self.data.append({
                    "id": int(row["ID"]),
                    "amount": float(row["Amount"]),
                    "category": row["Category"],
                    "date": row["Date"],
                    "description": row["Description"]
                })
        self.save_data()


class Calculator:
    # Калькулятор
    @staticmethod
    def calculate(expression):
        try:
            result = eval(expression)
            print(f"Результат: {result}")
        except ZeroDivisionError:
            print("Ошибка: деление на ноль.")
        except Exception as e:
            print(f"Ошибка: {e}")


class PersonalAssistant:
    # Главное приложение
    def __init__(self):
        self.notes_manager = NotesManager()
        self.task_manager = TaskManager()
        self.contacts_manager = ContactsManager()
        self.finance_manager = FinanceManager()

    def run(self):
        while True:
            print("\nДобро пожаловать в Персональный помощник!")
            print("  Выберите действие:")
            print("  1. Управление заметками")
            print("  2. Управление задачами")
            print("  3. Управление контактами")
            print("  4. Управление финансовыми записями")
            print("  5. Калькулятор")
            print("  6. Выход")
            choice = input("Ваш выбор: ")
            if choice == "1":
                self.manage_notes()
            elif choice == "2":
                self.manage_tasks()
            elif choice == "3":
                self.manage_contacts()
            elif choice == "4":
                self.manage_finances()
            elif choice == "5":
                self.use_calculator()
            elif choice == "6":
                print("До свидания!")
                break
            else:
                print("Неверный выбор.")

    def manage_notes(self):
        while True:
            print("\nУправление заметками:")
            print("  1. Добавить заметку")
            print("  2. Просмотреть заметки")
            print("  3. Просмотреть подробности заметки")
            print("  4. Редактировать заметку")
            print("  5. Удалить заметку")
            print("  6. Экспорт в CSV")
            print("  7. Импорт из CSV")
            print("  8. Назад")
            choice = input("Ваш выбор: ")
            if choice == "1":
                title = input("Заголовок: ")
                content = input("Содержание: ")
                self.notes_manager.add_note(title, content)
            elif choice == "2":
                self.notes_manager.view_notes()
            elif choice == "3":
                note_id = int(input("Введите ID заметки: "))
                self.notes_manager.view_note_details(note_id)
            elif choice == "4":
                note_id = int(input("Введите ID заметки: "))
                title = input("Новый заголовок (оставьте пустым для пропуска): ")
                content = input("Новое содержание (оставьте пустым для пропуска): ")
                self.notes_manager.edit_note(note_id, title, content)
            elif choice == "5":
                note_id = int(input("Введите ID заметки: "))
                self.notes_manager.delete_note(note_id)
            elif choice == "6":
                self.notes_manager.export_to_csv()
            elif choice == "7":
                file_name = input("Введите имя файла: ")
                self.notes_manager.import_from_csv(file_name)
            elif choice == "8":
                break

    def manage_tasks(self):
        while True:
            print("\nУправление задачами:")
            print("  1. Добавить задачу")
            print("  2. Просмотреть задачи")
            print("  3. Отметить задачу как выполненную")
            print("  4. Редактировать задачу")
            print("  5. Удалить задачу")
            print("  6. Экспорт в CSV")
            print("  7. Импорт из CSV")
            print("  8. Назад")
            choice = input("Ваш выбор: ")
            if choice == "1":
                title = input("Название задачи: ")
                description = input("Описание задачи: ")
                priority = input("Приоритет (Высокий/Средний/Низкий): ")
                due_date = input("Срок выполнения (ДД-ММ-ГГГГ): ")
                self.task_manager.add_task(title, description, priority, due_date)
            elif choice == "2":
                self.task_manager.view_tasks()
            elif choice == "3":
                task_id = int(input("Введите ID задачи: "))
                self.task_manager.mark_done(task_id)
            elif choice == "4":
                task_id = int(input("Введите ID задачи: "))
                title = input("Новое название (оставьте пустым для пропуска): ")
                description = input("Новое описание (оставьте пустым для пропуска): ")
                priority = input("Новый приоритет (оставьте пустым для пропуска): ")
                due_date = input("Новая дата (оставьте пустым для пропуска): ")
                self.task_manager.edit_task(task_id, title, description, priority, due_date)
            elif choice == "5":
                task_id = int(input("Введите ID задачи: "))
                self.task_manager.delete_task(task_id)
            elif choice == "6":
                self.task_manager.export_to_csv()
            elif choice == "7":
                file_name = input("Введите имя файла: ")
                self.task_manager.import_from_csv(file_name)
            elif choice == "8":
                break

    def manage_contacts(self):
        while True:
            print("\nУправление контактами:")
            print("  1. Добавить контакт")
            print("  2. Просмотреть контакты")
            print("  3. Искать контакт")
            print("  4. Редактировать контакт")
            print("  5. Удалить контакт")
            print("  6. Экспорт в CSV")
            print("  7. Импорт из CSV")
            print("  8. Назад")
            choice = input("Ваш выбор: ")
            if choice == "1":
                name = input("Имя: ")
                phone = input("Телефон: ")
                email = input("Email: ")
                self.contacts_manager.add_contact(name, phone, email)
            elif choice == "2":
                self.contacts_manager.view_contacts()
            elif choice == "3":
                query = input("Введите имя или телефон для поиска: ")
                self.contacts_manager.search_contact(query)
            elif choice == "4":
                contact_id = int(input("Введите ID контакта: "))
                name = input("Новое имя (оставьте пустым для пропуска): ")
                phone = input("Новый телефон (оставьте пустым для пропуска): ")
                email = input("Новый email (оставьте пустым для пропуска): ")
                self.contacts_manager.edit_contact(contact_id, name, phone, email)
            elif choice == "5":
                contact_id = int(input("Введите ID контакта: "))
                self.contacts_manager.delete_contact(contact_id)
            elif choice == "6":
                self.contacts_manager.export_to_csv()
            elif choice == "7":
                file_name = input("Введите имя файла: ")
                self.contacts_manager.import_from_csv(file_name)
            elif choice == "8":
                break

    def manage_finances(self):
        while True:
            print("\nУправление финансовыми записями:")
            print("  1. Добавить запись")
            print("  2. Просмотреть записи")
            print("  3. Фильтровать записи")
            print("  4. Генерация отчета")
            print("  5. Экспорт в CSV")
            print("  6. Импорт из CSV")
            print("  7. Назад")
            choice = input("Ваш выбор: ")
            if choice == "1":
                amount = float(input("Сумма: "))
                category = input("Категория: ")
                date = input("Дата (ДД-ММ-ГГГГ): ")
                description = input("Описание: ")
                self.finance_manager.add_record(amount, category, date, description)
            elif choice == "2":
                self.finance_manager.view_records()
            elif choice == "3":
                start_date = input("Начальная дата (ДД-ММ-ГГГГ): ")
                end_date = input("Конечная дата (опционально): ") or None
                category = input("Категория (опционально): ") or None
                self.finance_manager.filter_records(start_date, end_date, category)
            elif choice == "4":
                start_date = input("Начальная дата (ДД-ММ-ГГГГ): ")
                end_date = input("Конечная дата (ДД-ММ-ГГГГ): ")
                self.finance_manager.generate_report(start_date, end_date)
            elif choice == "5":
                self.finance_manager.export_to_csv()
            elif choice == "6":
                file_name = input("Введите имя файла: ")
                self.finance_manager.import_from_csv(file_name)
            elif choice == "7":
                break

    def use_calculator(self):
        while True:
            print("\nКалькулятор:")
            print("  1. Выполнить расчет")
            print("  2. Назад")
            choice = input("Ваш выбор: ")
            if choice == "1":
                expression = input("Введите выражение: ")
                Calculator.calculate(expression)
            elif choice == "2":
                break

app = PersonalAssistant()
app.run()