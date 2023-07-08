from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from connect_db import Base, engine


class Brand(Base):
    __tablename__ = "brands"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    size = Column(Integer)
    is_lux = Column(Boolean, default=False) #для навчальних цілей, щоб спробувати з булевим полем працювати
    description = Column(String, index=True)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=True)
    brand_id = Column(Integer, ForeignKey("brands.id"), nullable=True)
    #можливо додати поле кількість товарів на складі
    #можливо додати поле кількість товарів в корзині інших покупців

    brand = relationship("Brand", backref="brands")
    category = relationship("Category", backref="categories")




Base.metadata.create_all(bind=engine)

