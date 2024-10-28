import datetime as dt
import glob
import json
import os
import string
import pandas as pd
import random

from faker import Faker

from utils import add_password

DATA_FOLDER = "data"

files = glob.glob(os.path.join(DATA_FOLDER, "*"))
for f in files:
    os.remove(f)

fake = Faker()

headers = [
    "Student ID",
    "Test Name",
    "Gender",
    "Version",
    "Level",
    "Test Date",
    "Standardised Score",
]
extra_headers = {
    "DOB": "date_of_birth",
    "Name": "name",
    "Nationality": "nationality",
    "Email": "email",
}
tests = ["Maths", "English", "Science", "Overall"]
student_ids = list(
    set([random.randint(100000000000, 999999999999) for _ in range(0, 3000)])
)
passwords = {}
for i in range(50):
    ### New file

    lowercase_headers = bool(random.randint(0, 1))
    mangle_id = bool(random.randint(0, 2))
    date_version = random.randint(1, 2)

    # Pick a random extra column
    extra_header = random.choice(list(extra_headers.items()))

    headers.append(extra_header[0])

    test = random.choice(tests)
    level = random.randint(4, 12)
    date = dt.datetime(
        year=random.randint(2010, 2024),
        month=random.randint(1, 12),
        day=random.randint(1, 28),
    )
    if date_version == 1:
        date = str(date)
    else:
        date = str(date.strftime(format="%Y-%m-%d"))
    rows = []
    for j in range(1000):
        data = ""
        student_id = random.choice(student_ids)
        gender = fake.passport_gender()
        score = sum(map(int, str(student_id).strip())) % 60 + 80 + random.randint(1, 7)

        if test == "Maths":
            score += random.randint(1, 2)
        elif test == "English":
            score += 4
        elif test == "Science":
            score += random.randint(-5, 5)
        if random.randint(1, 100) == 100:
            score = None
        if mangle_id:
            student_id = str(student_id)[:11]
        if extra_header[1] == "name":
            data = str(" " * random.randrange(0, 3)) + fake.unique.name()
        elif extra_header[1] == "date_of_birth":
            data = fake.date_of_birth(minimum_age=5, maximum_age=25)
        elif extra_header[1] == "email":
            data = fake.email()

        rows.append(
            [
                student_id,
                test,
                gender,
                f"V{random.randint(1,3)}",
                level,
                date,
                score,
                data,
            ]
        )
    df = pd.DataFrame(columns=headers, data=rows)
    if lowercase_headers:
        df.columns = df.columns.str.lower()

    random_file = random.randint(1, 2)
    filename = "".join(
        random.choices(string.ascii_uppercase + string.digits, k=random.randint(3, 10))
    )

    if random_file == 1:
        df.to_csv(os.path.join(DATA_FOLDER, filename + ".csv"), index=False)
    elif random_file == 2:
        full_filename = filename + ".xlsx"
        file_path = os.path.join(DATA_FOLDER, full_filename)
        df.to_excel(file_path, index=False)
        if random.randint(1, 5) == 5:
            new_filename = add_password(file_path, filename)
            passwords[new_filename] = filename

    headers.remove(extra_header[0])


with open(os.path.join(DATA_FOLDER, "passwords.txt"), "w") as p:
    p.writelines(json.dumps(passwords))
