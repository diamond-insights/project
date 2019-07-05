import random,os,json
from flask import request,render_template,make_response,abort,redirect,flash,session,url_for,send_from_directory,jsonify
from flask_httpauth import HTTPBasicAuth
auth = HTTPBasicAuth()
import requests
from ppackage import app,csrf,db
from ppackage.models import Deal,Profile

@auth.get_password
def get_password(email):
    deets = db.session.query(Profile.pwd).filter(Profile.email==email).first()
    if deets:
        return deets.pwd
    else:
        return None
    
@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error':'Unauthorized access'}), 401)

@csrf.exempt
@app.route("/deal/api/v1.0/add/", methods=['POST','GET'])
def add_deal():
    # data  = request.json
    data=request.get_json(force=True)
    if 'dealname' in data:
        dealname=data['dealname']
        dealurl=data['deal_url']
        # insert into Deal Table
        dealobj=Deal(deal_name=dealname, deal_url=dealurl)
        db.session.add(dealobj)
        db.session.commit()
        # check if isertion was successful
        dealid = dealobj.id
        if dealid:
            rsp = {"status":"OK", "msg":"Deal Added!"}
            return jsonify(rsp)
        else:
            rsp = {"status":"FAILED", "msg":"Database Error"}
            return jsonify(rsp)
    else:
        rsp = {"status":"FAILED", "msg":"Wrong Input"}
        return jsonify(rsp)

@app.route("/deal/api/v1.0/list/", methods=['GET'])
def listdeal():
    data = db.session.query(Deal.deal_name,Deal.deal_url, Deal.id).all()
    # newdata = jsonify(data)
    deal_json = jsonify(data)
    return deal_json

@app.route("/deal/api/v1.0/delete/<int:id>/", methods=['GET'])

def delete_deal(id):
    deal = db.session.query(Deal).get(id)
    if deal !=None:
        db.session.delete(id)
        db.session.commit()
        rsp = {"status":"OK", "msg":"Successfully Deleted"}
    else:
        {"status":"FAILED", "msg":"Not Found"}
    return rsp

@csrf.exempt
@app.route("/deal/api/v1.0/edit/<int:id>", methods=['PUT'])
@auth.login_required
def edit_deal(id):
    deal = db.session.query(Deal).get(id)
    data = request.get_json(force=True)
    if deal != None:
        deal.deal_name = data['dealname']
        db.session.commit()
        rsp = {"status":"OK", "msg":"Successfully Edited"}
    else:
        rsp = {"status":"FAILED", "msg":"Not Found"}
    return jsonify(rsp)
