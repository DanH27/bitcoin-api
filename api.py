import flask
from flask import request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flaskext.mysql import MySQL
from datetime import datetime

app = flask.Flask(__name__)
app.config["DEBUG"] = True
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:root@localhost/bitrade'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://teopiqfwhkgadm:b39ab93fd66a7c02bf68417cc1dc62d67ed9fb1b68b51939908978c2f12bc11a@ec2-54-163-245-64.compute-1.amazonaws.com:5432/d72h6r5qn3sd0'

db = SQLAlchemy(app)



class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    currency = db.relationship('Currency', backref='owner', lazy=True)
    admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Currency(db.Model):
    __tablename__ = 'currency'
    id = db.Column(db.Integer, primary_key=True)
    btc = db.Column(db.Integer(), nullable=False, default=0)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    cash = db.Column(db.Integer, nullable=False, default=100000)

    def __repr__(self):
        return f"Currency('{self.btc}', '{self.date_posted}'"

@app.route('/api/users', methods=['GET'])
def allUsers():
    usernames = {}
    budget_tmp = User.query.all()
    for item in budget_tmp:
        usernames[str(item.id)] = {}
    for item in budget_tmp:
        usernames[str(item.id)]['username'] = str(item.username)
        usernames[str(item.id)]['email'] = str(item.email)
    print(usernames)
    return jsonify(usernames)


#Get one username
@app.route('/api/user/<user_id>', methods=['GET'])
def getuser(user_id):
    user_dict = {}
    user = User.query.filter_by(id=user_id).first()
    if user == None:
        return '404 User Not Found'
    user_dict[str(user.id)] = {}
    user_dict[str(user.id)]['username'] = str(user.username)
    user_dict[str(user.id)]['email'] = str(user.email)
    print(user_dict)


    return jsonify(user_dict)

#Get all currency trades
@app.route('/api/bitcoins/', methods=['GET'])
def gettrades():
    trades_dict = {}
    trades = Currency.query.all()

    for trade in trades:
        trades_dict[str(trade.user_id)] = {}
    for trade in trades:
        trades_dict[str(trade.user_id)]['btc'] = str(trade.btc)

    return jsonify(trades_dict)


#Get specific user btc amt
@app.route('/api/bitcoins/<id>', methods=['GET'])
def gettrade(id):
    trade_dict = {}
    trade = Currency.query.filter_by(user_id=id).all()
    last_trade = trade[len(trade) - 1]
    trade_dict[str(last_trade.user_id)] = {}
    trade_dict[str(last_trade.user_id)]['btc'] = str(last_trade.btc)

    return jsonify(trade_dict)

#Delete User
@app.route('/api/user/<d_user_id>', methods=['DELETE'])
def deleteUser(d_user_id):
    user = User.query.filter_by(id=d_user_id).first()
    if user == None:
        return 'User not found - delete unsucessful'
    else:
        currency = Currency.query.filter_by(user_id=d_user_id).all()
        for currency1 in currency:
            db.session.delete(currency1)
        db.session.delete(user)
        db.session.commit()
        return 'User deleted'


if __name__ == '__main__':
    app.run(debug=True)
