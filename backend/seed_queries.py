import requests
import random
import time

# Backend API endpoint
API_BASE = "http://localhost:8000"

# Predefined users
USER_ID = 1

# Common SQL patterns
operations = ["SELECT", "INSERT", "UPDATE", "DELETE"]
tables = ["users", "employees", "transactions", "orders", "products", "admin_users"]

select_templates = [
    "SELECT * FROM {table} WHERE id = {id};",
    "SELECT name, email FROM {table} WHERE active = TRUE;",
    "SELECT COUNT(*) FROM {table};",
    "SELECT * FROM {table} WHERE created_at > NOW() - INTERVAL '7 days';"
]

insert_templates = [
    "INSERT INTO {table} (name, value) VALUES ('item_{id}', {id});",
    "INSERT INTO {table} (email, role) VALUES ('user{id}@example.com', 'user');"
]

update_templates = [
    "UPDATE {table} SET role='admin' WHERE id={id};",
    "UPDATE {table} SET balance=balance+100 WHERE id={id};",
    "UPDATE {table} SET status='inactive' WHERE last_login < NOW() - INTERVAL '1 year';"
]

delete_templates = [
    "DELETE FROM {table} WHERE id={id};",
    "DELETE FROM {table} WHERE status='inactive';"
]

def random_query():
    op = random.choice(operations)
    table = random.choice(tables)
    id_val = random.randint(1, 50)

    if op == "SELECT":
        query = random.choice(select_templates).format(table=table, id=id_val)
    elif op == "INSERT":
        query = random.choice(insert_templates).format(table=table, id=id_val)
    elif op == "UPDATE":
        query = random.choice(update_templates).format(table=table, id=id_val)
    else:
        query = random.choice(delete_templates).format(table=table, id=id_val)
    return op, query


def add_query(user_id, query_text, operation_type):
    payload = {
        "user_id": user_id,
        "query_text": query_text,
        "operation_type": operation_type
    }
    try:
        response = requests.post(f"{API_BASE}/logs/add", json=payload)
        if response.status_code == 201:
            print(f"✅ Added: {operation_type} -> {query_text}")
        else:
            print(f"❌ Failed: {response.status_code}, {response.text}")
    except Exception as e:
        print(f"Error: {e}")


def main():
    print("🔹 Seeding synthetic query logs...")
    for i in range(15):
        op, query = random_query()
        add_query(USER_ID, query, op)
        time.sleep(0.2)  # avoid overwhelming the API
    print("✅ Seeding complete!")


if __name__ == "__main__":
    main()
