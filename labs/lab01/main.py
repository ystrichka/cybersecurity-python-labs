import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from labs.lab01.task1 import task1
from labs.lab01.task2 import task2
from labs.lab01.task3 import task3
from shared.student import GROUP_NAME, STUDENT_NAME, VARIANT_NUMBER

print(f"{STUDENT_NAME} ({GROUP_NAME}), варіант {VARIANT_NUMBER}")


def main():
    task1()
    task2()
    task3()


if __name__ == "__main__":
    main()
