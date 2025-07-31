from auth import init_db, add_user

init_db()
add_user("admin", "password123", role="admin")
print("Admin user created.")

