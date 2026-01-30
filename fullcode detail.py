# transport_access_full.py
# ✅ Full Transport Company Information System (Python + MS Access)
# ✅ Uses your MS Access file: C:\Users\ROG\OneDrive\Documents\Database 18.accdb
# ✅ Easy to understand, menu-driven, CRUD + shipments + search + report + join view
#
# REQUIREMENTS (Windows):
#   pip install pyodbc
#   Microsoft Access Database Engine installed (bitness must match Python)

import pyodbc
from datetime import datetime


# =========================
# CONFIG (YOUR DATABASE)
# =========================
DB_PATH = r"C:\Users\ROG\OneDrive\Documents\Database18.accdb"

CONN_STR = (
    r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
    rf"DBQ={DB_PATH};"
)


# =========================
# DB UTILITIES
# =========================
def get_conn():
    """Open a connection to MS Access."""
    return pyodbc.connect(CONN_STR)


def test_connection():
    """Test if database connection works."""
    try:
        conn = get_conn()
        conn.close()
        return True, "✅ Connected to MS Access successfully"
    except Exception as e:
        return False, f"❌ Connection failed:\n{e}"


# =========================
# INPUT HELPERS
# =========================
def input_non_empty(prompt: str) -> str:
    while True:
        s = input(prompt).strip()
        if s:
            return s
        print("❌ Cannot be empty")


def input_int(prompt: str) -> int:
    while True:
        try:
            return int(input(prompt).strip())
        except:
            print("❌ Please enter an integer (number)")


def input_float(prompt: str) -> float:
    while True:
        try:
            return float(input(prompt).strip())
        except:
            print("❌ Please enter a number")


# =========================
# PRINT HELPERS
# =========================
def print_table(title: str, headers: list[str], rows: list[tuple]):
    print("\n" + "=" * 100)
    print(title)
    print("=" * 100)
    if not rows:
        print("⚠️ No data")
        print("=" * 100)
        return

    # simple text header
    print(" | ".join(headers))
    print("-" * 100)

    for r in rows:
        print(" | ".join(str(x) for x in r))

    print("=" * 100)


# =========================
# GENERIC DB HELPERS
# =========================
def record_exists(table: str, rid: int) -> bool:
    """Check if ID exists in a specific table."""
    sql = f"SELECT 1 FROM {table} WHERE id=?"
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(sql, (rid,))
        return cur.fetchone() is not None


def safe_execute(sql: str, params: tuple = ()):
    """
    Execute a SQL command safely.
    Returns (True, None) if ok, otherwise (False, error_message).
    """
    try:
        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute(sql, params)
            conn.commit()
        return True, None
    except Exception as e:
        return False, str(e)


def fetch_all(sql: str, params: tuple = ()):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute(sql, params)
        return cur.fetchall()


# =========================
# CUSTOMERS (tbl_customers)
# =========================
def add_customer():
    cid = input_int("Customer ID (number): ")
    if record_exists("tbl_customers", cid):
        print("❌ Customer ID already exists")
        return

    name = input_non_empty("Name: ")
    phone = input_non_empty("Phone: ")
    address = input_non_empty("Address: ")

    ok, err = safe_execute(
        "INSERT INTO tbl_customers (id, [name], phone, address) VALUES (?, ?, ?, ?)",
        (cid, name, phone, address)
    )

    if ok:
        print("✅ Customer added")
    else:
        print("❌ Error adding customer:", err)


def view_customers():
    rows = fetch_all("SELECT id, [name], phone, address FROM tbl_customers ORDER BY id")
    print_table("CUSTOMERS", ["ID", "Name", "Phone", "Address"], rows)


def edit_customer():
    cid = input_int("Enter Customer ID to edit: ")
    if not record_exists("tbl_customers", cid):
        print("❌ Customer not found")
        return

    print("Press Enter to keep old value")
    new_name = input("New Name: ").strip()
    new_phone = input("New Phone: ").strip()
    new_address = input("New Address: ").strip()

    if new_name:
        ok, err = safe_execute("UPDATE tbl_customers SET [name]=? WHERE id=?", (new_name, cid))
        if not ok: print("❌", err)
    if new_phone:
        ok, err = safe_execute("UPDATE tbl_customers SET phone=? WHERE id=?", (new_phone, cid))
        if not ok: print("❌", err)
    if new_address:
        ok, err = safe_execute("UPDATE tbl_customers SET address=? WHERE id=?", (new_address, cid))
        if not ok: print("❌", err)

    print("✅ Customer updated")


def delete_customer():
    cid = input_int("Enter Customer ID to delete: ")
    if not record_exists("tbl_customers", cid):
        print("❌ Customer not found")
        return

    ok, err = safe_execute("DELETE FROM tbl_customers WHERE id=?", (cid,))
    if ok:
        print("✅ Customer deleted")
    else:
        # If references exist, Access may block deletion (good!)
        print("❌ Cannot delete (maybe referenced by shipments).")
        print("Error:", err)


# =========================
# DRIVERS (tbl_drivers)
# =========================
def add_driver():
    did = input_int("Driver ID (number): ")
    if record_exists("tbl_drivers", did):
        print("❌ Driver ID already exists")
        return

    name = input_non_empty("Name: ")
    phone = input_non_empty("Phone: ")
    license_no = input_non_empty("License: ")

    ok, err = safe_execute(
        "INSERT INTO tbl_drivers (id, [name], phone, license) VALUES (?, ?, ?, ?)",
        (did, name, phone, license_no)
    )
    if ok:
        print("✅ Driver added")
    else:
        print("❌ Error adding driver:", err)


def view_drivers():
    rows = fetch_all("SELECT id, [name], phone, license FROM tbl_drivers ORDER BY id")
    print_table("DRIVERS", ["ID", "Name", "Phone", "License"], rows)


def edit_driver():
    did = input_int("Enter Driver ID to edit: ")
    if not record_exists("tbl_drivers", did):
        print("❌ Driver not found")
        return

    print("Press Enter to keep old value")
    new_name = input("New Name: ").strip()
    new_phone = input("New Phone: ").strip()
    new_license = input("New License: ").strip()

    if new_name:
        ok, err = safe_execute("UPDATE tbl_drivers SET [name]=? WHERE id=?", (new_name, did))
        if not ok: print("❌", err)
    if new_phone:
        ok, err = safe_execute("UPDATE tbl_drivers SET phone=? WHERE id=?", (new_phone, did))
        if not ok: print("❌", err)
    if new_license:
        ok, err = safe_execute("UPDATE tbl_drivers SET license=? WHERE id=?", (new_license, did))
        if not ok: print("❌", err)

    print("✅ Driver updated")


def delete_driver():
    did = input_int("Enter Driver ID to delete: ")
    if not record_exists("tbl_drivers", did):
        print("❌ Driver not found")
        return

    ok, err = safe_execute("DELETE FROM tbl_drivers WHERE id=?", (did,))
    if ok:
        print("✅ Driver deleted")
    else:
        print("❌ Cannot delete (maybe referenced by shipments).")
        print("Error:", err)


# =========================
# VEHICLES (tbl_vehicles)
# =========================
def add_vehicle():
    vid = input_int("Vehicle ID (number): ")
    if record_exists("tbl_vehicles", vid):
        print("❌ Vehicle ID already exists")
        return

    plate = input_non_empty("Plate: ")
    vtype = input_non_empty("Vehicle Type: ")
    capacity = input_float("Capacity (kg): ")

    ok, err = safe_execute(
        "INSERT INTO tbl_vehicles (id, plate, vehicles_type, capacity_kg) VALUES (?, ?, ?, ?)",
        (vid, plate, vtype, capacity)
    )
    if ok:
        print("✅ Vehicle added")
    else:
        print("❌ Error adding vehicle:", err)


def view_vehicles():
    rows = fetch_all("SELECT id, plate, vehicles_type, capacity_kg FROM tbl_vehicles ORDER BY id")
    print_table("VEHICLES", ["ID", "Plate", "Type", "Capacity_kg"], rows)


def edit_vehicle():
    vid = input_int("Enter Vehicle ID to edit: ")
    if not record_exists("tbl_vehicles", vid):
        print("❌ Vehicle not found")
        return

    print("Press Enter to keep old value")
    new_plate = input("New Plate: ").strip()
    new_type = input("New Type: ").strip()
    new_cap = input("New Capacity (kg): ").strip()

    if new_plate:
        ok, err = safe_execute("UPDATE tbl_vehicles SET plate=? WHERE id=?", (new_plate, vid))
        if not ok: print("❌", err)
    if new_type:
        ok, err = safe_execute("UPDATE tbl_vehicles SET vehicles_type=? WHERE id=?", (new_type, vid))
        if not ok: print("❌", err)
    if new_cap:
        try:
            cap_val = float(new_cap)
            ok, err = safe_execute("UPDATE tbl_vehicles SET capacity_kg=? WHERE id=?", (cap_val, vid))
            if not ok: print("❌", err)
        except:
            print("⚠️ Invalid capacity, keeping old value")

    print("✅ Vehicle updated")


def delete_vehicle():
    vid = input_int("Enter Vehicle ID to delete: ")
    if not record_exists("tbl_vehicles", vid):
        print("❌ Vehicle not found")
        return

    ok, err = safe_execute("DELETE FROM tbl_vehicles WHERE id=?", (vid,))
    if ok:
        print("✅ Vehicle deleted")
    else:
        print("❌ Cannot delete (maybe referenced by shipments).")
        print("Error:", err)


# =========================
# SHIPMENTS (tbl_shipments)
# =========================
def add_shipment():
    sid = input_int("Shipment ID (number): ")
    if record_exists("tbl_shipments", sid):
        print("❌ Shipment ID already exists")
        return

    customer_id = input_int("Customer ID: ")
    if not record_exists("tbl_customers", customer_id):
        print("❌ Customer ID not found")
        return

    driver_id = input_int("Driver ID: ")
    if not record_exists("tbl_drivers", driver_id):
        print("❌ Driver ID not found")
        return

    vehicle_id = input_int("Vehicle ID: ")
    if not record_exists("tbl_vehicles", vehicle_id):
        print("❌ Vehicle ID not found")
        return

    origin = input_non_empty("From (Origin): ")
    destination = input_non_empty("To (Destination): ")
    weight = input_float("Weight (kg): ")
    price = input_float("Price ($): ")

    print("Status options: 1) Pending  2) In Transit  3) Delivered  4) Cancelled")
    status_choice = input_non_empty("Choose status (1-4): ")
    status_map = {"1": "Pending", "2": "In Transit", "3": "Delivered", "4": "Cancelled"}
    if status_choice not in status_map:
        print("❌ Invalid status")
        return

    status = status_map[status_choice]
    created_at = datetime.now()

    ok, err = safe_execute(
        """
        INSERT INTO tbl_shipments
        (id, customer_id, driver_id, vehicle_id, origin, destination, weight_kg, price_usd, status, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (sid, customer_id, driver_id, vehicle_id, origin, destination, weight, price, status, created_at)
    )

    if ok:
        print("✅ Shipment created")
    else:
        print("❌ Error creating shipment:", err)
        print("💡 If you have FK references enforced, wrong IDs will be blocked automatically.")


def view_shipments_simple():
    rows = fetch_all("""
        SELECT id, customer_id, driver_id, vehicle_id,
               origin, destination, weight_kg, price_usd, status, created_at
        FROM tbl_shipments
        ORDER BY created_at DESC
    """)
    print_table(
        "SHIPMENTS (SIMPLE VIEW)",
        ["ID", "Customer_ID", "Driver_ID", "Vehicle_ID", "From", "To", "Kg", "$", "Status", "Created_At"],
        rows
    )


def view_shipments_join():
    """
    JOIN view: show customer/driver names and vehicle plate (more readable).
    Note: Access JOIN needs parentheses for multiple joins.
    """
    rows = fetch_all("""
        SELECT
            s.id,
            c.[name] AS customer_name,
            d.[name] AS driver_name,
            v.plate AS vehicle_plate,
            s.origin,
            s.destination,
            s.weight_kg,
            s.price_usd,
            s.status,
            s.created_at
        FROM ((tbl_shipments AS s
        INNER JOIN tbl_customers AS c ON s.customer_id = c.id)
        INNER JOIN tbl_drivers AS d ON s.driver_id = d.id)
        INNER JOIN tbl_vehicles AS v ON s.vehicle_id = v.id
        ORDER BY s.created_at DESC
    """)
    print_table(
        "SHIPMENTS (JOIN VIEW)",
        ["ID", "Customer", "Driver", "Plate", "From", "To", "Kg", "$", "Status", "Created_At"],
        rows
    )


def update_shipment_status():
    sid = input_int("Enter Shipment ID: ")
    if not record_exists("tbl_shipments", sid):
        print("❌ Shipment not found")
        return

    print("1) Pending\n2) In Transit\n3) Delivered\n4) Cancelled")
    choice = input_non_empty("Choose new status: ")
    mapping = {"1": "Pending", "2": "In Transit", "3": "Delivered", "4": "Cancelled"}
    if choice not in mapping:
        print("❌ Invalid choice")
        return

    ok, err = safe_execute("UPDATE tbl_shipments SET status=? WHERE id=?", (mapping[choice], sid))
    if ok:
        print("✅ Status updated")
    else:
        print("❌ Error:", err)


def search_shipments():
    print("Search by: 1) Shipment ID  2) Customer ID  3) Driver ID  4) Vehicle ID  5) Status")
    choice = input_non_empty("Choose (1-5): ")

    if choice == "1":
        sid = input_int("Shipment ID: ")
        rows = fetch_all("""
            SELECT id, customer_id, driver_id, vehicle_id, origin, destination, weight_kg, price_usd, status, created_at
            FROM tbl_shipments
            WHERE id=?
        """, (sid,))
    elif choice == "2":
        cid = input_int("Customer ID: ")
        rows = fetch_all("""
            SELECT id, customer_id, driver_id, vehicle_id, origin, destination, weight_kg, price_usd, status, created_at
            FROM tbl_shipments
            WHERE customer_id=?
            ORDER BY created_at DESC
        """, (cid,))
    elif choice == "3":
        did = input_int("Driver ID: ")
        rows = fetch_all("""
            SELECT id, customer_id, driver_id, vehicle_id, origin, destination, weight_kg, price_usd, status, created_at
            FROM tbl_shipments
            WHERE driver_id=?
            ORDER BY created_at DESC
        """, (did,))
    elif choice == "4":
        vid = input_int("Vehicle ID: ")
        rows = fetch_all("""
            SELECT id, customer_id, driver_id, vehicle_id, origin, destination, weight_kg, price_usd, status, created_at
            FROM tbl_shipments
            WHERE vehicle_id=?
            ORDER BY created_at DESC
        """, (vid,))
    elif choice == "5":
        status = input_non_empty("Status (Pending/In Transit/Delivered/Cancelled): ")
        rows = fetch_all("""
            SELECT id, customer_id, driver_id, vehicle_id, origin, destination, weight_kg, price_usd, status, created_at
            FROM tbl_shipments
            WHERE status=?
            ORDER BY created_at DESC
        """, (status,))
    else:
        print("❌ Invalid choice")
        return

    print_table(
        "SHIPMENTS SEARCH RESULTS",
        ["ID", "Customer_ID", "Driver_ID", "Vehicle_ID", "From", "To", "Kg", "$", "Status", "Created_At"],
        rows
    )


def delete_shipment():
    sid = input_int("Enter Shipment ID to delete: ")
    if not record_exists("tbl_shipments", sid):
        print("❌ Shipment not found")
        return

    ok, err = safe_execute("DELETE FROM tbl_shipments WHERE id=?", (sid,))
    if ok:
        print("✅ Shipment deleted")
    else:
        print("❌ Error:", err)


# =========================
# REPORTS
# =========================
def report_summary():
    total_shipments = fetch_all("SELECT COUNT(*) FROM tbl_shipments")[0][0]

    delivered = fetch_all("SELECT COUNT(*) FROM tbl_shipments WHERE status='Delivered'")[0][0]
    in_transit = fetch_all("SELECT COUNT(*) FROM tbl_shipments WHERE status='In Transit'")[0][0]
    pending = fetch_all("SELECT COUNT(*) FROM tbl_shipments WHERE status='Pending'")[0][0]
    cancelled = fetch_all("SELECT COUNT(*) FROM tbl_shipments WHERE status='Cancelled'")[0][0]

    income = fetch_all("SELECT SUM(price_usd) FROM tbl_shipments WHERE status <> 'Cancelled'")[0][0]
    if income is None:
        income = 0

    print("\n" + "=" * 60)
    print("REPORT SUMMARY")
    print("=" * 60)
    print(f"Total shipments : {total_shipments}")
    print(f"Delivered       : {delivered}")
    print(f"In Transit      : {in_transit}")
    print(f"Pending         : {pending}")
    print(f"Cancelled       : {cancelled}")
    print(f"Total income($) : {income:.2f}")
    print("=" * 60)


# =========================
# MENUS
# =========================
def menu_customers():
    while True:
        print("\n--- Customers Menu ---")
        print("1) Add Customer")
        print("2) View Customers")
        print("3) Edit Customer")
        print("4) Delete Customer")
        print("0) Back")
        ch = input("Choose: ").strip()

        if ch == "1": add_customer()
        elif ch == "2": view_customers()
        elif ch == "3": edit_customer()
        elif ch == "4": delete_customer()
        elif ch == "0": break
        else: print("❌ Invalid choice")


def menu_drivers():
    while True:
        print("\n--- Drivers Menu ---")
        print("1) Add Driver")
        print("2) View Drivers")
        print("3) Edit Driver")
        print("4) Delete Driver")
        print("0) Back")
        ch = input("Choose: ").strip()

        if ch == "1": add_driver()
        elif ch == "2": view_drivers()
        elif ch == "3": edit_driver()
        elif ch == "4": delete_driver()
        elif ch == "0": break
        else: print("❌ Invalid choice")


def menu_vehicles():
    while True:
        print("\n--- Vehicles Menu ---")
        print("1) Add Vehicle")
        print("2) View Vehicles")
        print("3) Edit Vehicle")
        print("4) Delete Vehicle")
        print("0) Back")
        ch = input("Choose: ").strip()

        if ch == "1": add_vehicle()
        elif ch == "2": view_vehicles()
        elif ch == "3": edit_vehicle()
        elif ch == "4": delete_vehicle()
        elif ch == "0": break
        else: print("❌ Invalid choice")


def menu_shipments():
    while True:
        print("\n--- Shipments Menu ---")
        print("1) Create Shipment")
        print("2) View Shipments (Simple)")
        print("3) View Shipments (JOIN View)")
        print("4) Update Shipment Status")
        print("5) Search Shipments")
        print("6) Delete Shipment")
        print("0) Back")
        ch = input("Choose: ").strip()

        if ch == "1": add_shipment()
        elif ch == "2": view_shipments_simple()
        elif ch == "3": view_shipments_join()
        elif ch == "4": update_shipment_status()
        elif ch == "5": search_shipments()
        elif ch == "6": delete_shipment()
        elif ch == "0": break
        else: print("❌ Invalid choice")


def main():
    ok, msg = test_connection()
    print(msg)
    if not ok:
        print("\n✅ Fix tips:")
        print("1) pip install pyodbc")
        print("2) Install Microsoft Access Database Engine (match Python 32/64-bit)")
        print("3) Confirm file path is correct:", DB_PATH)
        return

    while True:
        print("\n" + "=" * 60)
        print("TRANSPORT COMPANY INFORMATION SYSTEM (Python + MS Access)")
        print("=" * 60)
        print("1) Customers")
        print("2) Drivers")
        print("3) Vehicles")
        print("4) Shipments / Orders")
        print("5) Report Summary")
        print("0) Exit")
        ch = input("Choose: ").strip()

        if ch == "1": menu_customers()
        elif ch == "2": menu_drivers()
        elif ch == "3": menu_vehicles()
        elif ch == "4": menu_shipments()
        elif ch == "5": report_summary()
        elif ch == "0":
            print("👋 Bye!")
            break
        else:
            print("❌ Invalid choice")


if __name__ == "__main__":
    main()
