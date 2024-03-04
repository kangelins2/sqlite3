import sqlite3
from random import choice, randint, shuffle

SKILLS = ['python', 'sql', 'git', 'django']
NAMES = ['Саша', 'Петя', 'Вова', 'Егор']
AGES = [18, 17, 15, 23]
WORK_EXPERIENCES = [3, 6, 8, 4]
START_WORKS = ['20.05.2021', '3.03.2018', '9.04.2016', '5.06.2007']

def create_tables(conn: sqlite3.Connection) -> None:
    cur = conn.cursor()
    create_person = """
    CREATE TABLE IF NOT EXISTS person (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name VARCHAR(30) NOT NULL,
    age INTEGER NOT NULL,
    work_experience INTEGER NOT NULL,
    start_work  VARCHAR(30) NOT NULL
    )
    """
    create_skills = """
    CREATE TABLE IF NOT EXISTS skill (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    name VARCHAR(30)
    )
    """
    create_link = """
    CREATE TABLE IF NOT EXISTS person_skill_link (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
    person_id INTEGER REFERENCES person(id),
    skill_id INTEGER REFERENCES skill(id)
    )
    """
    cur.execute(create_person)
    cur.execute(create_skills)
    cur.execute(create_link)
    conn.commit()


def insert_values(conn: sqlite3.Connection):
    cur = conn.cursor()
    for skill in SKILLS:
        insert_skills = """
        INSERT INTO skill (name)
        VALUES (?)
        """
        cur.execute(insert_skills, (skill,))
    skills_ids = list(range(1, len(SKILLS) + 1))
    for person_id in range(1, 3):
        name = choice(NAMES)
        age = choice(AGES)
        work_experience = choice(WORK_EXPERIENCES)
        start_work = choice(START_WORKS)
        insert_person = """
        INSERT INTO person (name, age, work_experience, start_work)
        VALUES (?, ?, ?, ?)
        """
        cur.execute(insert_person, (name, age, work_experience, start_work))
        insert_link = """
        INSERT INTO person_skill_link (person_id, skill_id)
        VALUES (?, ?)
        """
        count_skills = randint(2, 4)
        shuffle(skills_ids)
        for i in range(count_skills):
            skill_id = skills_ids[i]
            cur.execute(insert_link, (person_id, skill_id))
        conn.commit()


with sqlite3.connect('db.sqlite3') as conn:
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS person")
    cur.execute("DROP TABLE IF EXISTS skill")
    cur.execute("DROP TABLE IF EXISTS person_skill_link")
    create_tables(conn)
    insert_values(conn)
    conn.commit()