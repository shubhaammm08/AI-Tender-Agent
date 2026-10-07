from sqlalchemy import Column, String, BigInteger, Numeric, DateTime
from database import Base
from sqlalchemy.sql import func

class PriceHistory(Base):
    __tablename__ = "price_history"
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    item = Column(String, nullable=False)
    buyer = Column(String, nullable=True)
    state = Column(String, nullable=True)
    l1_price = Column(Numeric, nullable=True)
    awarded_on = Column(DateTime(timezone=True), nullable=True)
