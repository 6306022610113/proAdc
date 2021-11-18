from flask import Flask, config, render_template, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datatables import ColumnDT, DataTables
import datetime
import random
import requests

app = Flask(__name__)

api = 'https://covid19.ddc.moph.go.th/api/Cases/today-cases-by-provinces'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://webadmin:RALgta80961@node17340-lalana.app.ruk-com.cloud:5432/mydb'
db = SQLAlchemy(app)

res = requests.get(api)
pokedc = res.json()

class User(db.Model) :
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    province = db.Column(db.String(400))
    total_case = db.Column(db.String(100))
    new_case = db.Column(db.String(100))
    total_death = db.Column(db.String(100))
    new_death = db.Column(db.String(100))
    txn_date = db.Column(db.String(100))
@app.route('/', methods=['GET', 'POST'])
def index() :
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/typecovid')
def typecovid():
    return render_template('typecovid.html')

@app.route('/vaccine')
def vaccine():
    return render_template('vaccine.html')

@app.route('/load_table_sql', methods=['GET', 'POST'])
def load_table_sql() :
    columns = [
        ColumnDT(User.id),
        ColumnDT(User.province),
        ColumnDT(User.total_case),
        ColumnDT(User.new_case),
        ColumnDT(User.total_death),
        ColumnDT(User.new_death),
        ColumnDT(User.txn_date)
    ]
    query = db.session.query().select_from(User)
    rowTable = DataTables(request.args.to_dict(), query, columns)
    # returns what is needed by DataTable
    return rowTable.output_result()
    

def create_db_user() :
    db.drop_all()
    db.create_all()
    for i in pokedc :

        user = User(province=''+str(i['province']), total_case= ''+str(i['total_case']), new_case= ''+str(i['new_case']), 
                    total_death = ''+str(i['total_death']), new_death= ''+str(i['new_death']), txn_date= ''+str(i['txn_date']))
        db.session.add(user)
    db.session.commit()
    print('create done')


create_db_user()

if __name__ == "__main__" :
    app.run(host='0.0.0.0', debug=True, port=80)