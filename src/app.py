from flask import Flask, render_template, request, redirect, url_for
import os
import database as db

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'src', 'templates')

app = Flask(__name__, template_folder = template_dir)


#Rutas de la aplicacion
@app.route('/')
def home():
    cursor = db.database.cursor()
    cursor.execute("SELECT * FROM users")
    myresult = cursor.fetchall()
    #Convertir los datos a diccionario
    insertObjetc = []
    columnNames = [column[0] for column in cursor.description]
    for record in myresult:
        insertObjetc.append(dict(zip(columnNames, record)))
    cursor.close()
    return render_template('index.html', data=insertObjetc)

#Ruta para guardar usuarios en la base de datos
@app.route('/user', methods = ['POST'])
def addUser():
    serie = request.form['serie']
    name = request.form['name']
    place = request.form['place']

    if serie and name and place:
        cursor = db.database.cursor()
        sql = "INSERT INTO users (serie, name, place) VALUES (%s, %s, %s)"
        data = (serie, name, place)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('home'))

@app.route('/delete/<string:id>')
def delete(id):
    cursor = db.database.cursor()
    sql = "DELETE FROM users WHERE id=%s"
    data = (id,)
    cursor.execute(sql, data)
    db.database.commit()
    return redirect(url_for('home'))

@app.route('/edit/<string:id>', methods=['POST'])
def edit(id):
    serie = request.form['serie']
    name = request.form['name']
    place = request.form['place']

    if serie and name and place:
        cursor = db.database.cursor()
        sql = "UPDATE users SET serie = %s, name = %s, place = %s WHERE id = %s"
        data = (serie, name, place, id)
        cursor.execute(sql, data)
        db.database.commit()
    return redirect(url_for('home'))




if __name__ =='__main__':
    app.run(debug=True, port=4000)
