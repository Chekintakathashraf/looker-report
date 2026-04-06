"""Seed script — populates the SQLite database with realistic Indian e-commerce data."""

import random
import sys
import os
from datetime import datetime, timedelta

# Allow running from project root: python scripts/seed.py
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from faker import Faker

from app.db.database import Base, SessionLocal, engine
from app.models.models import Category, Customer, Order, OrderItem, Product

fake = Faker("en_IN")
random.seed(42)

# ---------------------------------------------------------------------------
# Static reference data
# ---------------------------------------------------------------------------

CATEGORIES = [
    "Electronics",
    "Fashion",
    "Home & Kitchen",
    "Sports",
    "Books",
    "Beauty",
]

PRODUCTS_BY_CATEGORY: dict[str, list[dict]] = {
    "Electronics": [
        {"name": "Redmi Note 13 Pro", "sku": "ELEC-001", "price": 24999, "cost": 18000},
        {"name": "boAt Airdopes 141", "sku": "ELEC-002", "price": 1299, "cost": 600},
        {"name": "Samsung 43-inch 4K TV", "sku": "ELEC-003", "price": 32999, "cost": 24000},
        {"name": "HP 15s Laptop", "sku": "ELEC-004", "price": 45999, "cost": 34000},
        {"name": "Canon EOS 200D DSLR", "sku": "ELEC-005", "price": 52999, "cost": 40000},
        {"name": "Mi Smart Band 8", "sku": "ELEC-006", "price": 2499, "cost": 1200},
        {"name": "Philips Air Fryer", "sku": "ELEC-007", "price": 6999, "cost": 4500},
        {"name": "JBL Charge 5 Speaker", "sku": "ELEC-008", "price": 12999, "cost": 8500},
        {"name": "Lenovo Tab M10 Plus", "sku": "ELEC-009", "price": 17999, "cost": 13000},
        {"name": "Zebronics Gaming Mouse", "sku": "ELEC-010", "price": 1499, "cost": 700},
    ],
    "Fashion": [
        {"name": "Manyavar Sherwani Set", "sku": "FASH-001", "price": 8999, "cost": 4500},
        {"name": "Fabindia Kurta Pyjama", "sku": "FASH-002", "price": 2499, "cost": 1200},
        {"name": "W Anarkali Kurti", "sku": "FASH-003", "price": 1799, "cost": 900},
        {"name": "Raymond Formal Trousers", "sku": "FASH-004", "price": 2199, "cost": 1100},
        {"name": "Bata Leather Sandals", "sku": "FASH-005", "price": 1599, "cost": 800},
        {"name": "Woodland Trekking Shoes", "sku": "FASH-006", "price": 3299, "cost": 1800},
        {"name": "Allen Solly Polo Shirt", "sku": "FASH-007", "price": 999, "cost": 500},
        {"name": "Libas Saree Cotton Blend", "sku": "FASH-008", "price": 1299, "cost": 650},
        {"name": "VIP Skybags Backpack", "sku": "FASH-009", "price": 2499, "cost": 1300},
        {"name": "Titan Raga Watch", "sku": "FASH-010", "price": 5999, "cost": 3500},
    ],
    "Home & Kitchen": [
        {"name": "Prestige Pressure Cooker 5L", "sku": "HOME-001", "price": 1799, "cost": 900},
        {"name": "Pigeon Induction Cooktop", "sku": "HOME-002", "price": 1499, "cost": 750},
        {"name": "Milton Thermosteel Flask 1L", "sku": "HOME-003", "price": 699, "cost": 350},
        {"name": "Solimo Microfibre Blanket", "sku": "HOME-004", "price": 799, "cost": 400},
        {"name": "Cello Modular Shelf", "sku": "HOME-005", "price": 2199, "cost": 1100},
        {"name": "Bajaj Mixer Grinder 750W", "sku": "HOME-006", "price": 2999, "cost": 1600},
        {"name": "Godrej Aer Room Freshener", "sku": "HOME-007", "price": 199, "cost": 80},
        {"name": "Wonderchef Non-stick Tawa", "sku": "HOME-008", "price": 899, "cost": 450},
        {"name": "AmazonBasics Curtains Set", "sku": "HOME-009", "price": 1299, "cost": 650},
        {"name": "Story@Home Bed Sheet King", "sku": "HOME-010", "price": 999, "cost": 500},
    ],
    "Sports": [
        {"name": "Yonex Astrox 88S Badminton", "sku": "SPRT-001", "price": 6999, "cost": 4000},
        {"name": "Nivia Football Size 5", "sku": "SPRT-002", "price": 899, "cost": 400},
        {"name": "Cosco Cricket Kit Senior", "sku": "SPRT-003", "price": 4999, "cost": 2800},
        {"name": "Decathlon Yoga Mat 8mm", "sku": "SPRT-004", "price": 1499, "cost": 700},
        {"name": "Vector X Badminton Net", "sku": "SPRT-005", "price": 799, "cost": 350},
        {"name": "Adidas Running Shoes", "sku": "SPRT-006", "price": 3999, "cost": 2200},
        {"name": "Boldfit Gym Gloves", "sku": "SPRT-007", "price": 499, "cost": 200},
        {"name": "Strauss Resistance Bands", "sku": "SPRT-008", "price": 699, "cost": 300},
        {"name": "Lifelong Fitness Cycle", "sku": "SPRT-009", "price": 8999, "cost": 5500},
        {"name": "Aurion Skipping Rope", "sku": "SPRT-010", "price": 349, "cost": 120},
    ],
    "Books": [
        {"name": "The Alchemist — Paulo Coelho", "sku": "BOOK-001", "price": 299, "cost": 120},
        {"name": "Atomic Habits — James Clear", "sku": "BOOK-002", "price": 499, "cost": 200},
        {"name": "Rich Dad Poor Dad", "sku": "BOOK-003", "price": 349, "cost": 140},
        {"name": "Wings of Fire — APJ Abdul Kalam", "sku": "BOOK-004", "price": 249, "cost": 100},
        {"name": "Ikigai — Francesc Miralles", "sku": "BOOK-005", "price": 299, "cost": 120},
        {"name": "The Psychology of Money", "sku": "BOOK-006", "price": 449, "cost": 180},
        {"name": "Deep Work — Cal Newport", "sku": "BOOK-007", "price": 399, "cost": 160},
        {"name": "Sapiens — Yuval Noah Harari", "sku": "BOOK-008", "price": 599, "cost": 240},
        {"name": "Zero to One — Peter Thiel", "sku": "BOOK-009", "price": 449, "cost": 180},
        {"name": "The Lean Startup", "sku": "BOOK-010", "price": 499, "cost": 200},
    ],
    "Beauty": [
        {"name": "Lakme Absolute Primer", "sku": "BEAU-001", "price": 699, "cost": 300},
        {"name": "Mamaearth Onion Shampoo", "sku": "BEAU-002", "price": 399, "cost": 160},
        {"name": "Biotique Bio Walnut Scrub", "sku": "BEAU-003", "price": 249, "cost": 100},
        {"name": "Forest Essentials Face Wash", "sku": "BEAU-004", "price": 895, "cost": 400},
        {"name": "Himalaya Neem Face Wash", "sku": "BEAU-005", "price": 175, "cost": 70},
        {"name": "WOW Skin Science Vitamin C", "sku": "BEAU-006", "price": 599, "cost": 250},
        {"name": "Plum Goodness Sheet Mask", "sku": "BEAU-007", "price": 149, "cost": 60},
        {"name": "MCaffeine Coffee Body Scrub", "sku": "BEAU-008", "price": 349, "cost": 140},
        {"name": "Dot & Key SPF 50 Sunscreen", "sku": "BEAU-009", "price": 499, "cost": 200},
        {"name": "Minimalist 10% Niacinamide", "sku": "BEAU-010", "price": 599, "cost": 250},
    ],
}

INDIAN_STATES = [
    "Maharashtra", "Tamil Nadu", "Karnataka", "Delhi", "West Bengal",
    "Uttar Pradesh", "Gujarat", "Telangana", "Rajasthan", "Kerala",
    "Madhya Pradesh", "Punjab", "Haryana", "Bihar", "Odisha",
]

CITIES_BY_STATE: dict[str, list[str]] = {
    "Maharashtra": ["Mumbai", "Pune", "Nagpur", "Nashik", "Aurangabad"],
    "Tamil Nadu": ["Chennai", "Coimbatore", "Madurai", "Tiruchirappalli", "Salem"],
    "Karnataka": ["Bengaluru", "Mysuru", "Hubli", "Mangaluru", "Belagavi"],
    "Delhi": ["New Delhi", "Dwarka", "Rohini", "Saket", "Lajpat Nagar"],
    "West Bengal": ["Kolkata", "Howrah", "Durgapur", "Asansol", "Siliguri"],
    "Uttar Pradesh": ["Lucknow", "Kanpur", "Agra", "Varanasi", "Meerut"],
    "Gujarat": ["Ahmedabad", "Surat", "Vadodara", "Rajkot", "Bhavnagar"],
    "Telangana": ["Hyderabad", "Warangal", "Nizamabad", "Karimnagar", "Khammam"],
    "Rajasthan": ["Jaipur", "Jodhpur", "Udaipur", "Kota", "Ajmer"],
    "Kerala": ["Thiruvananthapuram", "Kochi", "Kozhikode", "Thrissur", "Kollam"],
    "Madhya Pradesh": ["Bhopal", "Indore", "Gwalior", "Jabalpur", "Ujjain"],
    "Punjab": ["Ludhiana", "Amritsar", "Jalandhar", "Patiala", "Bathinda"],
    "Haryana": ["Gurugram", "Faridabad", "Panipat", "Ambala", "Hisar"],
    "Bihar": ["Patna", "Gaya", "Bhagalpur", "Muzaffarpur", "Darbhanga"],
    "Odisha": ["Bhubaneswar", "Cuttack", "Rourkela", "Berhampur", "Sambalpur"],
}

ORDER_STATUSES = ["pending", "processing", "shipped", "delivered", "cancelled"]
STATUS_WEIGHTS = [5, 10, 15, 55, 15]  # weighted toward delivered


def seed() -> None:
    """Drop and recreate all tables, then populate with seed data."""
    print("⟳  Dropping and recreating tables …")
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()
    try:
        # ------------------------------------------------------------------
        # Categories
        # ------------------------------------------------------------------
        print("⟳  Seeding categories …")
        category_objs: dict[str, Category] = {}
        for cat_name in CATEGORIES:
            cat = Category(name=cat_name)
            db.add(cat)
            category_objs[cat_name] = cat
        db.flush()

        # ------------------------------------------------------------------
        # Products
        # ------------------------------------------------------------------
        print("⟳  Seeding products …")
        product_objs: list[Product] = []
        for cat_name, products in PRODUCTS_BY_CATEGORY.items():
            for prod in products:
                stock = random.randint(0, 200)
                p = Product(
                    name=prod["name"],
                    sku=prod["sku"],
                    price=prod["price"],
                    cost_price=prod["cost"],
                    stock=stock,
                    category_id=category_objs[cat_name].id,
                )
                db.add(p)
                product_objs.append(p)
        db.flush()

        # ------------------------------------------------------------------
        # Customers
        # ------------------------------------------------------------------
        print("⟳  Seeding 300 customers …")
        customer_objs: list[Customer] = []
        used_emails: set[str] = set()
        for _ in range(300):
            state = random.choice(INDIAN_STATES)
            city = random.choice(CITIES_BY_STATE[state])
            email = fake.email()
            while email in used_emails:
                email = fake.email()
            used_emails.add(email)
            c = Customer(
                name=fake.name(),
                email=email,
                phone=fake.phone_number()[:20],
                city=city,
                state=state,
            )
            db.add(c)
            customer_objs.append(c)
        db.flush()

        # ------------------------------------------------------------------
        # Orders + OrderItems
        # ------------------------------------------------------------------
        print("⟳  Seeding 1500 orders with items …")
        start_date = datetime.now() - timedelta(days=365)

        for i in range(1500):
            customer = random.choice(customer_objs)
            status = random.choices(ORDER_STATUSES, weights=STATUS_WEIGHTS, k=1)[0]
            created_at = start_date + timedelta(
                seconds=random.randint(0, 365 * 24 * 3600)
            )
            delivered_at = None
            if status == "delivered":
                delivered_at = created_at + timedelta(days=random.randint(2, 10))

            order = Order(
                order_number=f"ORD-{i + 1:05d}",
                customer_id=customer.id,
                status=status,
                total_amount=0.0,
                discount=round(random.uniform(0, 500), 2),
                created_at=created_at,
                delivered_at=delivered_at,
            )
            db.add(order)
            db.flush()

            num_items = random.randint(1, 5)
            chosen_products = random.sample(product_objs, num_items)
            order_total = 0.0

            for product in chosen_products:
                qty = random.randint(1, 3)
                unit_price = round(product.price * random.uniform(0.9, 1.0), 2)
                total_price = round(unit_price * qty, 2)
                order_total += total_price

                item = OrderItem(
                    order_id=order.id,
                    product_id=product.id,
                    quantity=qty,
                    unit_price=unit_price,
                    total_price=total_price,
                )
                db.add(item)

            order.total_amount = round(order_total - order.discount, 2)
            if order.total_amount < 0:
                order.total_amount = 0.0

        db.commit()
        print("✓  Seeding complete.")
        print(f"   Categories : {len(CATEGORIES)}")
        print(f"   Products   : {sum(len(v) for v in PRODUCTS_BY_CATEGORY.values())}")
        print(f"   Customers  : 300")
        print(f"   Orders     : 1500")

    except Exception as exc:
        db.rollback()
        print(f"✗  Seeding failed: {exc}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed()
