import sqlite3 as sql
from peewee import *
from flask import Flask, render_template, request, url_for, redirect, flash

app = Flask(__name__)

global appType 
appType = 'Monolith'

database = SqliteDatabase('carsweb.db')

class BaseModel(Model):
     class Meta:
        database = database

class TBCars(BaseModel):
    carname = CharField()
    carbrand = CharField()
    carmodel = CharField()
    carprice = CharField()

def create_tables():
    with database:
        database.create_tables([TBCars])

@app.route('/')
def indeks():
    return render_template('index.html', appType=appType)

@app.route('/createcar')
def createcar():
    return render_template('createcar.html', appType=appType)

@app.route('/createcarsave',methods=['GET','POST'])
def createcarsave():
    fName = request.form['carName']
    fBrand = request.form['carBrand']
    fModel = request.form['carModel']
    fPrice = request.form['carPrice']

    viewData = {
        "name" : fName,
        "brand" : fBrand,
        "model" : fModel,
        "price" : fPrice 
    }

    #simpan di DB
    car_simpan = TBCars.create(
        carname = fName,
        carbrand = fBrand,
        carmodel = fModel,
        carprice = fPrice
        )
    return redirect(url_for('readcar'))

@app.route('/readcar')
def readcar():
    rows = TBCars.select()
    return render_template('readcar.html', rows=rows, appType=appType)

@app.route("/updatecar/<string:id>",methods=['POST','GET'])
def updatecar(id):
    if request.method=='POST':
        fName=request.form['carName']
        fBrand=request.form['carBrand']
        fModel=request.form['carModel']
        fPrice=request.form['carPrice']
        
        con=sql.connect("carsweb.db")
        cur=con.cursor()
        cur.execute("update tbcars set carname=?, carbrand=?, carmodel=?, carprice=? where id=?",(fName,fBrand,fModel,fPrice,id))
        con.commit()
        flash('TBCars Updated','success')
        return redirect(url_for("readcar"))
        
    con=sql.connect("carsweb.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select * from tbcars where id=?",(id))
    row=cur.fetchone()
    return render_template("updatecar.html", appType=appType, rows=row)

@app.route('/deletecar')
def deletecar():
    return render_template('deletecar.html', appType=appType)

@app.route('/deletecarsave', methods=['GET','POST'])
def deletecarsave():
    fName = request.form['carName']
    car_delete = TBCars.delete().where(TBCars.carname==fName)
    car_delete.execute()
    return redirect(url_for('readcar'))

@app.route('/searchcar')
def searchcar():
    car_search = TBCars.select()
    return render_template('searchcar.html', appType=appType, car_search=car_search)

@app.route('/searchCarSave', methods=['GET', 'POST'])
def searchCarSave():
    
    inputSearch = request.form['formSearchInput']
    car_search = TBCars.select().where(TBCars.carname.contains(inputSearch) | TBCars.carbrand.contains(inputSearch) )
    car_search.execute()
    return render_template(
        'searchcar.html',
        car_search=car_search,
        appType=appType
        )

if __name__ == '__main__':
    app.secret_key='admin123'
    app.run(
        host='0.0.0.0',
        debug = True
        )


