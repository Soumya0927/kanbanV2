from flask import request
from flask_restful import reqparse, Resource, marshal, fields, abort
from flask_security import auth_required, SQLAlchemyUserDatastore, current_user, hash_password
from models import db, User, List, Role, Card
from werkzeug.exceptions import NotFound, Conflict, BadRequest
from flask_login import current_user
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import json
import data_access
from flask_celery1 import export_list, export_card
from flask_cache import cache

test = {
    'msg': fields.String
}

user_resourse_fields = {
    # "username": fields.String,
    "get_cards": {}

}
user_req = reqparse.RequestParser()
user_req.add_argument('email', required=True, help="email required")
user_req.add_argument('username', required=True, help="username required")
user_req.add_argument('password', required=True, help="password required")

user_datastore = SQLAlchemyUserDatastore(db, User, Role)


class user(Resource):
    @auth_required("token")
    def get(self):
        print(current_user)
        lists = data_access.get_list_by_userId(current_user.id)
        d = {}
        for each in lists:
            d[each.list_name] = []
            cards = Card.query.filter_by(list_id=each.lid).all()
            for c in cards:
                d[each.list_name].append({"cid": c.cid, "card_title": c.card_title,
                                         "content": c.content, "deadline": c.deadline, "flag": c.flag})
        print(d)
        # data = {'username': "hello", 'get_cards': d}
        # users = User.query.fi
        # data = {current_user.username, d}
        data = {"result": d, "username": current_user.username}
        return data  # marshal(d, user_resourse_fields)
    '''
        if id:
            return marshal(current_user, user_resourse_fields)
        else:
            abort(400, message='You are not authorized to get the resource')

    '''

    def post(self):
        data = user_req.parse_args()
        # data = request.get_json()

        '''if user_datastore.find_user(email=data['email']):
            raise Conflict'''
        user = user_datastore.create_user(
            username=data['username'], email=data['email'],
            password=hash_password(data['password']))
        print("users", user)
        db.session.add(user)
        db.session.commit()
        # return marshal(data, user_resourse_fields)


list_resourse_fields = {
    "list_name": fields.String,
    "description": fields.String,

}
all_list_resource_fields = {
    "lid": fields.Integer,
    "list_name": fields.String
}
error_resourse_fields = {
    "err_code": fields.String,
    "err_msg": fields.String,

}


class list(Resource):
    @auth_required("token")
    def get(self, lname=None):
        if lname:
            ulist = List.query.filter_by(
                user_id=current_user.id, list_name=lname).first()
            if not ulist:
                raise NotFound("Data not found")
            else:
                # print(json.dumps(marshal(ulist, list_resourse_fields)))
                return marshal(ulist, list_resourse_fields)
        else:
            lists = data_access.get_list_by_userId(current_user.id)
            alllist = []
            for list in lists:
                alllist.append(marshal(list, all_list_resource_fields))

            return {"result": alllist}

        # return marshal({'msg': 'Hello from Api'}, test)

    def post(self):
        userlist = data_access.get_list_by_userId(current_user.id)
        data = request.get_json()
        print(data)
        # l_name = request.form['Lname']
        # l_desc = request.form['desc']
        found = False
        for l in userlist:
            if (l.list_name == data['lname']):
                found = True
                data = {'err_code': 400, 'err_msg': "already exist"}
            # return marshal(data, error_resourse_fields)
        if not found:
            createlist = List(
                list_name=data['lname'], description=data['desc'], user_id=current_user.id)
            print(createlist)
            db.session.add(createlist)
            db.session.commit()
            cache.delete_memoized(data_access.get_list_by_userId)

    def put(self, lname=None):
        if not lname:
            raise BadRequest

        data = request.get_json()
        List.query.filter_by(user_id=current_user.id, list_name=lname).update(
            {'list_name': data['lname'], 'description': data['desc']})
        db.session.commit()

    def delete(self, lname=None):
        curlist = List.query.filter_by(
            list_name=lname, user_id=current_user.id).first()
        cards = Card.query.filter_by(list_id=curlist.lid).all()
        # lname = curlist.list_name
        for card in cards:
            db.session.delete(card)
        db.session.delete(curlist)
        db.session.commit()
        cache.delete_memoized(data_access.get_list_by_userId)


class downloadTask(Resource):
    @auth_required("token")
    def get(self, lname=None, id=None):
        if lname:
            list = List.query.filter_by(
                list_name=lname, user_id=current_user.id).first()
        # print("Tracker ID")
        # print(tracker_id)
            export_list.delay(current_user.id, list.lid)
        if id:
            card = data_access.get_card_by_id(id)
            export_card.delay(current_user.id, card.cid)


class summary(Resource):
    @auth_required("token")
    def get(self):
        plotlist = {}
        lists = data_access.get_list_by_userId(current_user.id)
        for l in lists:
            plotlist[l.list_name] = []
            comp, incomp, deadpass = 0, 0, 0
            cards = Card.query.filter_by(list_id=l.lid).all()
            for c in cards:

                if c.flag == "1":
                    comp += 1
                else:
                    incomp += 1
                today = datetime.today()
                deadl = datetime.strptime(
                    c.deadline, "%Y-%m-%d").strftime("%Y-%m-%d")
                newdate1 = datetime.strptime(deadl, "%Y-%m-%d")
                if newdate1 < today:
                    deadpass += 1
            label = ["completed", "not completed", "deadline passed"]
            datasets = [comp, incomp, deadpass]

            plotlist[l.list_name] = datasets
            # plotlist[l.list_name].append(
            #     {"Completed": comp, "Incompleted": incomp, "deadline": deadpass})
        print(plotlist)
        return plotlist


card_resource_fields = {
    "cid": fields.Integer,
    "card_title": fields.String,
    "content": fields.String,
    "deadline": fields.String,
    "flag": fields.String,
    "list_id": fields.Integer,
    "last_change": fields.String,
    "card_created": fields.String

}


class card(Resource):
    @auth_required('token')
    def get(self, id=None):
        if id:
            card = data_access.get_card_by_id(id)
        print(card)
        return marshal(card, card_resource_fields)

    def post(self, lname=None, cid=None):
        data = request.get_json()
        created = datetime.now()
        list = List.query.filter_by(
            user_id=current_user.id, list_name=lname).first()
        card = Card(card_title=data['Title'], content=data['Content'], card_created=created,
                    # data['list_id']
                    deadline=data['Deadline'], list_id=list.lid, flag=data['Flag'])
        db.session.add(card)
        db.session.commit()

    def put(self, id=None):
        if not id:
            raise BadRequest
        data = request.get_json()
        Card.query.filter_by(cid=id).update({'card_title': data['Title'], 'content': data['Content'],
                                             'deadline': data['Deadline'], 'flag': data['Flag'],
                                             'list_id': data['list_belong']})
        db.session.commit()

    def delete(self, id=None):
        c = data_access.get_card_by_id(id)
        # c = Card.query.filter_by(cid=id).first()
        db.session.delete(c)
        db.session.commit()
        cache.delete_memoized(data_access.get_card_by_id)
