# Standard library imports
from random import randint, choice

# Local imports
from app import app, db, bcrypt
from models import User, Category, Item, Order, Feedback

def seed_users():
    users = []
    user_data = [
    {'username': 'alice', 'email': 'alice@example.com', 'password': 'password1', 'location': 'New York', 'bio': ''},
    {'username': 'bob', 'email': 'bob@example.com', 'password': 'password2', 'location': 'Los Angeles', 'bio': ''},
    {'username': 'charlie', 'email': 'charlie@example.com', 'password': 'password3', 'location': 'Chicago', 'bio': ''},
    {'username': 'diana', 'email': 'diana@example.com', 'password': 'password4', 'location': 'Houston', 'bio': ''},
    {'username': 'edward', 'email': 'edward@example.com', 'password': 'password5', 'location': 'Phoenix', 'bio': ''}
    ]


    for data in user_data:
        user = User(
            username=data['username'],
            email=data['email'],
            password=bcrypt.generate_password_hash(data['password']).decode('utf-8'),
            location=data['location'],
            bio=data['bio']
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
    items_data = [
        {'title': 'Smartphone', 'description': 'Latest model with advanced features', 'price': 50000, 'category_id': 1, 'imageurl': 'https://images.pexels.com/photos/4549408/pexels-photo-4549408.jpeg?auto=compress&cs=tinysrgb&dpr=1&w=252&fit=crop&h=408'},
        {'title': 'Jeans', 'description': 'Stylish denim', 'price': 3000, 'category_id': 2, 'imageurl': 'https://media.istockphoto.com/id/1032057264/photo/a-rack-of-second-hand-jeans.jpg?b=1&s=612x612&w=0&k=20&c=BB8lDuQtd8Oou3sqYGPi3lkPWJhRTWQ-RKGPlfOo_Lc='},
        {'title': 'Microwave', 'description': 'Efficient heating appliance', 'price': 6000, 'category_id': 3, 'imageurl': 'https://media.istockphoto.com/id/1406993092/photo/a-cropped-photo-of-an-anonymous-caucasian-female-heating-food-in-the-oven.jpg?b=1&s=612x612&w=0&k=20&c=oAigEGcaE-OiPuA8ixdmHgYUrZ5Vc1BOOatn0hr1GtE='},
        {'title': 'Cookbook', 'description': 'Inspiring recipes for every occasion', 'price': 1500, 'category_id': 4, 'imageurl': 'https://images.pexels.com/photos/8064906/pexels-photo-8064906.jpeg?auto=compress&cs=tinysrgb&w=400'},
        {'title': 'Puzzle', 'description': 'Challenging brain teaser', 'price': 800, 'category_id': 5, 'imageurl': 'https://images.pexels.com/photos/54101/magic-cube-cube-puzzle-play-54101.jpeg?auto=compress&cs=tinysrgb&w=400'},
        {'title': 'Mascara', 'description': 'Enhances eyelashes for a dramatic look', 'price': 1200, 'category_id': 6, 'imageurl': 'https://images.pexels.com/photos/2637820/pexels-photo-2637820.jpeg?auto=compress&cs=tinysrgb&w=400'},
        {'title': 'Tablet', 'description': 'Portable device for work and entertainment', 'price': 15000, 'category_id': 1, 'imageurl': 'https://media.istockphoto.com/id/1378688632/photo/mockup-image-of-a-woman-holding-digital-tablet-with-blank-white-desktop-screen-in-cafe.jpg?b=1&s=612x612&w=0&k=20&c=iM0XD84X2r1rfhtP67f4zuFvjNj_Yz3e3O2zpJSnCNg='},
        {'title': 'Jacket', 'description': 'Stylish and warm winter jacket', 'price': 5000, 'category_id': 2, 'imageurl': 'https://media.istockphoto.com/id/1438058575/photo/multicolored-winter-down-jackets-hanging-on-hangers-in-the-store-close-up-side-view.jpg?b=1&s=612x612&w=0&k=20&c=ljRP1lPVGLMd25gqooiwB1uuSqKbJi2kPnk5Tav_LFE='},
        {'title': 'Toaster', 'description': 'Stainless steel toaster with toast function', 'price': 3000, 'category_id': 3, 'imageurl': 'https://media.istockphoto.com/id/173626392/photo/stainless-toaster-with-toast.jpg?b=1&s=612x612&w=0&k=20&c=NeC4YnyJz_266HykDIiMmjsG66TjibAD8vmcc-Pcn58='},
        {'title': 'Biography', 'description': 'Compelling life story of a notable person', 'price': 1800, 'category_id': 4, 'imageurl': 'https://images.pexels.com/photos/3207628/pexels-photo-3207628.jpeg?auto=compress&cs=tinysrgb&w=400'},
        {'title': 'Board Game', 'description': 'Fun and engaging tabletop game for family and friends', 'price': 2500, 'category_id': 5, 'imageurl': 'https://images.pexels.com/photos/260024/pexels-photo-260024.jpeg?auto=compress&cs=tinysrgb&w=400'},
        {'title': 'Foundation', 'description': 'Makeup base for a flawless complexion', 'price': 2000, 'category_id': 6, 'imageurl': 'https://images.pexels.com/photos/6954001/pexels-photo-6954001.jpeg?auto=compress&cs=tinysrgb&w=400'},
        {'title': 'Dress', 'description': 'Elegant and stylish attire for special occasions', 'price': 4500, 'category_id': 2, 'imageurl': 'https://images.pexels.com/photos/985685/pexels-photo-985685.jpeg?auto=compress&cs=tinysrgb&w=400'},
        {'title': 'Smartwatch', 'description': 'Modern wearable technology for health and productivity', 'price': 12000, 'category_id': 1, 'imageurl': 'https://images.pexels.com/photos/2861929/pexels-photo-2861929.jpeg?auto=compress&cs=tinysrgb&w=400'},
        {'title': 'Coffee Maker', 'description': 'Modern espresso machine for brewing delicious coffee', 'price': 8000, 'category_id': 3, 'imageurl': 'https://media.istockphoto.com/id/1302271960/photo/modern-espresso-coffee-machine-with-a-cup-in-interior-of-kitchen-closeup.jpg?b=1&s=612x612&w=0&k=20&c=80o4VCsc78PAN88JNR7akYX2CD42RSs67U2dMWDWf4w='},
        {'title': 'Mystery Novel', 'description': 'Captivating book full of suspense and intrigue', 'price': 1500, 'category_id': 4, 'imageurl': 'https://images.pexels.com/photos/256450/pexels-photo-256450.jpeg?auto=compress&cs=tinysrgb&w=400'},
        {'title': 'Action Figure', 'description': 'Collectible toy depicting a heroic character', 'price': 1500, 'category_id': 5, 'imageurl': 'https://images.pexels.com/photos/4662338/pexels-photo-4662338.jpeg?auto=compress&cs=tinysrgb&w=400'},
        {'title': 'Nail Polish', 'description': 'Fashionable nail color for stylish looks', 'price': 500, 'category_id': 6, 'imageurl': 'https://images.pexels.com/photos/3060257/pexels-photo-3060257.jpeg?auto=compress&cs=tinysrgb&w=400'},
        {'title': 'Camera', 'description': 'High-quality digital camera for photography enthusiasts', 'price': 18000, 'category_id': 1, 'imageurl': 'https://images.pexels.com/photos/243757/pexels-photo-243757.jpeg?auto=compress&cs=tinysrgb&w=400'},
        {'title': 'Sweaters', 'description': 'Comfortable and stylish sweaters for warmth and fashion', 'price': 3000, 'category_id': 2, 'imageurl': 'https://images.pexels.com/photos/9594673/pexels-photo-9594673.jpeg?auto=compress&cs=tinysrgb&w=400'},
        {'title': 'Blender', 'description': 'Powerful electric blender for smoothies and cooking', 'price': 4000, 'category_id': 3, 'imageurl': 'https://media.istockphoto.com/id/471441539/photo/electric-blender.jpg?b=1&s=612x612&w=0&k=20&c=TMxefU1zw4siaaOyuU_nBd3A4Q07GneZuhOJMUQ8RNo='},
        {'title': 'Science Fiction', 'description': 'Exciting book exploring futuristic worlds and technologies', 'price': 1800, 'category_id': 4, 'imageurl': 'https://images.pexels.com/photos/4627894/pexels-photo-4627894.jpeg?auto=compress&cs=tinysrgb&w=400'},
        {'title': 'Doll', 'description': 'Adorable doll for play and collection', 'price': 1200, 'category_id': 5, 'imageurl': 'https://images.pexels.com/photos/753501/pexels-photo-753501.jpeg?auto=compress&cs=tinysrgb&w=400'},
        {'title': 'Perfume', 'description': 'Elegant fragrance for a refreshing scent', 'price': 2500, 'category_id': 6, 'imageurl': 'https://media.istockphoto.com/id/1399637805/photo/top-view-flat-lay-of-a-set-of-perfume-bottles-on-a-beige-blank-background.jpg?b=1&s=612x612&w=0&k=20&c=zhEZjtav7bCnjfzKq1DlrNvHthBWLh9tGjPZgyCrloY='},
        {'title': 'Headphone', 'description': 'High-quality headphones for immersive audio experience', 'price': 3500, 'category_id': 1, 'imageurl': 'https://images.pexels.com/photos/3587478/pexels-photo-3587478.jpeg?auto=compress&cs=tinysrgb&w=400'},
        {'title': 'Scarf', 'description': 'Warm and stylish scarf for cold weather', 'price': 1500, 'category_id': 2, 'imageurl': 'https://images.pexels.com/photos/2641022/pexels-photo-2641022.jpeg?auto=compress&cs=tinysrgb&w=400'},
        {'title': 'Air Fryer', 'description': 'Efficient air fryer for healthier cooking', 'price': 4000, 'category_id': 3, 'imageurl': 'https://media.istockphoto.com/id/1305594664/photo/air-frying-homemade-chicken-nuggets.jpg?b=1&s=612x612&w=0&k=20&c=x2c5QeVUnJHGB8sSCDD2UGgU2XWRKNxV0ZRltxhRXvY='},
        {'title': 'Fantasy Novel', 'description': 'Immerse yourself in a world of magic and adventure', 'price': 1200, 'category_id': 4, 'imageurl': 'https://images.pexels.com/photos/1005012/pexels-photo-1005012.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1'},
        {'title': 'Plush Toy', 'description': 'Soft and cuddly plush toy for kids', 'price': 800, 'category_id': 5, 'imageurl': 'https://images.pexels.com/photos/1860160/pexels-photo-1860160.jpeg?auto=compress&cs=tinysrgb&w=400'},
        {'title': 'Lip Balm', 'description': 'Moisturizing lip balm for soft and smooth lips', 'price': 200, 'category_id': 6, 'imageurl': 'https://images.pexels.com/photos/14438175/pexels-photo-14438175.jpeg?auto=compress&cs=tinysrgb&w=400'},
        {'title': 'Toy Car', 'description': 'Colorful toy cars for endless playtime fun', 'price': 500, 'category_id': 5, 'imageurl': 'https://media.istockphoto.com/id/1316414554/photo/colorful-toy-cars-top-view-on-a-yellow-background-with-copy-space.jpg?b=1&s=612x612&w=0&k=20&c=ikM67xSR1l-5TcyUNhFIcKUVw43VoSsoFMYWyGaORHg='},
        {'title': 'Laptop', 'description': 'Powerful and portable', 'price': 70000, 'category_id': 1, 'imageurl': 'https://media.istockphoto.com/id/1394988455/photo/laptop-with-a-blank-screen-on-a-white-background.jpg?b=1&s=612x612&w=0&k=20&c=VCCVeK25QpSCdGjiDgeviwz2pJfikLyclwhX-MQblhg='},
        {'title': 'Lipstick', 'description': 'Vibrant lipstick for adding color and style', 'price': 300, 'category_id': 6, 'imageurl': 'https://images.pexels.com/photos/2533266/pexels-photo-2533266.jpeg?auto=compress&cs=tinysrgb&w=400'},
        {'title': 'Sneakers', 'description': 'Comfortable sneakers for everyday wear', 'price': 800, 'category_id': 2, 'imageurl': 'https://images.pexels.com/photos/1456706/pexels-photo-1456706.jpeg?auto=compress&cs=tinysrgb&w=400'},
        {'title': 'Desk Lamp', 'description': 'Modern desk lamp for home or office use', 'price': 1500, 'category_id': 2, 'imageurl': 'https://media.istockphoto.com/id/1219750966/photo/working-from-home.jpg?b=1&s=612x612&w=0&k=20&c=6vJhunkz_Um9QhvZnxOVJzbmHPmeSn-W0ZPLNwRfYsE='},

    ]
    items = []
    for data in items_data:
        item = Item(
            title=data['title'],
            description=data['description'],
            price=data['price'],
            imageurl=data['imageurl'],
            category_id=data['category_id']
        )
        items.append(item)
        db.session.add(item)
    db.session.commit()
    return items

def seed_feedback(items):
    feedback_data = [
        {'email': 'john.doe@example.com', 'name': 'John Doe', 'feedback': 'Great product!'},
        {'email': 'jane.doe@example.com', 'name': 'Jane Doe', 'feedback': 'Loved it!'},
        {'email': 'mark.smith@example.com', 'name': 'Mark Smith', 'feedback': 'Highly recommend.'},
        {'email': 'lucy.brown@example.com', 'name': 'Lucy Brown', 'feedback': 'Very satisfied.'},
        {'email': 'michael.johnson@example.com', 'name': 'Michael Johnson', 'feedback': 'Five stars!'},
        {'email': 'mary.williams@example.com', 'name': 'Mary Williams', 'feedback': 'Amazing quality.'},
        {'email': 'peter.jones@example.com', 'name': 'Peter Jones', 'feedback': 'Will buy again.'},
        {'email': 'susan.miller@example.com', 'name': 'Susan Miller', 'feedback': 'Very happy with the purchase.'},
        {'email': 'david.moore@example.com', 'name': 'David Moore', 'feedback': 'Exceeded expectations.'},
        {'email': 'linda.taylor@example.com', 'name': 'Linda Taylor', 'feedback': 'Fantastic!'},
        {'email': 'james.anderson@example.com', 'name': 'James Anderson', 'feedback': 'Good value for money.'},
        {'email': 'patricia.thomas@example.com', 'name': 'Patricia Thomas', 'feedback': 'Very pleased.'},
        {'email': 'robert.jackson@example.com', 'name': 'Robert Jackson', 'feedback': 'Top quality.'},
        {'email': 'barbara.white@example.com', 'name': 'Barbara White', 'feedback': 'Better than expected.'},
        {'email': 'steven.harris@example.com', 'name': 'Steven Harris', 'feedback': 'Will recommend to others.'},
        {'email': 'joseph.martin@example.com', 'name': 'Joseph Martin', 'feedback': 'Loved the product.'},
        {'email': 'margaret.lee@example.com', 'name': 'Margaret Lee', 'feedback': 'Very happy.'},
        {'email': 'charles.walker@example.com', 'name': 'Charles Walker', 'feedback': 'Worth the money.'},
        {'email': 'ruth.allen@example.com', 'name': 'Ruth Allen', 'feedback': 'Great experience.'},
        {'email': 'kevin.king@example.com', 'name': 'Kevin King', 'feedback': 'Superb!'},
        {'email': 'betty.scott@example.com', 'name': 'Betty Scott', 'feedback': 'Really nice!'},
        {'email': 'george.baker@example.com', 'name': 'George Baker', 'feedback': 'Amazing product.'},
        {'email': 'carol.nelson@example.com', 'name': 'Carol Nelson', 'feedback': 'Better than expected.'},
        {'email': 'richard.carter@example.com', 'name': 'Richard Carter', 'feedback': 'Superb!'},
        {'email': 'karen.mitchell@example.com', 'name': 'Karen Mitchell', 'feedback': 'Will recommend to others.'},
        {'email': 'donald.perez@example.com', 'name': 'Donald Perez', 'feedback': 'Loved the product.'},
        {'email': 'lisa.roberts@example.com', 'name': 'Lisa Roberts', 'feedback': 'Very happy.'},
        {'email': 'kevin.wilson@example.com', 'name': 'Kevin Wilson', 'feedback': 'Worth the money.'},
        {'email': 'susan.martin@example.com', 'name': 'Susan Martin', 'feedback': 'Great experience.'}
    ]
    feedbacks = []
    for data in feedback_data:
        feedback = Feedback(
            email=data['email'],
            name=data['name'],
            feedback=data['feedback'],
            item_id=choice(items).id
        )
        feedbacks.append(feedback)
        db.session.add(feedback)
    db.session.commit()
    return feedbacks

def seed_orders(users, items, categories):
    orders = []
    for _ in range(10):  # Adjust the range as needed
        order = Order(
            title=f"Order Title {_}",
            description=f"Order Description {_}",
            price=randint(10, 100),  # Example: Random price between 10 and 100
            imageurl=f"http://example.com/image{_}.jpg",
            category_id=choice(categories).id  # Random category ID from categories
        )
         # Add random items to the order
        order_items = [choice(items) for _ in range(randint(1, 5))]  # Randomly pick 1 to 5 items
        order.items.extend(order_items)
        orders.append(order)
    # Add orders to the session and commit
    db.session.add_all(orders)
    db.session.commit()



def seed_all():
    with app.app_context():
        db.drop_all()
        db.create_all()
        
        users = seed_users()
        categories = seed_categories()
        items = seed_items(categories)
        feedbacks = seed_feedback(items)
        orders = seed_orders(users, items)
        
        print("Seeding complete!")

if __name__ == '__main__':
    seed_all()