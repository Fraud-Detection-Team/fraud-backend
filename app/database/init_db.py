from app.auth.models import Base
from app.database.db import engine

existing = db.query(User).filter(User.username == "admin@example.com").first()
if not existing:
    new_user = User(
        email="admin@example.com",
        hashed_password=get_password_hash("password123"),
        role="admin"
    )
    db.add(new_user)
    db.commit()
    print("✅ Admin user created")
else:
    print("ℹ️ Admin user already exists")
