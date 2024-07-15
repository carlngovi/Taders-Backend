from flask import Flask, request, jsonify
from models import db, User, Category, Item, Order, Feedback
from flask_migrate import Migrate
from flask_restful import Api
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
import os
import random

# Init
app = Flask(__name__)
api = Api(app)
CORS(app)

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_URI = os.environ.get("DB_URI", f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'app.db')}")

app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.json.compact = False
app.config["JWT_SECRET_KEY"] = "fsbdgfnhgvjnvhmvh" + str(random.randint(1, 1000000000000))
app.config["SECRET_KEY"] = "JKSRVHJVFBSRDFV" + str(random.randint(1, 1000000000000))

bcrypt = Bcrypt(app)
jwt = JWTManager(app)

migrate = Migrate(app, db)
db.init_app(app)
ma = Marshmallow(app)

@app.route('/')
def index():
    return "Welcome to the API"

# Schemas for serialization/deserialization
class ItemSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Item

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

class FeedbackSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Feedback

item_schema = ItemSchema()
items_schema = ItemSchema(many=True)
user_schema = UserSchema()
users_schema = UserSchema(many=True)
feedback_schema = FeedbackSchema()
feedbacks_schema = FeedbackSchema(many=True)

# Login endpoint 
# Login endpoint 
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Invalid input'}), 400

    user = User.query.filter_by(email=data['email']).first()
    if user and bcrypt.check_password_hash(user.password, data['password']):
        access_token = create_access_token(identity=user.id)
        return jsonify({'token': access_token}), 200
    else:
        return jsonify({'message': 'Invalid credentials'}), 401

@app.route('/current_user', methods=['GET'])
@jwt_required()
def get_current_user():
    try:
        current_user_id = get_jwt_identity()
        current_user = User.query.get(current_user_id)
        
        if current_user:
            return jsonify({
                'email': current_user.email,
                'name': current_user.username,
                'location': current_user.location,
                'bio': current_user.bio
            }), 200
        else:
            return jsonify({'message': 'User not found'}), 404

    except Exception as e:
        return jsonify({'message': 'Internal server error', 'error': str(e)}), 500


# Get all users
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return users_schema.jsonify(users)

# Get all items
@app.route('/items', methods=['GET'])
def get_items():
    items = Item.query.all()
    return items_schema.jsonify(items)

# Get all categories
@app.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([{"id": category.id, "name": category.name} for category in categories]), 200

# Get all feedbacks
@app.route('/feedbacks', methods=['GET'])
def get_feedbacks():
    feedbacks = Feedback.query.all()
    return feedbacks_schema.jsonify(feedbacks)

# Get all orders
@app.route('/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    return jsonify([
        {
            "id": order.id,
            "title": order.title,
            "description": order.description,
            "price": order.price,
            "imageurl": order.imageurl,
            "category_id": order.category_id
        } for order in orders
    ]), 200


# Add items to the db
@app.route('/additems', methods=['POST'])
def add_item():
    data = request.get_json()
    new_item = Item(
        title=data['title'],
        description=data['description'],
        price=data['price'],
        imageurl=data['imageurl'],
        category_id=data['category_id']
    )
    db.session.add(new_item)
    db.session.commit()
    return item_schema.jsonify(new_item), 201

# Add user to the db / sign up
@app.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({'message': 'Invalid input'}), 400

    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    new_user = User(
        email=data['email'],
        password=hashed_password,
        username=data.get('username'),
        location=data.get('location'),
        bio=data.get('bio')
    )

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User created successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'User already exists or other error', 'error': str(e)}), 409

    


# Add feedback
@app.route('/addfeedbacks', methods=['POST'])
def add_feedback():
    data = request.get_json()
    new_feedback = Feedback(
        email=data['email'],
        name=data['name'],
        feedback=data['feedback'],
        item_id=data.get('item_id')  # include item_id if provided
    )
    db.session.add(new_feedback)
    db.session.commit()

    response = {
        "name": new_feedback.name,
        "email": new_feedback.email,
        "feedback": new_feedback.feedback
    }
    
    return jsonify(response), 201 

# Add order
@app.route('/addorders', methods=['POST'])
def add_order():
    data = request.get_json()
    # Create a new Order instance
    new_order = Order(
        title=data['title'],
        description=data['description'],
        price=data['price'],
        imageurl=data['imageurl'],
        category_id=data['category_id']
    )

    # Add items to the order if provided
    if 'item_ids' in data:
        items = Item.query.filter(Item.id.in_(data['item_ids'])).all()
        new_order.items.extend(items)

    # Add the new order to the session and commit
    db.session.add(new_order)
    db.session.commit()

    return jsonify(new_order.to_dict()), 201

# Update an item
@app.route('/updateitems/<int:id>', methods=['PUT'])
def update_item(id):
    item = Item.query.get_or_404(id)
    data = request.get_json()
    item.title = data.get('title', item.title)
    item.description = data.get('description', item.description)
    item.price = data.get('price', item.price)
    item.imageurl = data.get('imageurl', item.imageurl)
    item.category_id = data.get('category_id', item.category_id)
    db.session.commit()
    return item_schema.jsonify(item)

# Update a user
@app.route('/updateusers/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json()
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    user.location = data.get('location', user.location)
    user.bio = data.get('bio', user.bio)
    db.session.commit()
    return user_schema.jsonify(user)

# Delete an item by its id
@app.route('/deleteitems/<int:id>', methods=['DELETE'])
def delete_item(id):
    item = Item.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    return '', 204

# Delete a user by its id
@app.route('/deleteusers/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return '', 204

# Error handler
@app.errorhandler(404)
def resource_not_found(e):
    return jsonify(error=str(e)), 404

if __name__ == "__main__":
    app.run()
