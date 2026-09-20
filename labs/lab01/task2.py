import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))
from shared.student import GROUP_NAME, STUDENT_NAME, VARIANT_NUMBER


def task2():
    print("Завдання 2")

    users = {
        "devsecops_lead": {
            "role": "devsecops",
            "clearance": 4,
            "department": "DevSecOps",
            "active": True,
        },
        "security_engineer": {
            "role": "security_engineer",
            "clearance": 3,
            "department": "Security Engineering",
            "active": True,
        },
        "automation_tech": {
            "role": "automation",
            "clearance": 2,
            "department": "Automation",
            "active": True,
        },
        "api_developer": {
            "role": "api_developer",
            "clearance": 2,
            "department": "API",
            "active": True,
        },
        "sandbox_env": {
            "role": "sandbox",
            "clearance": 1,
            "department": "Testing",
            "active": False,
        },
    }

    resources = [
        ("security_pipelines", 4),
        ("secure_coding_standards", 3),
        ("automation_scripts", 2),
        ("api_specifications", 2),
        ("threat_models", 4),
        ("testing_frameworks", 1),
        ("security_gates", 3),
        ("vulnerability_scans", 4),
        ("integration_tests", 2),
        ("mock_services", 1),
    ]

    security_levels = ("Sandbox", "Development", "Secure", "Production Critical")
    blocked_users = {"sandbox_env", "pipeline_breach", "automation_fail"}

    def get_level(level_num):
        return security_levels[level_num - 1]

    def check_access(username, resource_level):
        if username not in users:
            return "DENY", "User not found"

        if username in blocked_users:
            return "DENY", "User is blocked"

        user_info = users[username]

        if not user_info.get("active", False):
            return "DENY", "User is not active"

        if user_info["clearance"] >= resource_level:
            return "ALLOW", None
        else:
            return "DENY", "Insufficient clearance"

    print(f"{STUDENT_NAME} {GROUP_NAME} {VARIANT_NUMBER}")
    print("-" * 70)
    print(
        f"{'№':<3} | {'Ресурс':<26} | {'Рівень(код)':<13} | {'Рівень(назва)':<20}"
    )
    print("-" * 70)
    for i, (res_name, res_lvl) in enumerate(resources, 1):
        lvl_name = get_level(res_lvl)
        print(f"{i:<3} | {res_name:<26} | {res_lvl:<13} | {lvl_name:<20}")

    for username in users:
        print(f"\n[Користувач: {username}]")
        for res_name, res_lvl in resources:
            status, reason = check_access(username, res_lvl)
            if status == "ALLOW":
                result = "ALLOW"
            else:
                result = f"DENY({reason})"

            print(f"user={username:<18} resource={res_name:<24} -> {result}")

if __name__ == "__main__":
    task2()

