import random,os,json,requests
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request,render_template,make_response,abort,redirect,flash,session,url_for,send_from_directory,jsonify
from werkzeug.utils import secure_filename
from money import Money
from PIL import Image
from ppackage.myforms import ContactForm, LoginForm, Usersignup,Payment
from ppackage import app, db, mail, Message, csrf
from ppackage.models import User,Product, Skills, Profile, member_skills,Items,Transaction

# from werkzeug.datastructures import Comb
# @csrf.exempt
# @app.route('/submitcontact/', methods=['GET', 'POST'])
# def submitcontact():
#     data = "<select><option>Lagos</option></select>"
#     return data

@app.route('/search/')
def search():
    return render_template("search.html")

@csrf.exempt
@app.route('/searchre/', methods=['GET', 'POST'])
def searchre():
    fordata = request.args.get('fordata')
    data = db.session.query(Profile.fname,Profile.lname).filter(Profile.email==fordata).first()
    json_data = json.dumps(data)
    dataobj = make_response(json_data,200)
    dataobj.headers['content-type']="application/json"
    return dataobj
    # if data:
    #     return f"This email '{fordata}', has been registered, pls log in to continue"
    # else:
    #     return "Email is available"

@app.route("/pay/", methods=['GET','POST'])
def payment():
    if request.method=='GET':
        form=Payment()
        items = db.session.query(Items).all()
        return render_template("payment.html", form=form, items=items)
    else:
        customer = request.form['custname']
        email = request.form['email']
        phone = request.form['phone']
        prodid = request.form['product']
        deets = db.session.query(Items).get(prodid)
        amt = deets.item_amt
        trans_ref = random.random()
        trans_obj = Transaction(trans_status=0,trans_amt=amt,trans_phone=phone,trans_email=email,trans_customer=customer, trans_ref=trans_ref,trans_productid=prodid)
        db.session.add(trans_obj)
        db.session.commit()
        session['trans_id'] = trans_obj.trans_id
        return redirect("/makepay/")

@csrf.exempt
@app.route('/makepay/', methods=['GET','POST'])
def makepay():
    trans_id = session['trans_id']
    if request.method=='GET':
        transaction_details = db.session.query(Transaction).get(trans_id)
        productid = transaction_details.trans_productid
        productname = db.session.query(Items).get(productid)
        return render_template('makepay.html', deets = transaction_details, productname=productname)
    else:
        trx_details = db.session.query(Transaction).get(trans_id)
        amt = trx_details.item.item_amt*100
        custemail = trx_details.trans_email
        headers = {
            "content-Type":"application/json",
            "authorization":"Bearer sk_test_b70964efeb5bb89e57244b23052294150dc14b46"
        }
        data = {
            "reference":trx_details.trans_ref,
            "amount":amt,
            "email":custemail
        }
        response = requests.post("https://api.paystack.co/transaction/initialize", headers=headers, data=json.dumps(data))
        rsp= response.json()
        accesscode = rsp['data']['access_code']
        url  = rsp['data']['authorization_url']
        return redirect(url)

@app.route("/landing/")
def landing():
    headers = {"Content-Type":"application/json", "Authorization":"Bearer sk_test_b70964efeb5bb89e57244b23052294150dc14b46"}
    trans_ref = request.args.get('trxref')
    response = requests.get('https://api.paystack.co/transaction/verify/' + trans_ref, headers=headers)
    rsp = response.json()
    if rsp['status']== True:
        return render_template("landing.html", response=rsp, headers=headers)
    else:
        return render_template("landing.html", response=rsp,headers=headers)





@csrf.exempt
@app.route("/loadamt/", methods=['POST'])
def getamount():
    id = request.form['itemid']
    amt= db.session.query(Items).get(id)
    if amt != None:
        formatted = Money(amount=amt.item_amt, currency='NGN')
        return str(formatted)
    else:
        return "You have to make a choice"

@app.route('/contactus/')
def contact():
    return render_template('contactus.html')

@app.route('/example/')
def example():
    deal = '{"no":1, "description":"40% discount on orders of 10,000 naira and above"}'
    deal_dict = json.loads(deal)
    python_tup = ('23','45','14','54')
    json_equiv = json.dumps(python_tup)
    return render_template('test.html', deal_dict=deal_dict, json_equiv=json_equiv)

@app.route('/')
@app.route('/home/')
def home():
    return render_template('bootstrap.html')

@app.route('/allmembers/')
def allmembers():
    # using method 1 to get from database and applying filter
    # members = Profile.query.all()
    members = db.session.query(Profile).all()
    return render_template("report.html", members=members)

@app.route('/signup/', methods=['GET','POST'])
def signup():
    form = Usersignup()
    allskills = db.session.query(Skills).all()
    if request.method == "GET":
        return render_template('signup.html', form=form, allskills=allskills)
    else:
        if form.validate_on_submit():
            data = db.session.query(Skills).all()
            ppt = request.files['photo'] #FileStorage
            name, ext = os.path.splitext(ppt.filename)
            newname = secure_filename(name)+ str(random.random()) + ext
            ppt.save(app.config['UPLOAD_FOLDER'] + newname)
            
            pillowobj = Image.open(app.config['UPLOAD_FOLDER'] + newname)
            pillowobj.thumbnail((240, 240))
            newname = newname + str(random.random()) + ext
            pillowobj.save(app.config['UPLOAD_FOLDER']+ newname)
            if data != None:
                # signup query
                skills = request.form.getlist('skills')
                fname = request.form['firstname']
                lname = request.form['lastname']
                email = request.form['email']
                pwd = request.form['pwd']
                profileobj = Profile(fname=fname,lname=lname,email=email,pwd=pwd,photo=newname)
                db.session.add(profileobj)
                db.session.commit()
                # Email Sending
                rep = request.form['email']
                msg = Message(subject='Welcome to Starter', sender='Starter.com', recipients=[rep])
                msg.html = "<h4>Welcome to Starter Bootstrap</h4> <br> Proceed to your page to continue. <br> This is a test email using python"
                mail.send(msg)
                # Session
                membid = profileobj.profileid
                session['memberid'] = membid
                # inserting into association table. Mehtod 2
                if skills:
                    for s in skills:
                        statement = member_skills.insert().values(memberid=membid, skill_id=s)
                        db.session.execute(statement)
                        db.session.commit()

                # optional validation
                # else:
                #     flash('You should choose at least one skill')

                # set session
                session['name'] = request.form['firstname']
                return redirect(url_for('profile'))
            else:
                flash('Complete all fields')
                return render_template('signup.html', form=form, allskills=allskills)
        else:
            return render_template('signup.html', form=form, allskills=allskills)
        return "Added Successfully"

@app.route('/details/<userid>')
def userdetails(userid):
    members = db.session.query(Profile).filter(member_skills.c.memberid==1).all()

    membskills = db.session.query(member_skills,Skills).join(Skills).filter(member_skills.c.memberid==userid).all()
    return render_template("userdetails.html", membskills=membskills, members=members)

@app.route('/skills/')
def skills():
    allskills = db.session.query(Skills).join(member_skills).all()
    return render_template("skills.html", allskills=allskills)

@app.route('/profile/')
def profile():
    if session.get('name'):
        id = session['memberid']
        return render_template('profile.html', id=id)
    else:
        return redirect('/login/')

@app.route('/login/', methods=['GET','POST'])
def login():
    form = LoginForm()
    
    if request.method == 'GET':
        return render_template('login.html',form=form)
    else:
        if form.validate_on_submit():
            data = db.session.query(Profile).filter(Profile.email == request.form['email'], Profile.pwd == request.form['pwd']).first()
            if data != None:
                membid = data.profileid
                session['memberid'] = membid
                session['name'] = data.fname
                return redirect(url_for('profile'))
            else:
                flash('Invalid Login Details')
                return render_template('login.html', form=form)
        else:
            return render_template('login.html', form=form)

@app.route('/uploads/<path:filename>')
def download_file(filename):
    return send_from_directory('../' + app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

@app.route('/editprofile/<int:profileid>')
def editprofile(profileid):
    form = Usersignup()
    id = session['memberid']
    data = db.session.query(Profile).filter(Profile.profileid==id).first()
    
    return render_template("editprofile.html", id=id, form=form, data=data)

# handles profile editing inserting to database
@app.route('/update/', methods=['POST'])
def update():
    if session.get('name'):
        form = Usersignup()
        id = session['memberid']
        data = db.session.query(Profile).get(id)
        data.email = request.form['email']
        data.pwd = request.form['pwd']
        db.session.commit()
        return render_template("editprofile.html", id=id, form=form, data=data)
    else:
        return redirect("/login/")

@app.route('/deals/')
def deals():
    response= response.get("http://127.0.0.1:8000/deal/api/v1.0/list", auth=())

@app.route('/logout/')
def logout():
    if session.get('name'):
        session.pop('name')
        session.pop('memberid')
    return redirect('/login/')


# @app.route('/aboutus/')
# def about():
    
#     return render_template('about.html')

# @app.route('/products/')
# def products():
#     return render_template('products.html')

# @app.route('/stores/')
# def store():
#     return render_template('store.html')

# @app.route("/contactus/")
# def contacts():
#     formdata= ContactForm()
#     return render_template('contactus.html',formdata=formdata)

# @app.route("/formsubmit/",methods=["POST"])
# def formsubmit():
#     form= ContactForm()
#     if form.validate_on_submit():
#         username=request.form['name']
#         session['name']=username
#         session.get('name')
#         return redirect('profile', username=username)
        
#         # return "Thank You for filling all required fields"
#     else:
#         return render_template('contactus.html', formdata=form)




# # @app.route('/test/<username>/<pwd>')
# # def test(username,pwd):
# #     if username == 'ola' and pwd == '1234':

# #         return redirect("/profile/")

# #         # obj = make_response("This is a Mimic Not Found",404)
# #         # obj.headers['content-encoding'] = 'text/plain-html'

# #         # return obj
# #     else:
# #         return redirect("/login")
# #         # abort(403)

        
# @app.route('/profile/', methods=['GET','POST'])
# def profile():
#     return render_template('profile.html')


# # @app.route('/login/', methods=['GET','POST'])
# # def check():
# #     if request.method=='GET':
# #         return render_template('form.html')
# #     else:
# #         username=request.form['username']
# #         pwd=request.form['pwd']
# #         msg=f'Welcome {username}'
# #         if username=='ola' and pwd=='1234' :
# #             session['username']=username
# #             name = session.get('username')
# #             return 
# #             # resp = make_response(render_template('profile.html', msg=msg))
# #             # resp.set_cookie('userID', username)
# #             # return resp
# #             # cook= request.cookies.get('UserID')
# #             # return cook
# #         else:
# #             flash('Invalid Login details.')
# #             return redirect('/login/')
        
# @app.route("/logout/")
# def logout():
#     session.pop('name')
#     return "You have been successfully logged out"

@app.errorhandler(404)
def error(error):
    return render_template('404error.html', error=error),404