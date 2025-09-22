# iShop4U Backend – Database Schema

This project defines the database schema for the iShop4U system using Flask + SQLAlchemy.  
It provides a unified shopping cart across multiple affiliate platforms (Amazon, AliExpress, etc.) while maintaining affiliate links for checkout.

---

## Schema Pages Link
https://chiznox6.github.io/ishop4u-backend/

## Schema Overview

### Tables
- **users**
  - Stores shopper accounts (name, email, password hash).
- **affiliate_sources**
  - Stores affiliate platforms (Amazon, AliExpress, etc.).
- **products**
  - Stores product data (name, price, image, affiliate link).
- **cart_items**
  - Connects users and products (with quantity & notes).

---

## Relationships
- **User -< CartItem >- Product** (many-to-many via `cart_items`).  
- **Product >- AffiliateSource** (one-to-many).  

Entity Relationship Diagram:

users                       products                       affiliate_sources
  │                            │                                 │
  │ 1                          │ 1                               │ 1
  │                            │                                 │
  └──────< cart_items >────────┘                                 └───< products
         (quantity, notes)



## How to read this:

A user can have many cart items.

A product can appear in many users’ carts (many-to-many via cart_items).

Each product belongs to one affiliate source (Amazon, AliExpress, etc.).


---

## Example SQL Schema

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE affiliate_sources (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    api_name VARCHAR(100),
    base_url TEXT
);

CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    image_url TEXT,
    price DECIMAL(10,2),
    affiliate_link TEXT NOT NULL,
    affiliate_source_id INT REFERENCES affiliate_sources(id) ON DELETE CASCADE
);

CREATE TABLE cart_items (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    product_id INT REFERENCES products(id) ON DELETE CASCADE,
    quantity INT DEFAULT 1,
    notes TEXT,
    added_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE (user_id, product_id)

);



---

## Running Locally

1. Clone the repository:

git clone git@github.com:chiznox6/ishop4u-backend.git
cd ishop4u-backend


2. Install dependencies:

pip install -r requirements.txt


3. Run migrations:

flask db upgrade


4. Verify tables:

sqlite3 ishop4u.db ".tables"



## GitHub Pages

This repository is published on GitHub Pages as documentation:  https://github.com/chiznox6/ishop4u-backend.git


## Notes

This schema is designed for a Flask + React full-stack project.

iShop4U does not handle payments directly; checkout redirects to affiliate links.

The schema supports CRUD for CartItem and read/create for Product.