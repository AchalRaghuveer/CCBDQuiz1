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

@app.route("/search", methods=['GET', 'POST'])
def searchName():
    search_query = request.form.get('telNo')
    print('search', search_query)
    cursor = connection.cursor()
    # cursor.execute("select * from dbo.[people]")
    cursor.execute("select * from dbo.[q0c] where teln = ?", search_query)
    data = cursor.fetchone()
    print("result = ", data)
    name = data[0]
    room = data[1]
    img = data[2]
    teln = data[3]
    descript = data[4]
    # image_paths = [row[0] for row in data if row[0].strip() != '']
    # print("output", image_paths)
    if img != None:
        link="https://abr2435assign1.blob.core.windows.net/quiz0contain/"+img
    else:
        link="No image Found"
    print('link----->', link)
    return render_template('index.html', imgLink=link, room = room, name=name, descript=descript)

@app.route("/range", methods=['GET', 'POST'])
def moneyRange():
    number1 = request.form.get('number1')
    number2 = request.form.get('number2')
    cursor = connection.cursor()
    cursor.execute("select * from dbo.[q0c] where room between ? and ? ",(number1, number2))
    data = cursor.fetchall()
    linkVals = []
    # nameVals = []
    # discriptVals = []
    if data:
        print("result = ", data)
        for i in range(len(data)):
            print('img val', data[i])
            # nameVals.append(image_paths[i][0])
            # discriptVals.append(image_paths[i][4])
            if str(data[i][2]) != None:
                img = "https://abr2435assign1.blob.core.windows.net/quiz0contain/" + str(data[i][2])
            else:
                img = "No Image Found"
            print('image value -------> ', img)
            val = ValuesOBJ(data[i][0],img , data[i][4])
            linkVals.append(val)
            print('vals =====>', val)

    return render_template('index.html', linkVals=linkVals)

@app.route("/changeName", methods=['GET', 'POST'])
def changeDescript():
    name = request.form.get('name')
    discript = request.form.get('discription')
    # print('search', search_query)
    cursor = connection.cursor()
    # cursor.execute("select * from dbo.[people]")
    # cursor.execute("select * from dbo.[q0c] where teln = ?", search_query)
    cursor.execute("Update dbo.[q0c] set descript = ? where name = ?", (discript, name))
    connection.commit()
    cursor.execute("select * from dbo.[q0c] where name = ?", name)
    data = cursor.fetchone()
    print("result = ", data)
    name = data[0]
    descript = data[4]
    # image_paths = [row[0] for row in data if row[0].strip() != '']
    # print("output", image_paths)
    return render_template('index.html', name3=name, descript3=descript)

class ValuesOBJ:
            
         
    # The init method or constructor
    def __init__(self, name, link, descript):
             
        # Instance Variable
        self.name = name
        self.link = link
        self.descript = descript            

if __name__ == "__main__":
    app.run(debug = True)
