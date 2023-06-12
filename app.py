from flask import Flask, render_template, request
import pyodbc

app = Flask(__name__)

connection = pyodbc.connect('Driver={ODBC Driver 18 for SQL Server};Server=tcp:ccbdserver2.database.windows.net,1433;Database=CCBD;Uid=abr2435;Pwd=UTApass3;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30')

cursor = connection.cursor()

@app.route("/")
def index():
    cursor = connection.cursor()
    cursor.execute("select * from dbo.[q0c]")
    data = cursor.fetchall()
    print("length = ", len(data))
    return render_template('index.html')


if __name__ == "__main__":
    app.run(debug = True)
