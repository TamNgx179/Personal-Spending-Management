# scripts/test_models.py
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from datetime import datetime
from decimal import Decimal
from sqlalchemy import text
from app.database import SessionLocal
from app.models import User, Category, Transaction

def main():
    db = SessionLocal()
    try:
        # seed nhẹ (tùy chọn)
        u = db.query(User).first()
        if not u:
            u = User(name="Admin Demo", email="admin@example.com", password="demo")
            db.add(u); db.flush()
            c1 = Category(name="Ăn uống"); c2 = Category(name="Lương")
            db.add_all([c1, c2]); db.flush()
            db.add_all([
                Transaction(user_id=u.id, category_id=c1.id, amount=Decimal("45000.00"), date=datetime.utcnow(), note="Cà phê", type="outcome"),
                Transaction(user_id=u.id, category_id=c2.id, amount=Decimal("15000000.00"), date=datetime.utcnow(), note="Lương", type="income"),
            ])
            db.commit()

        # test query ORM
        print("\n--- USERS ---")
        for x in db.query(User).all():
            print(x.id, x.name, x.email)

        # test query SQL thô
        print("\n--- TRANSACTIONS (sum by type) ---")
        rows = db.execute(text("SELECT type, SUM(amount) AS total FROM transactions GROUP BY type"))
        for r in rows:
            print(r.type, r.total)
    finally:
        db.close()

if __name__ == "__main__":
    main()
