import os
from dotenv import load_dotenv
import psycopg2
from psycopg2.extras import RealDictCursor
from models import UserReg, UserLogin, Insert_note, Update_note
from fastapi import Depends, HTTPException
from all_functions import create_hash_pwd

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
# print(DATABASE_URL)



def create_conn():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor(cursor_factory=RealDictCursor)
    return conn, cur

def close_connection(conn, cur):
    
    cur.close()
    conn.close()



def get_by_username(username:str):
    conn, cur = create_conn()
    try:
        cur.execute("""
            SELECT * FROM users WHERE username = %s
            """,(username,))
        
        return cur.fetchone()
    finally:
        close_connection(conn, cur)

def get_by_email(email:str):
    conn, cur = create_conn()
    try:
        cur.execute("""
            SELECT * FROM users WHERE email = %s
            """,(email,))
        
        return cur.fetchone()
    finally:
        close_connection(conn, cur)


def create_user(user:UserReg):
    conn, cur = create_conn()
    
    h_pwd = create_hash_pwd(user.h_pwd)
    try:
        cur.execute("""
                INSERT INTO users(name,username, email, hashed_password)
                VALUES(%s, %s, %s, %s)
                RETURNING id

                """, (user.name,user.username, user.email, h_pwd))

        conn.commit()
        get_id = cur.fetchone()["id"]
        return {"message": "User created", "ID is": get_id}
    finally:
        close_connection(conn, cur)


def insert_note(username: str, note: Insert_note):
    user = get_by_username(username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    conn, cur = create_conn()
    try:
        cur.execute(
            """
            INSERT INTO notes (user_id, title, content)
            VALUES (%s, %s, %s)
            RETURNING id
            """,
            (user["id"], note.title, note.content),
        )
        note_id = cur.fetchone()["id"]
        conn.commit()
        return {"message": "Note created", "id": note_id}
    except Exception:
        conn.rollback()
        raise
    finally:
        close_connection(conn, cur)

def show_notes(username:str):
    user = get_by_username(username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    conn, cur = create_conn()
    try:
        cur.execute(
            """
            SELECT * FROM notes
            WHERE user_id = %s
            """,
            (user["id"],),
        )
        all_notes = cur.fetchall()
        return {"message": f"user is {user["name"]}", "notes": all_notes}
    except Exception:
        conn.rollback()
        raise
    finally:
        close_connection(conn, cur)

def update_notes(username:str, note:Update_note):
    user = get_by_username(username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    conn, cur = create_conn()
    try:
        cur.execute(
            """
            UPDATE notes
            SET title = %s, content = %s, updated_at = NOW()
            WHERE id = %s AND user_id = %s
            RETURNING id, title, content, updated_at
            """,
            (note.title, note.content, note.id, user["id"]),
        )
        conn.commit()
        updated = cur.fetchone()
        return {"message": f"user is {user["name"]}", "notes": updated}
    except Exception:
        conn.rollback()
        raise
    finally:
        close_connection(conn, cur)

def delete_notes(username:str, note_id:int):
    user = get_by_username(username)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    conn, cur = create_conn()
    try:
        cur.execute(
            """
            
            DELETE FROM notes
            WHERE id = %s AND user_id = %s
            RETURNING id
            """,
            (note_id, user["id"]),
        )
        deleted_note = cur.fetchone()

        if deleted_note is None:
            conn.rollback()
            raise HTTPException(status_code=404, detail="Note not found")

        conn.commit()
        return {"message": "Notes Deleted", "id": deleted_note["id"]}
    except Exception:
        conn.rollback()
        raise
    finally:
        close_connection(conn, cur)