import csv
import functools
import hashlib
import json
import os
import sys
from datetime import datetime

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from shared.student import GROUP_NAME, STUDENT_NAME, VARIANT_NUMBER


def task3():
    print("Завдання 3")
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    DATA_DIR = os.path.join(CURRENT_DIR, "data")
    USERS_CSV_PATH = os.path.join(DATA_DIR, "users.csv")
    LOG_JSON_PATH = os.path.join(DATA_DIR, "log.json")

    MIN_PASSWORD_LENGTH = 8
    HASH_ALGORITHM = "md5"

    SALT = str(VARIANT_NUMBER).zfill(5)

    class ValidationError(Exception):
        pass

    def generate_hash(password, salt):
        if not password or not salt:
            raise ValidationError("Пароль та сіль не можуть бути порожніми")

        if len(password) < MIN_PASSWORD_LENGTH:
            raise ValidationError(
                f"Пароль закороткий. Мінімальна довжина паролю: {MIN_PASSWORD_LENGTH}"
            )

        salt_data = (password + salt).encode("utf_8")
        return hashlib.md5(salt_data).hexdigest()

    def log_event(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            username = args[0] if len(args) > 0 else kwargs.get("username", "unknown")

            result = "fail"
            try:
                success = func(*args, **kwargs)
                if success:
                    result = "success"
                return success
            except Exception:
                result = "fail"
                raise
            finally:
                log_record = {
                    "event": "login",
                    "user": username,
                    "result": result,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "args": [arg for arg in args],
                    "kwargs": {k: v for k, v in kwargs.items() if k != "password"},
                }

                try:
                    os.makedirs(DATA_DIR, exist_ok=True)
                    existing_logs = []
                    if os.path.exists(LOG_JSON_PATH) and os.path.getsize(LOG_JSON_PATH) > 0:
                        with open(LOG_JSON_PATH, mode="r", encoding="utf_8") as jf:
                            try:
                                existing_logs = json.load(jf)
                                if not isinstance(existing_logs, list):
                                    existing_logs = []
                            except json.decoder.JSONDecodeError:
                                existing_logs = []

                    existing_logs.append(log_record)
                    with open(LOG_JSON_PATH, mode="w", encoding="utf_8") as jf:
                        json.dump(
                            existing_logs, jf, ensure_ascii=False, indent=4
                        )

                except (OSError, PermissionError) as log_error:
                    print(log_error)

        return wrapper

    def create_user(username, password):
        pwd_hash = generate_hash(password, SALT)
        return username, pwd_hash

    def create_users(users_list):
        os.makedirs(DATA_DIR, exist_ok=True)

        with open(USERS_CSV_PATH, mode="w", encoding="utf_8") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["username", "password_hash"])
            for username, password in users_list:
                u_name, pass_hash = create_user(username, password)
                writer.writerow([u_name, pass_hash])

    def read_users():
        users_list = []
        with open(USERS_CSV_PATH, mode="r", encoding="utf_8") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                users_list.append(row)
        return users_list

    @log_event
    def login(username, password, users_list):
        if not username or not password:
            raise ValueError("Ім'я користувача та пароль не можуть бути порожніми.")

        input_hash = generate_hash(password, salt=SALT)

        for user_entry in users_list:
            if user_entry["username"] == username:
                return user_entry["password_hash"] == input_hash

        return False

    users_to_register = (
        ("user_1", "Black_ha20lo21"),
        ("user_2", "every22_20Machine"),
        ("user_3", "NuLL_45Set"),
        ("user_4", "white_38Flowers"),
        ("user_5", "Saint4_6destroyer"),
        ("user_6", "sIlent_28coLLisions"),
        ("user_7", "Hymn!for328Droids"),
        ("user_8", "6miRacle&mIlk2"),
        ("user_9", "U3_do_1t1!weLL"),
        ("user_10", "co11apse&the323Speed"),
    )
    print("-" * 70)
    print(f"Студент: {STUDENT_NAME} ({GROUP_NAME}) | Варіант: {VARIANT_NUMBER}")

    try:
        create_users(users_to_register)

        print("База даних користувачів")
        users_list = read_users()
        print(f"{'№':<3} | {'Username':<18} | {'Hashed password':<34}")
        print("-" * 70)
        for i, entry in enumerate(users_list, 1):
            print(f"{i:<3} | {entry['username']:<18} | {entry['password_hash']:<34}")

        print("Автентифікація користувачів")
        test_cases = [
            ("user_10", "co11apse&the323Speed", "Правильний логін і пароль"),
            ("user_12", "WrongPassword1", "Неправильний пароль"),
            ("unknown_user", "SomeSecret123", "Неіснуючий користувач"),
        ]

        for u_name, pwd, description in test_cases:
            is_auth = login(u_name, pwd, users_list=users_list)
            status = "success" if is_auth else "fail"
            print(f"({description}): user = '{u_name}' -> {status}")
    except (OSError, FileNotFoundError, PermissionError) as file_error:
        print(file_error)
    except (ValidationError, ValueError) as val_error:
        print(val_error)
    except Exception as error:
        print(error)


if __name__ == "__main__":
    task3()
