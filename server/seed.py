# Standard library imports
from random import randint, choice

# Remote library imports
from faker import Faker

# Local imports
from app import app, db, bcrypt
from models import User, Category, Item, Order, Feedback

fake = Faker()

def seed_users():
    users = []
    for _ in range(10):
        user = User(
            username=fake.user_name(),
            email=fake.email(),
            password=bcrypt.generate_password_hash("password").decode("utf-8"),
            location=fake.text(max_nb_chars=20),
            bio=fake.text(max_nb_chars=200)
        )
        users.append(user)
        db.session.add(user)
    db.session.commit()
    return users
    

def seed_categories():
    categories_data = ['Electronics', 'Clothing', 'Home & Kitchen', 'Books', 'Toys', 'Beauty']
    categories = []
    for name in categories_data:
        category = Category(name=name)
        categories.append(category)
        db.session.add(category)
    db.session.commit()
    return categories

def seed_items(categories):
    items = []
    for _ in range(20):
        item = Item(
            title=fake.word(),
            description=fake.text(max_nb_chars=200),
            price=round(randint(100, 10000) / 100, 2),
            imageurl=fake.image_url(),
            category_id=choice(categories).id
        )
        items.append(item)
        db.session.add(item)
    db.session.commit()
    return items

def seed_orders(users, items):
    orders = []
    for _ in range(10):
        order = Order(
            quantity=randint(1, 5),
            status=choice(['pending', 'shipped', 'delivered', 'cancelled']),
            user_id=choice(users).id
        )
        for _ in range(randint(1, 3)):  # Randomly add items to orders
            order.items.append(choice(items))
        orders.append(order)
        db.session.add(order)
    db.session.commit()
    return orders

def seed_feedback(items):
    feedbacks = []
    for _ in range(20):
        feedback = Feedback(
            email=fake.email(),
            name=fake.name(),
            feedback=fake.text(max_nb_chars=300),
            item_id=choice(items).id
        )
        feedbacks.append(feedback)
        db.session.add(feedback)
    db.session.commit()
    return feedbacks

def main():
    with app.app_context():
        print("Starting seed...")

        # Clear existing data
        db.drop_all()
        db.create_all()

        # Seed data
        users = seed_users()
        categories = seed_categories()
        items = seed_items(categories)
        orders = seed_orders(users, items)
        feedbacks = seed_feedback(items)

        print("Database seeded successfully.")

if __name__ == '__main__':
    main()
