# models.py

from sqlalchemy import Column, Integer, String, Text, JSON
from db import Base

class BrandData(Base):
    __tablename__ = "brand_data"

    id = Column(Integer, primary_key=True, index=True)
    website_url = Column(String(255), unique=True, nullable=False)
    data = Column(JSON, nullable=False)
