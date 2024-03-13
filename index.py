import psycopg

try :
    conn = psycopg.connect("dbname=mydb user=myuser host=localhost")
except psycopg.operationalError as e:
    print(f"Error: {e}")
    exit(1)
