
from sqlalchemy import select
from app.db.database import SessionLocal
from app.models import User, Role

db = SessionLocal()

try:
    users = db.execute(select(User)).scalars().all()
    roles = db.execute(select(Role)).scalars().all()

    print("USER MODEL: Working")
    print("ROLE MODEL: Working")

    print("\nConfigured roles:")
    for role in roles:
        print(role.role_id, role.role_name)

    print("\nTotal user accounts:", len(users))

except Exception as error:
    print("Model test failed:")
    print(error)

finally:
    db.close()
