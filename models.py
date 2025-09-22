from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # relationship
    cart_items = db.relationship("CartItem", back_populates="user", cascade="all, delete-orphan")

class AffiliateSource(db.Model):
    __tablename__ = "affiliate_sources"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    api_name = db.Column(db.String(100))
    base_url = db.Column(db.Text)

    # relationship
    products = db.relationship("Product", back_populates="affiliate_source", cascade="all, delete")

class Product(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    image_url = db.Column(db.Text)
    price = db.Column(db.Numeric(10, 2))
    affiliate_link = db.Column(db.Text, nullable=False)

    affiliate_source_id = db.Column(db.Integer, db.ForeignKey("affiliate_sources.id", ondelete="CASCADE"))
    affiliate_source = db.relationship("AffiliateSource", back_populates="products")

    # relationship
    cart_items = db.relationship("CartItem", back_populates="product", cascade="all, delete-orphan")

class CartItem(db.Model):
    __tablename__ = "cart_items"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id", ondelete="CASCADE"))
    product_id = db.Column(db.Integer, db.ForeignKey("products.id", ondelete="CASCADE"))
    quantity = db.Column(db.Integer, default=1)
    notes = db.Column(db.Text)
    added_at = db.Column(db.DateTime, default=datetime.utcnow)

    # relationships
    user = db.relationship("User", back_populates="cart_items")
    product = db.relationship("Product", back_populates="cart_items")

    # prevent duplicate cart entries
    __table_args__ = (
        db.UniqueConstraint("user_id", "product_id", name="unique_user_product"),
    )
