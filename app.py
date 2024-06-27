from flask import Flask, render_template, request
from flask_mysqldb import MySQL
import MySQLdb.cursors

app = Flask(__name__)

# Configuração do MySQL
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'meu_banco_de_dados'

mysql = MySQL(app)

@app.route('/')
def index():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT DISTINCT coluna1 FROM dados")
    options1 = cursor.fetchall()
    cursor.execute("SELECT DISTINCT coluna2 FROM dados")
    options2 = cursor.fetchall()
    cursor.execute("SELECT DISTINCT coluna3 FROM dados")
    options3 = cursor.fetchall()
    return render_template('index.html', options1=options1, options2=options2, options3=options3)

@app.route('/templates/resultados.html', methods=['POST'])
def resultados():
    filtro1 = request.form.get('filtro1')
    filtro2 = request.form.get('filtro2')
    filtro3 = request.form.get('filtro3')

    print(f"Filtro 1: {filtro1}, Filtro 2: {filtro2}, Filtro 3: {filtro3}")  # Depuração dos filtros

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    query = "SELECT * FROM dados WHERE coluna1 = %s AND coluna2 = %s AND coluna3 = %s"
    cursor.execute(query, (filtro1, filtro2, filtro3))
    dados_filtrados = cursor.fetchall()

    print(f"Dados Filtrados: {dados_filtrados}")  # Depuração dos dados filtrados

    return render_template('resultados.html', dados=dados_filtrados)

if __name__ == '__main__':
    app.run(debug=True)