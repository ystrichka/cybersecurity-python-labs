import os
import random
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from shared.student import GROUP_NAME, STUDENT_NAME, VARIANT_NUMBER


def task1():
    print("Завдання 1")
    passwords = [
        "SIEM@An4lysis",
        "easy123",
        "S0C@Analyst",
        "observer",
        "Threat@Hunt1ng",
        "viewer",
        "Incid3nt@Handle",
        "monitor",
        "Log@An4lysis",
        "watcher",
    ]

    criteria = {
        "min_length": 9,
        "require_digits": True,
        "require_upper": True,
        "require_special": True,
    }

    forbidden_passwords = {
        "easy123",
        "observer",
        "viewer",
        "monitor",
        "watcher",
        "admin",
    }

    SPECIAL_CHARS = "!@#$%^&*()-_=+[]{}|;:,.<>?/"

    all_passwords = list(passwords)
    for p in range(3):
        index = random.randint(0, len(all_passwords) - 1)
        all_passwords.append(all_passwords[index])

    def check_password(password):
        if password in forbidden_passwords or len(password) < criteria["min_length"]:
            return "Заборонений"
        has_digit = any(p.isdigit() for p in password)
        has_upper = any(p.isupper() for p in password)
        has_special = any(p in SPECIAL_CHARS for p in password)

        requirements = has_digit and has_upper and has_special
        uniqueness = all_passwords.count(password) == 1

        if requirements and len(password) >= criteria["min_length"] + 4 and uniqueness:
            return "Дуже сильний"

        if requirements:
            return "Сильний"

        if has_digit or has_upper or has_special:
            return "Середній"

        return "Слабкий"

    print(f"{STUDENT_NAME} {GROUP_NAME} {VARIANT_NUMBER}")
    print("-" * 65)
    print(f"{'Пароль':<20} | {'Довжина':<8} | {'Статус':<15}")
    print("-" * 65)

    for password in all_passwords:
        status = check_password(password)
        print(f"{password:<20} | {len(password):<8} | {status:<15}")


if __name__ == "__main__":
    task1()
