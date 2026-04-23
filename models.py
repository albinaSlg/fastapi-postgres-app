from sqlalchemy import Column, Integer, String, Float, Boolean
from database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    on_offer = Column(Boolean, default=False)