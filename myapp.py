from flask import Flask,request

app = Flask(__name__)

@app.route('/home/products/')
@app.route('/home/products/<int:productname>')
def products(productname):
    # return "Hello World!!!"
    if productname == "beans":
        return "We have Beans"
    elif productname == "rice":
        return "We have Rice"
    else:
        return f"We do not have {productname}"


#multi-routing is possible

@app.route('/')
@app.route('/home/')
def home():
    return "Welcome Home"

@app.route('/hello/',methods=['POST','GET'])
def hello():
    if request.method == 'GET':
        return "Login Form Here"
    else:
        return "Submitted Successfully"
    
    return 'Hello home'


@app.route('/about/')
def page():
    return "This is the about us page"

if __name__ == '__main__':
    app.run(debug=True, port=8080)