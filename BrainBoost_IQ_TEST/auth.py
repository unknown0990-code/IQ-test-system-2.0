import hashlib
from db_files import get_connection


def hash_password(password):
    """Convert password into a secure hash."""
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(name, username, email, password):
    """Register a new user."""

    connection = get_connection()
    cursor = connection.cursor()

    try:
        hashed_password = hash_password(password)

        cursor.execute("""
            INSERT INTO users (name, username, email, password, role)
            VALUES (?, ?, ?, ?, ?)
        """, (name, username, email, hashed_password, "user"))

        connection.commit()
        return True, "Account created successfully!"

    except Exception as e:
        return False, str(e)

    finally:
        connection.close()


def login_user(username, password):
    """Check username and password."""

    connection = get_connection()
    cursor = connection.cursor()

    hashed_password = hash_password(password)

    cursor.execute("""
        SELECT id, name, username, email, role
        FROM users
        WHERE username = ? AND password = ?
    """, (username, hashed_password))

    user = cursor.fetchone()

    connection.close()

    if user:
        return user

    return None

