# transport_access_simple.py
# Simple Transport System (Python + MS Access)
# Tables: tbl_customers, tbl_drivers, tbl_vehicles, tbl_shipments

import pyodbc
from datetime import datetime

DB_PATH = r"C:\Users\ROG\OneDrive\Documents\Database18.accdb"
CONN_STR = r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=" + DB_PATH + ";"

# -------------------------
# 1) CONNECT + BASIC DB HELPERS
# -------------------------
def connect():
    return pyodbc.connect(CONN_STR)

def run(sql, params=()):
    """For INSERT/UPDATE/DELETE"""
    with connect() as conn:
        cur = conn.cursor()
        cur.execute(sql, params)
        conn.commit()

def fetch(sql, params=()):
    """For SELECT"""
    with connect() as conn:
        cur = conn.cursor()
        cur.execute(sql, params)
        return cur.fetchall()

def exists(table, rid):
    rows = fetch(f"SELECT 1 FROM {table} WHERE id=?", (rid,))
    return len(rows) > 0


# -------------------------
# 2) SIMPLE PRINT
# -------------------------
def show(title, rows):
    print("\n" + "="*60)
    print(title)
    print("="*60)
    if not rows:
        print("No data")
        return
    for r in rows:
        print(r)


# -------------------------
# 3) CUSTOMERS (CRUD)
# -------------------------
def customer_menu():
    while True:
        print("\n--- Customers ---")
        print("1) Add  2) View  3) Delete  0) Back")
        ch = input("Choose: ").strip()

        if ch == "1":
            cid = int(input("Customer ID: "))
            if exists("tbl_customers", cid):
                print("ID already exists!")
                continue
            name = input("Name: ")
            phone = input("Phone: ")
            address = input("Address: ")
            run("INSERT INTO tbl_customers (id, [name], phone, address) VALUES (?, ?, ?, ?)",
                (cid, name, phone, address))
            print("✅ Added customer")

        elif ch == "2":
            rows = fetch("SELECT id, [name], phone, address FROM tbl_customers ORDER BY id")
            show("CUSTOMERS", rows)

        elif ch == "3":
            cid = int(input("Customer ID to delete: "))
            run("DELETE FROM tbl_customers WHERE id=?", (cid,))
            print("✅ Deleted customer (if not referenced)")

        elif ch == "0":
            break


# -------------------------
# 4) SHIPMENTS (Create + View Join + Report)
# -------------------------
def shipment_menu():
    while True:
        print("\n--- Shipments ---")
        print("1) Create  2) View (JOIN)  3) Report  0) Back")
        ch = input("Choose: ").strip()

        if ch == "1":
            sid = int(input("Shipment ID: "))
            if exists("tbl_shipments", sid):
                print("Shipment ID exists!")
                continue

            customer_id = int(input("Customer ID: "))
            driver_id = int(input("Driver ID: "))
            vehicle_id = int(input("Vehicle ID: "))
            origin = input("Origin: ")
            destination = input("Destination: ")
            weight = float(input("Weight (kg): "))
            price = float(input("Price ($): "))
            status = "Pending"
            created_at = datetime.now()

            run("""
                INSERT INTO tbl_shipments
                (id, customer_id, driver_id, vehicle_id, origin, destination, weight_kg, price_usd, status, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (sid, customer_id, driver_id, vehicle_id, origin, destination, weight, price, status, created_at))

            print("✅ Shipment created")

        elif ch == "2":
            rows = fetch("""
                SELECT s.id, c.[name], d.[name], v.plate,
                       s.origin, s.destination, s.weight_kg, s.price_usd, s.status, s.created_at
                FROM ((tbl_shipments AS s
                INNER JOIN tbl_customers AS c ON s.customer_id = c.id)
                INNER JOIN tbl_drivers AS d ON s.driver_id = d.id)
                INNER JOIN tbl_vehicles AS v ON s.vehicle_id = v.id
                ORDER BY s.created_at DESC
            """)
            show("SHIPMENTS (JOIN VIEW)", rows)

        elif ch == "3":
            total = fetch("SELECT COUNT(*) FROM tbl_shipments")[0][0]
            delivered = fetch("SELECT COUNT(*) FROM tbl_shipments WHERE status='Delivered'")[0][0]
            income = fetch("SELECT SUM(price_usd) FROM tbl_shipments WHERE status<>'Cancelled'")[0][0] or 0

            print("\n===== REPORT =====")
            print("Total shipments :", total)
            print("Delivered       :", delivered)
            print("Total income($) :", round(income, 2))

        elif ch == "0":
            break


# -------------------------
# 5) MAIN MENU
# -------------------------
def main():
    # Quick connection test
    try:
        connect().close()
        print("✅ Connected to MS Access!")
    except Exception as e:
        print("❌ Connection failed:", e)
        return

    while True:
        print("\n==== TRANSPORT SYSTEM ====")
        print("1) Customers")
        print("2) Shipments")
        print("0) Exit")
        ch = input("Choose: ").strip()

        if ch == "1":
            customer_menu()
        elif ch == "2":
            shipment_menu()
        elif ch == "0":
            print("Bye!")
            break

if __name__ == "__main__":
    main()
