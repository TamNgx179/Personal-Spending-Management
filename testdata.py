import pyodbc

# ====== 1. Thông tin kết nối ======
driver   = 'SQL Server'     # Hoặc "ODBC Driver 17 for SQL Server" / "ODBC Driver 18 for SQL Server"
server   = r'LAPTOP-7N0B7R24\SQL'   # ⚠️ Giữ nguyên như của bạn
database = 'ChiTieu'        # Đúng tên database bạn tạo trong SQL Server
username = ''               # Nếu dùng Windows Auth -> để trống
password = ''               # Nếu dùng Windows Auth -> để trống

# Nếu bạn dùng Windows Authentication:
conn_str = (
    f"DRIVER={{{driver}}};"
    f"SERVER={server};"
    f"DATABASE={database};"
    "Trusted_Connection=Yes;"
)
# Nếu bạn dùng SQL Authentication (tài khoản sa...), thì thay bằng:
# conn_str = f"DRIVER={{{driver}}};SERVER={server};DATABASE={database};UID={username};PWD={password}"

# ====== 2. Kết nối tới SQL Server ======
try:
    cnxn = pyodbc.connect(conn_str)
    cursor = cnxn.cursor()
    print("✅ Kết nối thành công đến database ChiTieu!")
except Exception as e:
    print("❌ Kết nối thất bại:", e)
    exit()

# ====== 3. Thực thi truy vấn thử ======

# Ví dụ 1: lấy danh sách user
print("\n--- Danh sách người dùng ---")
cursor.execute("SELECT id, name, email, password FROM dbo.users;")
for row in cursor.fetchall():
    print(f"{row.id}. {row.name} - {row.email} - {row.password}")

# Ví dụ 2: lấy tổng chi tiêu theo danh mục
print("\n--- Tổng chi tiêu theo danh mục ---")
cursor.execute("""
SELECT c.name AS category, SUM(t.amount) AS total
FROM dbo.transactions t
JOIN dbo.categories c ON c.id = t.category_id
WHERE t.type = N'outcome'
GROUP BY c.name;
""")
for row in cursor.fetchall():
    print(f"{row.category}: {row.total:,.0f} VND")

# Ví dụ 3: thêm 1 bản ghi chi tiêu mới
print("\n--- Thêm giao dịch mẫu ---")
cursor.execute("""
INSERT INTO dbo.transactions (user_id, amount, date, category_id, note, type)
VALUES (1, 250000, GETDATE(), 1, N'Cà phê sáng', N'outcome');
""")
cnxn.commit()
print("Đã thêm giao dịch mới thành công!")

# ====== 4. Đóng kết nối ======
cursor.close()
cnxn.close()
print("\n✅ Đã đóng kết nối SQL Server.")
