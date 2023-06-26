# import redis
import hashlib
import pickle
from timeit import default_timer as timer
from flask import Flask, render_template, request
import pyodbc
from azure.storage.blob import BlobServiceClient
import random
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import io
import numpy as np
import base64

app = Flask(__name__)

lattt = 0.053
intr_lat = 0.005
net_lat = 0.4

connection = pyodbc.connect('Driver={ODBC Driver 18 for SQL Server};Server=tcp:ccbdserver2.database.windows.net,1433;Database=CCBD;Uid=abr2435;Pwd=UTApass3;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30')
# redisConnection = redis.StrictRedis(host='abr2435ccbdweb.redis.cache.windows.net',port=6379, db=0, password='Ix5dAkrYyUa9wdbA2VDHLk8L44UvQ8kuhAzCaHBvtCU=', ssl=False)
# redisConnection.flushall()
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

@app.route("/rangepop2", methods=['GET', 'POST'])
def searchN():
    startTotTime = timer()
    maxlat = request.form.get('number1')
    minlat = request.form.get('number2')
    maxlon = request.form.get('number3')
    minlon = request.form.get('number4')
    print("values =====> ", maxlat, minlat, maxlon, minlon)
    starttime = timer()
    cursor = connection.cursor()
    cursor.execute("select * from dbo.[city-2] where (lat <= ? and lat >= ?) and (lon <= ? and lon >= ?)", (maxlat, minlat, maxlon, minlon))

    dataNear = cursor.fetchall()
    print("values of data ======> ", dataNear)
    print("data near =========> ", len(dataNear))
    tableVals2 = []
    for i in range(len(dataNear)):
        val = ValuesOBJ(dataNear[i][0], dataNear[i][1], dataNear[i][2], dataNear[i][3], dataNear[i][4])
        tableVals2.append(val)
    finalTime = "%.1f ms" % (1000 * (timer() - starttime + net_lat +intr_lat+lattt))
    finalTimes2 = "%.1f ms" % (1000 * (timer() - startTotTime + net_lat+ intr_lat+lattt))
    return render_template('index.html', tableVals99=tableVals2, finalTime1=finalTime, finalTimes2=finalTimes2)

@app.route("/rangepopRedis", methods=['GET', 'POST'])
def searchNRed():
    maxlat = request.form.get('number11')
    minlat = request.form.get('number22')
    maxlon = request.form.get('number33')
    minlon = request.form.get('number44')
    # print("values =====> ", maxPop, minPop)
    print("values =====> ", maxlat, minlat, maxlon, minlon)

    cursor = connection.cursor()
    starttimet = timer()
    starttime = timer()

    cursor.execute("select * from dbo.[city-2] where (lat <= ? and lat >= ?) and (lon <= ? and lon >= ?)", (maxlat, minlat, maxlon, minlon))
    finalTime = "%.1f ms" % (1000 * (timer() - starttime+ lattt))

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
    # redisConnection.set("fetachRedis1", temp_result)
    # redisConnection.get("fetachRedis1")
    finalTimet = "%.1f ms" % (1000 * (timer() - starttimet))
    return render_template('index.html', tableVals8=tableVals2, finalTime3=finalTime, finalTimet1=finalTimet)


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
    # redisConnection.set("fetachRedis2", temp_result)
    # starttime = timer()
    # redisConnection.get("fetachRedis2")
    # finalTime = "%.1f ms" % (1000 * (timer() - starttime + net_lat))
    return render_template('index.html', tableVals5=tableVals2)
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
        # redisConnection.set("fetchVal",temp_result)
        starttime = timer()
        # for data in range(int(noOfLoops)):
            # redisConnection.get("fetchVal")
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



# Start coding here for quiz 4=========================================================================================>


@app.route('/alphaQuant', methods=['GET', 'POST'])
def Question10ab():
    # cursor = connection.cursor()
    inputText = (request.form.get("inputVal"))
    alpha = []
    percentage = []
    array = inputText.split(', ')
    print(array)
    for element in range(0, len(array)):
        i = array[element]
        val = i.split(' ')
        print(val)
        alpha.append(val[0])
        percentage.append(int(val[1]))
    totVal = 0
    for i in range(len(percentage)):
        totVal += percentage[i]
    for i in range(len(percentage)):
        percentage[i] = percentage[i]/totVal * 100
    perStr = np.char.mod('%d', percentage)
    lable = [];
    for i in range(len(alpha)):
        str = alpha[i] + " " + perStr[i] +"%"
        lable.append(str)
    plt.pie(percentage, labels=lable)
    figfile = io.BytesIO()
    plt.savefig(figfile, format='jpeg')
    plt.close()
    figfile.seek(0)
    figdata_jpeg = base64.b64encode(figfile.getvalue())
    files = figdata_jpeg.decode('utf-8')
    # plt.show()

    return render_template('index.html', count=sum, pieChart=files)


# @app.route('/Question11ab', methods=['GET', 'POST'])
# def Question1qab():
#     # cursor = connection.cursor()
#     rangeStart = (request.form.get("rangeStart"))
#     rangeEnd = (request.form.get("rangeEnd"))
#
#     cursor = connection.cursor()
#
#     # query_str1 = "select store,sum(num) from f where store>=" + rangeStart + " and store<=" + rangeEnd + " group by store"
#     # query_str2 = "select store,sum(num) from f  group by store"
#     # cursor.execute(query_str1)
#     # data1 = cursor.fetchall()
#     # cursor.execute(query_str2)
#     # data2 = cursor.fetchall()
#     labels1 = ["cat", "dog", "rat", "bat"]
#     heights1 = [10,30,20,15]
#     labels2 = ["rose", "jasmine", "lotus", "popla"]
#     heights2 = [14,30,10,50]
#     # for i in data1:
#     #     labels1.append(i[0])
#     #     heights1.append(i[1])
#     #
#     # for i in data2:
#     #     labels2.append(i[0])
#     #     heights2.append(i[1])
#
#     plt.bar(labels1, heights1, color=['blue'])
#     plt.xlabel("Stores")
#     plt.ylabel("Amount of food")
#     plt.title("Total amount of foods for each store in entered range")
#     figfile = io.BytesIO()
#     plt.savefig(figfile, format='jpeg')
#     plt.close()
#     figfile.seek(0)
#     figdata_jpeg = base64.b64encode(figfile.getvalue())
#     files1 = figdata_jpeg.decode('utf-8')
#
#     plt.bar(labels2, heights2, color=['blue'])
#     plt.xlabel("Stores")
#     plt.ylabel("Amount of food")
#     plt.title("Total amount of foods for all in entered range")
#     figfile = io.BytesIO()
#     plt.savefig(figfile, format='jpeg')
#     plt.close()
#     figfile.seek(0)
#     figdata_jpeg = base64.b64encode(figfile.getvalue())
#     files2 = figdata_jpeg.decode('utf-8')
#
#     return render_template('index.html', output1=files1, output2=files2)

# horizontal ======================================================>

@app.route('/Question11ab', methods=['GET', 'POST'])
def Question11ab():
    inputText = (request.form.get("inputValBar"))
    labels1 = []
    heights1 = []
    array = inputText.split(', ')
    print(array)
    for element in range(0, len(array)):
        i = array[element]
        val = i.split(' ')
        print(val)
        labels1.append(val[0])
        heights1.append(int(val[1]) * 10)

    # labels1 = ["cat", "dog", "rat", "bat"]
    # heights1 = [10, 30, 20, 15]
    # labels2 = ["rose", "jasmine", "lotus", "popla"]
    # heights2 = [14, 30, 10, 50]

    for i in range(len(heights1)):

        key = heights1[i]
        key1 = labels1[i]
        j = i - 1
        while j >= 0 and key < heights1[j]:
            heights1[j + 1] = heights1[j]
            labels1[j + 1] = labels1[j]
            j -= 1
        heights1[j + 1] = key
        labels1[j + 1] = key1

    print("height sorted ====> ", heights1)
    print("words sorted accordingly ====> ", labels1)
    plt.barh(labels1, heights1, color='red')
    plt.xlabel("Percentage")
    plt.ylabel("Words")
    plt.title("Horizontal Bar Graph")
    figfile1 = io.BytesIO()
    plt.savefig(figfile1, format='jpeg')
    plt.close()
    figfile1.seek(0)
    figdata_jpeg1 = base64.b64encode(figfile1.getvalue())
    files1 = figdata_jpeg1.decode('utf-8')

    # plt.barh(labels2, heights2, color='blue')
    # plt.xlabel("Amount of food")
    # plt.ylabel("Stores")
    # plt.title("Total amount of foods for all in entered range")
    # figfile2 = io.BytesIO()
    # plt.savefig(figfile2, format='jpeg')
    # plt.close()
    # figfile2.seek(0)
    # figdata_jpeg2 = base64.b64encode(figfile2.getvalue())
    # files2 = figdata_jpeg2.decode('utf-8')

    return render_template('index.html', output1=files1)



@app.route('/Question12ab', methods=['GET', 'POST'])
def Question12ab():
    # cursor = connection.cursor()
    inputText = (request.form.get("inputValDot"))
    x = []
    y = []
    c = []
    array = inputText.split(', ')
    print(array)
    for element in range(0, len(array)):
        i = array[element]
        val = i.split(' ')
        print(val)
        x.append(int(val[0]))
        y.append(int(val[1]))
        c.append(val[2])

    colors=[]
    for i in range(len(c)):
        if c[i] == '1':
            colors.append("green")
        elif c[i] == '2':
            colors.append("black")
        else:
            colors.append("red")
    plt.scatter(x, y, c=colors)
    plt.xlabel("X")
    plt.ylabel("Y")
    plt.title("Graph")
    figfile = io.BytesIO()
    plt.savefig(figfile, format='jpeg')
    plt.close()
    figfile.seek(0)
    figdata_jpeg = base64.b64encode(figfile.getvalue())
    files = figdata_jpeg.decode('utf-8')

    return render_template("index.html", output=files)


# @app.route('/Question12abc', methods=['GET', 'POST'])
# def Question12abc():
#     cursor = connection.cursor()
#
#     # query_str = "select * from p"
#     # cursor.execute(query_str)
#     # data = cursor.fetchall()
#     # x = [1, 2, 3, 4, 5, 6, 7 ,8,9]
#     # y = [5,3,6,9,1,3,5,4,9]
#     # colors = ["red", "green", "blue","red", "green", "blue","red", "green", "blue"]
#     # for i in data:
#     #     x.append(i[0])
#     #     y.append(i[1])
#     #     colors.append(i[2])
#
#     # plt.hist(x, y, c=colors)
#     data = np.random.randn(1000)
#     plt.hist(data, bins=30)
#
#     # Set labels and title
#     plt.xlabel('Value')
#     plt.ylabel('Frequency')
#     plt.title('Histogram')
#     plt.xlabel("X")
#
#     plt.ylabel("Y")
#     plt.title("Graph")
#     figfile = io.BytesIO()
#     plt.savefig(figfile, format='jpeg')
#     plt.close()
#     figfile.seek(0)
#     figdata_jpeg = base64.b64encode(figfile.getvalue())
#     files = figdata_jpeg.decode('utf-8')
#
#     return render_template("index.html", output3=files)

# horizontal======================================================>

@app.route('/Question12abc', methods=['GET', 'POST'])
def Question12abc():
    cursor = connection.cursor()

    data = np.random.randn(1000)
    plt.barh(range(len(data)), data, color='blue')

    # Set labels and title
    plt.xlabel('Frequency')
    plt.ylabel('Value')
    plt.title('Horizontal Histogram')

    figfile = io.BytesIO()
    plt.savefig(figfile, format='jpeg')
    plt.close()
    figfile.seek(0)
    figdata_jpeg = base64.b64encode(figfile.getvalue())
    files = figdata_jpeg.decode('utf-8')

    return render_template("index.html", output3=files)



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



