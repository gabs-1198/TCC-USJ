from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('meu_banco_de_dados.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    options1 = conn.execute("SELECT DISTINCT coluna1 FROM dados").fetchall()
    options2 = conn.execute("SELECT DISTINCT coluna2 FROM dados").fetchall()
    options3 = conn.execute("SELECT DISTINCT coluna3 FROM dados").fetchall()
    conn.close()
    return render_template('index.html', options1=options1, options2=options2, options3=options3)

@app.route('/resultados', methods=['POST'])
def resultados():
    filtro1 = request.form.get('filtro1')
    filtro2 = request.form.get('filtro2')
    filtro3 = request.form.get('filtro3')

    conn = get_db_connection()
    query = "SELECT * FROM dados WHERE coluna1 = ? AND coluna2 = ? AND coluna3 = ?"
    dados_filtrados = conn.execute(query, (filtro1, filtro2, filtro3)).fetchall()
    conn.close()

    return render_template('resultados.html', dados=dados_filtrados)

if __name__ == '__main__':
    app.run(debug=True)
