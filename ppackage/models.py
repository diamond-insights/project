from datetime import datetime
from ppackage import db

class User(db.Model):
    __tablename__ = 'users'
    userid = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    pwd = db.Column(db.String(50), nullable=False)
    user_created_on = db.Column(db.DateTime(), default=datetime.utcnow())

    def __repr__(self):
        return "<{}>:{}>".format(self.userid, self.username)

member_skills = db.Table('member_skills',
db.Column('memberid',db.Integer(), db.ForeignKey('profile.profileid'), primary_key=True),
db.Column('skill_id', db.Integer(),db.ForeignKey('skills.id'), primary_key=True, nullable=True)
)

class Profile(db.Model):
    __tablename__ = 'profile'
    profileid = db.Column(db.Integer(), primary_key=True)
    fname = db.Column(db.String(50), nullable=False)
    lname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable = False)
    pwd = db.Column(db.String(50), nullable=False)
    photo = db.Column(db.String(200), nullable=False)
    user_created_on = db.Column(db.DateTime(), default=datetime.utcnow())
    #relationship
    skills = db.relationship("Skills", secondary="member_skills", backref=db.backref('members'))





class Skills(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    skill_name = db.Column(db.String(255), nullable=True)


class Product(db.Model):
    ''' the child class, parent is Category '''
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(64), index=True, unique=True)
    product_price = db.Column(db.String(120), index=True, unique=True)
    # create a Foreign Key Column
    product_category = db.Column(db.Integer(),  db.ForeignKey('category.id'))

class Category(db.Model):
    ''' The Parent Class, we only define relationship here '''
    __tablename__ = 'category'
    id = db.Column(db.Integer,primary_key=True)
    category_name = db.Column(db.String(50), nullable=False)
    # the relationship can be used to #retrieve many instances of the child #class
    products = db.relationship('Product', backref='category')

class Deal(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    deal_name = db.Column(db.String(255), nullable=False)
    deal_url = db.Column(db.String(255), nullable=False)
    deal_created_on = db.Column(db.DateTime, default=datetime.utcnow(), nullable=False)

class Transaction(db.Model):
    trans_id = db.Column(db.Integer(), primary_key=True)
    trans_status = db.Column(db.Integer())
    trans_date = db.Column(db.DateTime(), default=datetime.utcnow)
    trans_phone = db.Column(db.String(255))
    trans_amt = db.Column(db.Integer()) 
    trans_customer = db.Column(db.String(255), nullable=False)
    trans_ref = db.Column(db.String(255))
    trans_paystackref = db.Column(db.String(255))
    trans_others = db.Column(db.Text())
    trans_email = db.Column(db.String(255), nullable=False)

    # create a Foreign Key Column
    trans_productid = db.Column(db.Integer(), db.ForeignKey('items.item_id'))

class Items(db.Model):
    item_id = db.Column(db.Integer(), primary_key=True)
    item_amt = db.Column(db.Integer())
    item_name = db.Column(db.String(255), nullable=False)
    item_desc = db.Column(db.String(255), nullable=False)
    # the relationship can be used to retrieve many instances of the child class
    transactions = db.relationship('Transaction', backref='item')