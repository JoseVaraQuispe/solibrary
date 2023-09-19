from flask import Flask, render_template, request, url_for, redirect, flash
from flask_mysqldb import MySQL

#mysql coneccion
app = Flask(__name__)
app.config['MYSQL_HOST'] = '13.93.196.155'
app.config['MYSQL_USER'] = 'TA1'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'library'
mysql = MySQL(app)

#settins
app.secret_key = 'mysecreykey'

#LECTORES
@app.route('/')
def index():    
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM lector')
    data = cur.fetchall()
    return render_template('index.html', lectores = data)
@app.route('/add', methods = ['POST'])
def add():
    if request.method == 'POST':
        try:
            dni = request.form['dni']
            nombres = request.form['nombres']
            apellidos = request.form['apellidos']
            numero = request.form['numero']
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO lector(dni, nombres, apellidos, numero) VALUES(%s,%s,%s,%s)',
            (dni, nombres, apellidos, numero))
            mysql.connection.commit()
            flash('contacto agregado exitosamente')
            return redirect(url_for('index'))
        except:
            flash('Dni invalido')
            return redirect(url_for('index'))

@app.route('/edit/<dni>')
def get_lector(dni):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM lector WHERE dni = {0}'.format (dni))
    data = cur.fetchall()
    #print(data[0])
    return render_template('edit_lector.html', lector = data[0])
@app.route('/update/<dni>', methods =['POST'])
def update_lector(dni):
    if request.method == 'POST':
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        numero = request.form['numero']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE lector  
            SET nombres = %s,
                apellidos = %s,
                numero = %s
            WHERE dni = %s    
        """,(nombres, apellidos, numero, dni))
        mysql.connection.commit()
        flash('contacto editado exitosamente')
        return redirect(url_for('index'))
@app.route('/delete/<string:dni>')
def delete(dni):
    cur = mysql.connection.cursor()
    try:
        cur.execute('DELETE FROM lector WHERE dni = {0}'.format (dni))
        mysql.connection.commit()
        flash('contacto removido exitosamente')
        return redirect(url_for('index'))
    except:
        flash('No se puede eliminar hasta que devuelva el libro')
        return redirect(url_for('index'))


#LIBROS
@app.route('/Libros')
def Libros(): 
    cur = mysql.connection.cursor()
    cur.execute("""
    SELECT libros.id, libros.titulo, libros.editorial, autores.nombre, autores.apellido  
    FROM libros 
    JOIN autores ON libros.id_autor = autores.id 
    ORDER BY libros.id
    """)
    data = cur.fetchall()
    return render_template('Libros.html', lista_libros = data)

@app.route('/Add_Libros', methods = ['POST'])
def Add_Libros():
    if request.method == 'POST':
        try:
            id_autor = request.form['Idautor']
            titulo = request.form['Titulo']
            editorial = request.form['Editorial']
            fecha_lanzamiento = request.form['Fecha']
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO libros(id_autor, titulo, editorial, fecha_lanzamiento) VALUES(%s,%s,%s,%s)', (id_autor, titulo, editorial, fecha_lanzamiento))
            mysql.connection.commit()
            flash('Libro agregado exitosamente')
            return redirect(url_for('Libros'))
        except:
            flash('Id de autor no valido')
            return redirect(url_for('Libros'))

@app.route('/Delete_Libros/<int:id>')
def Delete_Libros(id):
    cur = mysql.connection.cursor()
    try:
        cur.execute('DELETE FROM libros WHERE id = {0}'.format (id))
        mysql.connection.commit()
        flash('Libro removido exitosamente')
        return redirect(url_for('Libros'))
    except:
        flash('Primero debe ser devuelto')
        return redirect(url_for('Libros'))
    
@app.route('/Libros_Edit/<id>')
def Get_Libros(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM libros WHERE id = {0}'.format (id))
    data = cur.fetchall()
    return render_template('Libros_Edit.html', libro = data[0])

@app.route('/Update_Libros/<id>', methods =['POST'])
def Update_Libros(id):
    if request.method == 'POST':
        try:
            id_autor = request.form['Idautor']
            titulo = request.form['Titulo']
            editorial = request.form['Editorial']
            fecha_lanzamiento = request.form['Fecha']
            cur = mysql.connection.cursor()
            cur.execute("""
                UPDATE libros  
                SET id_autor = %s,
                    titulo = %s,
                    editorial = %s,
                    fecha_lanzamiento = %s
                WHERE id = %s    
            """,(id_autor, titulo, editorial, fecha_lanzamiento,id))
            mysql.connection.commit()
            flash('Libro editado exitosamente')
            return redirect(url_for('Libros'))
        except:
            flash('Id de autor no valido')
            return redirect(url_for('Libros'))


#PRESTAMOS 
@app.route('/Prestamos')
def Prestamos(): 
    cur = mysql.connection.cursor()
    cur.execute("""
    SELECT prestamos.id, lector.dni, lector.nombres, lector.apellidos, libros.titulo, prestamos.fecha_prestamo 
    FROM prestamos JOIN lector ON prestamos.dni =lector.dni 
    JOIN libros  ON prestamos.id_libro = libros.id
    ORDER BY prestamos.id
    """)
    data = cur.fetchall()
    return render_template('Prestamos.html', lista_prestamos = data)

@app.route('/Prestamos_Add', methods = ['POST'])
def Prestamos_Add():
    if request.method == 'POST':
        try:
            id_libro = request.form['id_libro']
            dni = request.form['dni']
            fecha_prestamo = request.form['fecha_prestamo']
            cur = mysql.connection.cursor()
            cur.execute('INSERT INTO prestamos(id_libro, dni, fecha_prestamo)  VALUES(%s,%s,%s)', (id_libro, dni, fecha_prestamo))
            mysql.connection.commit()
            flash("Prestamo agregado exitosamente")
            return redirect(url_for('Prestamos'))
        except:
            flash("Id o DNI incorrecto")
            return redirect(url_for('Prestamos'))

@app.route('/Prestamos_Delete/<int:id>')
def Prestamos_Delete(id):
    cur = mysql.connection.cursor()
    try:
        cur.execute('DELETE FROM prestamos WHERE id = {0}'.format (id))
        mysql.connection.commit()
        flash('Prestamo finalizado')
        return redirect(url_for('Prestamo'))
    except:
        return redirect(url_for('Prestamos'))
   
@app.route('/Prestamos_Edit/<id>')
def Prestmos_Get(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM prestamos WHERE id = {0}'.format (id))
    data = cur.fetchall()
    print(data[0])
    return render_template('Prestamos_Edit.html', prestamo = data[0])

@app.route('/Prestamos_Update/<id>', methods =['POST'])
def Prestamos_Update(id):
    if request.method == 'POST':
        try:
            id_libro = request.form['id_libro']
            dni = request.form['dni']
            fecha_prestamo = request.form['fecha_prestamo']
            cur = mysql.connection.cursor()
            cur.execute("""
                UPDATE prestamos  
                SET id_libro = %s,
                    dni = %s,
                    fecha_prestamo = %s
                WHERE id = %s    
            """,(id_libro, dni, fecha_prestamo, id))
            mysql.connection.commit()
            flash("Prestamo editado exitosamente")
            return redirect(url_for('Prestamos'))
        except:
            flash("error")
            return redirect(url_for('Prestamos'))
   


    



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)

