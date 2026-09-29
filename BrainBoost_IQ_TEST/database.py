import sqlite3
import hashlib

def hash_password(password):

    return hashlib.sha256(
        password.encode()
    ).hexdigest()


def create_tables():

    conn = sqlite3.connect("iq_test.db")
    cursor = conn.cursor()

    # Users table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Results table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            category TEXT NOT NULL,
            score INTEGER NOT NULL,
            total INTEGER NOT NULL,
            percentage REAL NOT NULL,
            test_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Questions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS questions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            question TEXT NOT NULL,
            option1 TEXT NOT NULL,
            option2 TEXT NOT NULL,
            option3 TEXT NOT NULL,
            option4 TEXT NOT NULL,
            answer TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


def register_user(name, username, password):

    conn = sqlite3.connect("iq_test.db")
    cursor = conn.cursor()

    try:

        hashed_password = hash_password(password)

        cursor.execute("""
            INSERT INTO users (name, username, password)
            VALUES (?, ?, ?)
        """, (name, username, hashed_password))

        conn.commit()

        return True

    except sqlite3.IntegrityError:

        return False

    finally:

        conn.close()


def login_user(username, password):

    conn = sqlite3.connect("iq_test.db")
    cursor = conn.cursor()

    # First check for the username
    cursor.execute("""
        SELECT *
        FROM users
        WHERE username = ?
    """, (username,))

    user = cursor.fetchone()

    if user is None:

        conn.close()
        return None

    stored_password = user[3]

    # Hash the password entered by the user
    hashed_password = hash_password(password)

    # ------------------------------------------
    # NEW HASHED PASSWORD
    # ------------------------------------------

    if stored_password == hashed_password:

        conn.close()
        return user

    # ------------------------------------------
    # OLD PLAIN-TEXT PASSWORD
    # ------------------------------------------

    if stored_password == password:

        # Convert old password to hash
        cursor.execute("""
            UPDATE users
            SET password = ?
            WHERE username = ?
        """, (
            hashed_password,
            username
        ))

        conn.commit()

        conn.close()

        return user

    conn.close()

    return None


def save_result(username, category, score, total, percentage):

    conn = sqlite3.connect("iq_test.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO results
        (username, category, score, total, percentage)
        VALUES (?, ?, ?, ?, ?)
    """, (
        username,
        category,
        score,
        total,
        percentage
    ))

    conn.commit()
    conn.close()


def get_results(username):

    conn = sqlite3.connect("iq_test.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT category, score, total, percentage, test_date
        FROM results
        WHERE username = ?
        ORDER BY id DESC
    """, (username,))

    results = cursor.fetchall()

    conn.close()

    return results

def add_question(
    category,
    question,
    option1,
    option2,
    option3,
    option4,
    answer
):

    conn = sqlite3.connect("iq_test.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO questions
        (
            category,
            question,
            option1,
            option2,
            option3,
            option4,
            answer
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        category,
        question,
        option1,
        option2,
        option3,
        option4,
        answer
    ))

    conn.commit()
    conn.close()


def get_all_questions():

    conn = sqlite3.connect("iq_test.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM questions
        ORDER BY id DESC
    """)

    questions = cursor.fetchall()

    conn.close()

    return questions


def delete_question(question_id):

    conn = sqlite3.connect("iq_test.db")
    cursor = conn.cursor()

    cursor.execute("""
        DELETE FROM questions
        WHERE id = ?
    """, (question_id,))

    conn.commit()
    conn.close()

def get_questions_by_category(category):

    conn = sqlite3.connect("iq_test.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, question, option1, option2, option3, option4, answer
        FROM questions
        WHERE category = ?
        ORDER BY id
    """, (category,))

    questions = cursor.fetchall()

    conn.close()

    return questions

def get_total_users():

    conn = sqlite3.connect("iq_test.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM users
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total


def get_total_questions():

    conn = sqlite3.connect("iq_test.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM questions
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total


def get_total_tests():

    conn = sqlite3.connect("iq_test.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM results
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total


def get_average_score():

    conn = sqlite3.connect("iq_test.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT AVG(percentage)
        FROM results
    """)

    average = cursor.fetchone()[0]

    conn.close()

    if average is None:
        return 0

    return average

def get_all_results():

    conn = sqlite3.connect("iq_test.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT username, category, score, total, percentage, test_date
        FROM results
        ORDER BY id DESC
    """)

    results = cursor.fetchall()

    conn.close()

    return results

def update_question(
    question_id,
    category,
    question,
    option1,
    option2,
    option3,
    option4,
    answer
):

    conn = sqlite3.connect("iq_test.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE questions
        SET category = ?,
            question = ?,
            option1 = ?,
            option2 = ?,
            option3 = ?,
            option4 = ?,
            answer = ?
        WHERE id = ?
    """, (
        category,
        question,
        option1,
        option2,
        option3,
        option4,
        answer,
        question_id
    ))

    conn.commit()
    conn.close()

def get_all_users():

    conn = sqlite3.connect("iq_test.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, username
        FROM users
        ORDER BY id DESC
    """)

    users = cursor.fetchall()

    conn.close()

    return users

def get_user_results(username):

    conn = sqlite3.connect("iq_test.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT category, score, total, percentage, test_date
        FROM results
        WHERE username = ?
        ORDER BY id DESC
    """, (username,))

    results = cursor.fetchall()

    conn.close()

    return results

def update_user_name(username, new_name):

    conn = sqlite3.connect("iq_test.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET name = ?
        WHERE username = ?
    """, (new_name, username))

    conn.commit()
    conn.close()

def update_user_password(username, new_password):

    conn = sqlite3.connect("iq_test.db")
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE users
        SET password = ?
        WHERE username = ?
    """, (new_password, username))

    conn.commit()
    conn.close()

def validate_password(password):

    if len(password) < 6:
        return False, "Password must be at least 6 characters."

    if not any(char.isdigit() for char in password):
        return False, "Password must contain at least one number."

    return True, ""

def validate_user_details(name, username):

    name = name.strip()
    username = username.strip()

    if len(name) < 2:
        return False, "Name must contain at least 2 characters."

    if not name.replace(" ", "").isalpha():
        return False, "Name should contain letters only."

    if len(username) < 3:
        return False, "Username must contain at least 3 characters."

    if " " in username:
        return False, "Username cannot contain spaces."

    return True, ""