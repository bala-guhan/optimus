import os
import psycopg2
from dotenv import load_dotenv

# Load environment variables (DATABASE_URL)
load_dotenv()

db_url = os.getenv("DATABASE_URL")

alter_sql = """
ALTER TABLE chat_history
ALTER COLUMN thread_id TYPE TEXT;
"""

def alter_table():
    try:
        conn = psycopg2.connect(db_url)
        cur = conn.cursor()
        cur.execute(alter_sql)
        conn.commit()
        print("Column 'message_type' type changed to TEXT successfully!")
        cur.close()
        conn.close()
    except Exception as e:
        print("Error:", e)

if __name__ == "__main__":
    alter_table() 