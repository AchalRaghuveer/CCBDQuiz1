import redis
import hashlib
import pickle
from timeit import default_timer as timer
from flask import Flask, render_template, request
import pyodbc
from azure.storage.blob import BlobServiceClient

app = Flask(__name__)

lat = 0.053
intr_lat = 0.005
net_lat = 0.4

connection = pyodbc.connect('Driver={ODBC Driver 18 for SQL Server};Server=tcp:ccbdserver2.database.windows.net,1433;Database=CCBD;Uid=abr2435;Pwd=UTApass3;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30')
redisConnection = redis.StrictRedis(host='abr2435ccbdweb.redis.cache.windows.net',port=6379, db=0, password='Ix5dAkrYyUa9wdbA2VDHLk8L44UvQ8kuhAzCaHBvtCU=', ssl=False)
redisConnection.flushall()
cursor = connection.cursor()

@app.route("/")
def index():
    cursor = connection.cursor()
    cursor.execute("select * from dbo.[city-1]")
    data = cursor.fetchall()
    print("length = ", len(data))
    return render_template('index.html')


# @app.route("/search", methods=['GET', 'POST'])
# def searchRow():
#     search_query = request.form.get('city')
#     print('search', search_query)
#     cursor = connection.cursor()
#     cursor.execute("select * from dbo.[city] where city = ?", search_query)
#     data = cursor.fetchall()
#     if len(data) > 0:
#         cityVal = ValuesOBJ(data[0][0],data[0][1], data[0][2], data[0][3], data[0][4])
#         lat = data[0][3]
#         long = data[0][4]
#     else:
#         cityVal = ValuesOBJ("No City","No State","0","9999999","9999999")
#         lat = 9999999999
#         long = 9999999999
#     km = 100
#     print("city val =======> ", cityVal.state)
#     cursor1 = connection.cursor()
#     cursor1.execute("SELECT * FROM dbo.[city] WHERE (6371 * ACOS( COS(RADIANS(?)) * COS(RADIANS(lat)) * COS(RADIANS(lon) - RADIANS(?)) + SIN(RADIANS(?)) * SIN(RADIANS(lat)) )) <= ?", (lat,long,lat,km))
#     dataNear = cursor1.fetchall()
#     print("data near =========> ", len(dataNear))
#     tableVals = []
#     for i in range(len(dataNear)):
#         if dataNear[i][0] != data[0][0]:
#             val = ValuesOBJ(dataNear[i][0],dataNear[i][1], dataNear[i][2], dataNear[i][3], dataNear[i][4])
#             tableVals.append(val)
#     return render_template('index.html', tableVals=tableVals, cityVal=cityVal)

@app.route("/rangepop", methods=['GET', 'POST'])
def searchN():
    startTotTime = timer()
    maxPop = request.form.get('number5')
    minPop = request.form.get('number6')
    print("values =====> ", maxPop, minPop)
    starttime = timer()
    cursor = connection.cursor()
    cursor.execute("select * from dbo.[city-1] where population <= ? and population >= ?", (minPop, maxPop))

    dataNear = cursor.fetchall()
    print("values of data ======> ", dataNear)
    print("data near =========> ", len(dataNear))
    tableVals2 = []
    for i in range(len(dataNear)):
        val = ValuesOBJ(dataNear[i][0], dataNear[i][1], dataNear[i][2], dataNear[i][3], dataNear[i][4])
        tableVals2.append(val)
    finalTime = "%.1f ms" % (1000 * (timer() - starttime + net_lat))
    finalTimes2 = "%.1f ms" % (1000 * (timer() - startTotTime + net_lat))
    return render_template('index.html', tableVals2=tableVals2, finalTime1=finalTime, finalTimes2=finalTimes2)

@app.route("/rangepopRedis", methods=['GET', 'POST'])
def searchNRed():
    maxPop = request.form.get('number15')
    minPop = request.form.get('number16')
    print("values =====> ", maxPop, minPop)
    cursor = connection.cursor()
    cursor.execute("select * from dbo.[city-1] where population <= ? and population >= ?", (minPop, maxPop))

    dataNear = cursor.fetchall()
    print("values of data ======> ", dataNear)
    print("data near =========> ", len(dataNear))
    tableVals2 = []
    for i in range(len(dataNear)):
        val = ValuesOBJ(dataNear[i][0], dataNear[i][1], dataNear[i][2], dataNear[i][3], dataNear[i][4])
        tableVals2.append(val)
    temp_result = []
    for j in tableVals2:
        temp_result = temp_result + str(j)
    redisConnection.set("fetachRedis1", temp_result)
    starttime = timer()
    redisConnection.get("fetachRedis1")
    finalTime = "%.1f ms" % (1000 * (timer() - starttime + net_lat))
    return render_template('index.html', tableVals8=tableVals2, finalTime7=finalTime)


@app.route("/rangepoptup", methods=['GET', 'POST'])
def searchNtup():
    startTotTime = timer()
    maxPop = request.form.get('number7')
    minPop = request.form.get('number8')
    tup = request.form.get('tup')
    print("values =====> ", maxPop, minPop, tup)
    starttime = timer()
    cursor = connection.cursor()
    # cursor.execute("select Top ? rand() * from dbo.[city-1] where population <= ? and population >= ?", (tup, minPop, maxPop))
    cursor.execute("SELECT * FROM dbo.[city-1] where population <= ? and population >= ? ORDER BY NEWID()", (minPop, maxPop))
    dataNear = cursor.fetchall()
    print("values of data ======> ", dataNear)
    print("data near =========> ", len(dataNear))
    tableVals2 = []
    for i in range(int(tup)):
        val = ValuesOBJ(dataNear[i][0], dataNear[i][1], dataNear[i][2], dataNear[i][3], dataNear[i][4])
        tableVals2.append(val)
    finalTime = "%.1f ms" % (1000 * (timer() - starttime + net_lat))
    finalTimes2 = "%.1f ms" % (1000 * (timer() - startTotTime + net_lat))
    return render_template('index.html', tableVals3=tableVals2, finalTime2=finalTime, finalTimes3= finalTimes2)

@app.route("/rangepoptupRedis", methods=['GET', 'POST'])
def searchNtupRed():
    maxPop = request.form.get('number11')
    minPop = request.form.get('number12')
    tup = request.form.get('tupRed')
    print("values =====> ", maxPop, minPop, tup)
    cursor = connection.cursor()
    # cursor.execute("select Top ? rand() * from dbo.[city-1] where population <= ? and population >= ?", (tup, minPop, maxPop))
    cursor.execute("SELECT * FROM dbo.[city-1] where population <= ? and population >= ? ORDER BY NEWID()",(minPop, maxPop))
    dataNear = cursor.fetchall()
    print("values of data ======> ", dataNear)
    print("data near =========> ", len(dataNear))
    tableVals2 = []
    for i in range(int(tup)):
        val = ValuesOBJ(dataNear[i][0], dataNear[i][1], dataNear[i][2], dataNear[i][3], dataNear[i][4])
        tableVals2.append(val)
    temp_result = ""
    for j in tableVals2:
        temp_result = temp_result + str(j)
    redisConnection.set("fetachRedis2", temp_result)
    starttime = timer()
    redisConnection.get("fetachRedis2")
    finalTime = "%.1f ms" % (1000 * (timer() - starttime + net_lat))
    return render_template('index.html', tableVals5=tableVals2, finalTime4=finalTime)
@app.route("/incrange", methods=['GET', 'POST'])
def incrange():
    state = request.form.get('state')
    maxPopu = request.form.get('number9')
    minPopu = request.form.get('number10')
    inc = request.form.get('inc')
    print("max and min vals ========> ", state, maxPopu, minPopu, inc)
    starttime = timer()
    cursor = connection.cursor()
    cursor.execute("update dbo.[city-1] set population = ? + population where state = ? and (population <= ? and population >= ?)", (inc,state, maxPopu, minPopu))
    connection.commit()
    cursor1 = connection.cursor()
    maxPopu1=int(maxPopu)+int(inc)
    minPopu2=int(minPopu)+int(inc)
    print(minPopu2, maxPopu1)
    cursor1.execute("select * from dbo.[city-1] where state = ? and (population <= ? and population >= ?)", (state, maxPopu1, minPopu2))
    dataNear = cursor1.fetchall()
    print("values of data ======> ", dataNear)
    print("data near =========> ", len(dataNear))
    tableVals2 = []
    for i in range(len(dataNear)):
        val = ValuesOBJ(dataNear[i][0], dataNear[i][1], dataNear[i][2], dataNear[i][3], dataNear[i][4])
        tableVals2.append(val)
    finalTime = "%.1f ms" % (1000 * (timer() - starttime + net_lat))
    return render_template('index.html', tableVals4=tableVals2, finalTime3=finalTime)

@app.route("/incstate", methods=['GET', 'POST'])
def incstate():
    state = request.form.get('state')
    maxPopu = request.form.get('number5')
    minPopu = request.form.get('number6')
    inc = request.form.get('inc')
    cursor = connection.cursor()
    cursor.execute("update dbo.[city] set population = ? + population where state = ? and (population <= ? and population >= ?)", (inc, state, maxPopu, minPopu))
    connection.commit()
    cursor1 = connection.cursor()
    cursor1.execute("select * from dbo.[city] where state = ? and (population <= ? and population >= ?)", (state, maxPopu, minPopu))
    dataNear = cursor1.fetchall()
    print("values of data ======> ", dataNear)
    print("data near =========> ", len(dataNear))
    tableVals2 = []
    for i in range(len(dataNear)):
        val = ValuesOBJ(dataNear[i][0], dataNear[i][1], dataNear[i][2], dataNear[i][3], dataNear[i][4])
        tableVals2.append(val)
    return render_template('index.html', tableVals4=tableVals2)


@app.route("/delete", methods=['GET', 'POST'])
def deleteCity():

    name = request.form.get('nameDel')
    cursor.execute("Delete from dbo.[city] where city = ?", name)
    cursor.commit()
    return render_template('index.html', msgDel="Success")

@app.route("/deleteS", methods=['GET', 'POST'])
def deleteState():

    name = request.form.get('nameDelS')
    cursor.execute("Delete from dbo.[city] where state = ?", name)
    cursor.commit()
    return render_template('index.html', msgDelS="Success")

@app.route("/add", methods=['GET', 'POST'])
def add():

    city = request.form.get('cityAdd')
    state = request.form.get('stateAdd')
    pop = request.form.get('popAdd')
    lat = request.form.get('latAdd')
    lon = request.form.get('lonAdd')
    cursor.execute("insert into dbo.[city] values (?,?,?,?,?)", (city, state, pop, lat, lon))
    cursor.commit()
    return render_template('index.html', msgAddS="Success")




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

@app.route('/searchNormal', methods=['GET', 'POST'])
def randomquery():
    if request.method == 'POST':
        NoOfLoops = request.form.get('normal')
        starttime = timer()
        for data in range(int(NoOfLoops)):
            cursor.execute("select top 1000 * from dbo.[all_month]")
            # cursor.execute("INSERT INTO dbo.[all_month] VALUES('2022-06-20T00:14:13.990Z','00:14:13', 65.56016739, -196.0518964, 42.64500046, 3.54, 'ml', 55, 894, 0.03837, 0.899999995, 'hv', '2022-06-20T00:27:46.240Z', '27 km SSE of Fern Forest', 'Hawaii', 'earthquake', 0.89, 0.479999989,3.22,26, 'automatic', 'hv', 'hv')")
            cursor.commit()
        finalTime = "%.1f ms" % (1000 * (timer() - starttime + net_lat))
    return render_template('index.html', randomquerytime = finalTime )


@app.route('/search', methods = ['GET', 'POST'])
def redisValue():
    if request.method == 'POST':
        noOfLoops = request.form.get('name')
        print("redis Q =====> ", noOfLoops)
        q = "select top 1000 * from dbo.[all_month]"
        cursor.execute(q)
        temp = cursor.fetchall()
        temp_result = ""
        for j in temp:
            temp_result = temp_result + str(j)
        redisConnection.set("fetchVal",temp_result)
        starttime = timer()
        for data in range(int(noOfLoops)):
            redisConnection.get("fetchVal")
        # finalTime = "%.1f ms" % (1000 * (timer() - starttime - lat - intr_lat - net_lat))
        # hashing = hashlib.sha224(q.encode('utf-8')).hexdigest()
        # key = "valRedis:{}".format(hashing)
        # starttime = timer()
        # for data in range(int(noOfLoops)):
        #     if not (redisConnection.get(key)):
        #         cursor.execute(q)
        #         outputVal = list(cursor.fetchall())
        #         print("fetched val =====> ", outputVal)
        #         redisConnection.set(key, pickle.dumps(list(outputVal)))
        #         redisConnection.expire(key, 40)
        #     else:
        #         print("caching redis")
        # finalTime = "%.1f ms" % (1000 * (timer() - starttime - lat - intr_lat - net_lat))
        finalTime = "%.1f ms" % (1000 * (timer() - starttime + net_lat))
    return render_template('index.html', randomquerytimeredis = finalTime)

# @app.route("/updateNote", methods=['GET', 'POST'])
# def updateNotes():
#
#     row = request.form.get('noteUp')
#     name = request.form.get('nameDel')
#
#     print("Name =======> ",name)
#
#     cursor.execute("Update dbo.[q1c] set notes=? where name = ?", (row,name))
#     cursor.commit()
#     return render_template('index.html', msgDel="Success")
# @app.route("/updateImg", methods=['GET', 'POST'])
# def updateImg():
#
#     img = request.files['imgUp']
#     name = request.form.get('nameDel')
#
#     print("Name =======> ",name)
#     upload(img)
#     cursor.execute("Update dbo.[q1c] set pic=? where name = ?", (img.filename,name))
#     cursor.commit()
#     return render_template('index.html', msgDel="Success")
#
#
# def upload(file):
#     account_url = "DefaultEndpointsProtocol=https;AccountName=abr2435assign1;AccountKey=vD9scxZxq94P15DKDccDeGj1I10NJJux8Y8Qh6tTdM9ubazSBLqs7QyxVYvIR/ehAhUgmNKgSS3I+AStWiOwEg==;EndpointSuffix=core.windows.net"
#     blob_service_client = BlobServiceClient.from_connection_string(account_url)
#     container_client = blob_service_client.get_container_client("quiz1container")
#     print("File", file)
#     blob_client = container_client.upload_blob(name=file.filename, data=file.stream, overwrite=True)
#     return "success"


class ValuesOBJ:

    # The init method or constructor
    def __init__(self, name, link, descript, seat, long):
        # Instance Variable
        self.city = name
        self.state = link
        self.population = descript
        self.lat = seat
        self.long = long
if __name__ == "__main__":
    app.run(debug = True)
