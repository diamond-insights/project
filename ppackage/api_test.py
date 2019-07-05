#FORM
class Payment(FlaskForm):
    custname = StringField("Customer Fullname: ", validators=[DataRequired(message='Pls fill this field')])
    email = StringField("Email: ", validators=[DataRequired(message='Pls fill this field'),Email()])
    phone = StringField("Phone: ", validators=[DataRequired(message='Pls fill this field')])
    submit = SubmitField("Sign Up Now")


# MODELS

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
    trans_productid = db.Column(db.Integer(), db.ForeignKey('product.prod_id'))


class Items(db.Model):
    item_id = db.Column(db.Integer(), primary_key=True)
    item_amt = db.Column(db.Integer())
    item_name = db.Column(db.String(255), nullable=False)
    # the relationship can be used to retrieve many instances of the child class
    transactions = db.relationship('Transaction', backref='item')


#TEMPLATE

<html>
    <head>
        <title>Payment Page</title>
         <!-- Bootstrap core CSS -->
    <link href="{{ url_for('static', filename='vendor/bootstrap/css/bootstrap.min.css')}}" rel="stylesheet">

    </head>

    <body>
     <form action="#" method="POST">
         <div class="form-group">
             <label></label>
             
         </div>
     </form>

    
    </body>
</html>