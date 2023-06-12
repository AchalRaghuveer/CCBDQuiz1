from flask import Flask, render_template, request
import pyodbc
from azure.storage.blob import BlobServiceClient

app = Flask(__name__)

connection = pyodbc.connect('Driver={ODBC Driver 18 for SQL Server};Server=tcp:ccbdserver2.database.windows.net,1433;Database=CCBD;Uid=abr2435;Pwd=UTApass3;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30')

cursor = connection.cursor()

@app.route("/")
def index():
    cursor = connection.cursor()
    cursor.execute("select * from dbo.[q1c]")
    data = cursor.fetchall()
    print("length = ", len(data))
    return render_template('index.html')


@app.route("/search", methods=['GET', 'POST'])
def searchRow():
    search_query = request.form.get('row')
    print('search', search_query)
    cursor = connection.cursor()
    # cursor.execute("select * from dbo.[people]")
    cursor.execute("select * from dbo.[q1c] where row = ?", search_query)
    data = cursor.fetchall()
    tableVals = []
    for i in range(len(data)):
        if str(data[i][2]) != None:
            img = "https://abr2435assign1.blob.core.windows.net/quiz1container/" + str(data[i][3])
        else:
            img = "No Image Found"
        print('image value -------> ', img)
        val = ValuesOBJ(data[i][0], img, data[i][2], "")
        tableVals.append(val)
    return render_template('index.html', tableVals=tableVals)

@app.route("/findNumber", methods=['GET', 'POST'])
def searchN():
    number1 = request.form.get('number1')
    number2 = request.form.get('number2')
    seat = request.form.get('seat')
    print("Numbers =======> ", number1, number2, seat)
    cursor = connection.cursor()
    data = None
    if number1 != '' and number2 != '' and seat != '':
        print("executed 1st condition")
        cursor.execute("select * from dbo.[q1c] where row between ? and ? and seat = ?",(number1, number2, seat))
        data = cursor.fetchall()
    elif number1 != '' and number2 != '' and seat == '':
        print("executed 2nd condition")
        cursor.execute("select * from dbo.[q1c] where row between ? and ?", (number1, number2))
        data = cursor.fetchall()
    else:
        print("executed else condition")
        cursor.execute("select * from dbo.[q1c] where seat = ?", (seat,))
        data = cursor.fetchall()
    print("length = ", len(data))
    print("Data Imp =====> ", data)
    tableVals = []
    for i in range(len(data)):
        if str(data[i][2]) != None:
            img = "https://abr2435assign1.blob.core.windows.net/quiz1container/" + str(data[i][3])
        else:
            img = "No Image Found"
        print('image value -------> ', img)
        val = ValuesOBJ(data[i][0], img, data[i][2], data[i][4])
        tableVals.append(val)
    return render_template('index.html', tableVals2=tableVals)

@app.route("/add", methods=['GET', 'POST'])
def addUser():
    row = request.form.get('rowAdd')
    img = request.files['imgAdd']
    name = request.form.get('nameAdd')
    seat = request.form.get('seatAdd')
    notes = request.form.get('notesAdd')

    print("Numbers =======> ", row, img, name, seat, notes)
    if img != None:
        upload(img)
    cursor = connection.cursor()

    cursor.execute("INSERT INTO dbo.[q1c] VALUES (?,?,?,?,?)", (name, row, seat, img.filename, notes))
    cursor.commit()
    return render_template('index.html', msg="Success")

@app.route("/delete", methods=['GET', 'POST'])
def deleteUser():

    name = request.form.get('nameDel')


    print("Name =======> ",name)

    cursor.execute("Delete from dbo.[q1c] where name = ?", name)
    cursor.commit()
    return render_template('index.html', msgDel="Success")

@app.route("/updateRow", methods=['GET', 'POST'])
def updateRow():

    row = request.form.get('rowUp')
    name = request.form.get('nameDel')

    print("Name =======> ",name)

    cursor.execute("Update dbo.[q1c] set row=? where name = ?", (row,name))
    cursor.commit()
    return render_template('index.html', msgDel="Success")

@app.route("/updateSeat", methods=['GET', 'POST'])
def updateSeat():

    seat = request.form.get('seatUp')
    name = request.form.get('nameDel')

    print("Name =======> ",name)

    cursor.execute("Update dbo.[q1c] set seat=? where name = ?", (seat,name))
    cursor.commit()
    return render_template('index.html', msgDel="Success")

@app.route("/updateNote", methods=['GET', 'POST'])
def updateNotes():

    row = request.form.get('noteUp')
    name = request.form.get('nameDel')

    print("Name =======> ",name)

    cursor.execute("Update dbo.[q1c] set notes=? where name = ?", (row,name))
    cursor.commit()
    return render_template('index.html', msgDel="Success")
@app.route("/updateImg", methods=['GET', 'POST'])
def updateImg():

    img = request.files['imgUp']
    name = request.form.get('nameDel')

    print("Name =======> ",name)
    upload(img)
    cursor.execute("Update dbo.[q1c] set pic=? where name = ?", (img.filename,name))
    cursor.commit()
    return render_template('index.html', msgDel="Success")


def upload(file):
    account_url = "DefaultEndpointsProtocol=https;AccountName=abr2435assign1;AccountKey=vD9scxZxq94P15DKDccDeGj1I10NJJux8Y8Qh6tTdM9ubazSBLqs7QyxVYvIR/ehAhUgmNKgSS3I+AStWiOwEg==;EndpointSuffix=core.windows.net"
    blob_service_client = BlobServiceClient.from_connection_string(account_url)
    container_client = blob_service_client.get_container_client("quiz1container")
    print("File", file)
    blob_client = container_client.upload_blob(name=file.filename, data=file.stream, overwrite=True)
    return "success"
class ValuesOBJ:

    # The init method or constructor
    def __init__(self, name, link, descript, seat):
        # Instance Variable
        self.name = name
        self.link = link
        self.descript = descript
        self.seat = seat
if __name__ == "__main__":
    app.run(debug = True)
