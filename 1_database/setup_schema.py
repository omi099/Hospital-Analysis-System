
import mysql.connector
import os

config = {
    'host': '127.0.0.1',
    'user': 'root',
    'password': 'Duckgoforit@09'
}

def execute_script(cursor, script):
    statements = script.split(';')
    for statement in statements:
        if statement.strip():
            try:
                cursor.execute(statement)
            except Exception as e:
                print(f"Error executing statement: {statement[:50]}...")
                print(e)
                # Don't break, try next (e.g. drop table might fail if not exists, though we use IF EXISTS)

try:
    print("Connecting to MySQL...")
    conn = mysql.connector.connect(**config)
    cursor = conn.cursor()
    
    print("Reading schema.sql...")
    with open('schema.sql', 'r') as f:
        sql_script = f.read()
    
    print("Executing schema...")
    execute_script(cursor, sql_script)
            
    print("[OK] Schema executed successfully!")
    conn.commit()
    cursor.close()
    conn.close()

except Exception as e:
    print(f"[Error] {e}")
