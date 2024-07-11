from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

# contains definitions of tables and associated schema constructs
# read more about Metadata using the link at the bottom of the page
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

# create the Flask SQLAlchemy extension
db = SQLAlchemy(metadata=metadata)

# Models go here!
#Association table to store many-to-many relationship

item_order = db.Table(
    'items_orders',
    metadata,
    db.Column('item_id', db.Integer, db.ForeignKey('items.id'), primary_key=True),
    db.Column('order_id', db.Integer, db.ForeignKey('orders.id'), primary_key=True)
)

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False )
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.String(350), nullable=False)

    def __repr__(self):
        return f'<User {self.username}, {self.email}, {self.password}, {self.location}, {self.bio}>'

    #One to many with the order 
    orders = db.relationship('Order', back_populates="user", cascade = "all,delete-orphan")


class Category(db.Model):
    __tablename__ = "categorys"

    id = db.Column(db.Integer, primary_key=True)
    name =db.Column(db.String, unique=True, nullable=False) 

    #One to many with the item 
    items = db.relationship('Item', back_populates="category", cascade = "all,delete-orphan")

    def __repr__(self):
        return f'<Category {self.id}, {self.name}>'


class Item(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    price = db.Column(db.Float, nullable=False)
    imageurl = db.Column(db.String, nullable=False)
    
    #One to many with the feedbacks
    feedbacks = db.relationship('Feedback', back_populates="items", cascade = "all,delete-orphan")

    #Foreign key to store the category id
    category_id = db.Column(db.Integer, db.ForeignKey('categorys.id'))
    #Relationship mapping the item to the category
    category = db.relationship('Category', back_populates="items")

    #Relationship mapping item to related order(m-m)
    orders = db.relationship('Order', secondary=item_order, back_populates='items')
    
    def __repr__(self):
        return f'<Item {self.id}, {self.title}, {self.description}, {self.price}, {self.imageurl}>'


class Order(db.Model):
    __tablename__ = "orders"

    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String, nullable=False)

    #Foreign key to store the users id
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    #Relationship mapping the order to the user
    user = db.relationship('User', back_populates="orders")
    #Relationship mapping item to related order
    items = db.relationship('Item', secondary=item_order, back_populates='orders')

    def __repr__(self):
        return f'<Order {self.id}, {self.quantity}, {self.status}>'


class Feedback(db.Model):
    __tablename__ = "feedbacks"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    feedback = db.Column(db.String, nullable=False)

    #Foreign key to store the category id
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'))
    #Relationship mapping the item to the category
    items = db.relationship('Item', back_populates="feedbacks")

    def __repr__(self):
        return f'<Feedback {self.id}, {self.email}, {self.name}, {self.feedback}>'