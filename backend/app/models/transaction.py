from sqlalchemy import Column, Integer, String, DateTime, DECIMAL, ForeignKey, CheckConstraint
from sqlalchemy.orm import relationship
from ..database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id          = Column(Integer, primary_key=True, autoincrement=True)
    user_id     = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount      = Column(DECIMAL(18, 2), nullable=False)
    date        = Column(DateTime, nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)
    note        = Column(String(255))
    type        = Column(String(10), nullable=False)  # 'income' | 'outcome'

    __table_args__ = (
        CheckConstraint("type IN ('income','outcome')", name="ck_transactions_type"),
    )

    user = relationship("User", back_populates="transactions")
    category = relationship("Category", back_populates="transactions")