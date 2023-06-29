import os
import re
import string
import urllib
import urllib.request
import requests

from flask import Flask, render_template, request
import pyodbc
from azure.storage.blob import BlobServiceClient
import random
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import io
import numpy as np
import base64
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
from nltk.probability import FreqDist
from nltk.tag import pos_tag
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
# test="George is very clever but he doesn’t study his lessons"
# tokens = word_tokenize(test)
import nltk
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from collections import Counter

nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')


# Example usage
story = "Es war einmal ein Mann namens Peter. ääääääääääääääEr lebte in einem kleinen Dorf. Eines Tages traf er eine wunderschöne Frau. Sie war die Prinzessin des Königreichs. Peter verliebte sich sofort in sie. Sie hatten viele Abenteuer zusammen."




from werkzeug.utils import secure_filename

app = Flask(__name__)

connection = pyodbc.connect('Driver={ODBC Driver 18 for SQL Server};Server=tcp:ccbdserver2.database.windows.net,1433;Database=CCBD;Uid=abr2435;Pwd=UTApass3;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30')

cursor = connection.cursor()

# Placeholder for document index
document_index = {}

# Placeholder for stop words
stop_words = set([
    'the', 'and', 'or', 'is', 'are', 'in', 'of', 'to', 'a', 'an', 'on', 'that',
    'this', 'it', 'for', 'with', 'as', 'be', 'can', 'if', 'but', 'not'
])

# @app.route("/")
# def index():
#     with open("demoDoc.txt", 'r', encoding="utf-8") as file:
#         text = file.read()
#     print("Story ======================> "+text)
#     # lowercase
#     textValue = "Dbs Mäachen ging aurch aie Hintertür nbch aem Gbrten una rief ihr zbhmen Täubchen, ihr Turteltäubchen, bll ihr Vaglein unter aem Himmel, kommt una helft mir lesen, aie guten ins Tapfchen, aie schlechten ins Krapfchen."
#     lowerText = textValue.lower()
#     print("text in lower case ==============> ", lowerText)
#     # remove punctuations
#     translator = str.maketrans('', '', string.punctuation)
#     text_without_punctuation = lowerText.translate(translator)
#     print("Punction removed ==============> ", text_without_punctuation)
#     # remove stop_words
#     stop_words = set(stopwords.words('german'))
#
#     words = text_without_punctuation.split()
#     filtered_words = [word for word in words if word.lower() not in stop_words]
#     filtered_text = ' '.join(filtered_words)
#     print("filtered text ==============> ", filtered_text)
#     # remove stem words like cats -> cat
#     stemmer = PorterStemmer()
#
#     tokens = word_tokenize(filtered_text)
#     stemmed_tokens = [stemmer.stem(word) for word in tokens]
#     stemmed_text = ' '.join(stemmed_tokens)
#
#     print("stemmed text ==============> ", stemmed_text)
#
#     n = 5
#     top_nouns = find_top_n_nouns(story, n)
#
#     for noun, count in top_nouns:
#         print("values of noun and count =======================================>", f"{noun}: {count}")
#
#     character_occurances()
#     characterReplace()
#     get_lines_with_word(3,"muÃŸte")
#     return render_template('index.html')


# @app.route("/", methods=['GET', 'POST'])
# def index():
#     if request.method == 'POST':
#         N = 3
#         word = "muÃŸte"
#
#         # Read the story from the file
#         with open("demoDoc.txt", 'r', encoding="utf-8") as file:
#             story = file.read()
#
#         # Convert to lowercase
#         lower_text = story.lower()
#
#         # Remove punctuations
#         translator = str.maketrans('', '', string.punctuation)
#         text_without_punctuation = lower_text.translate(translator)
#
#         # Remove stop words
#         stop_words = set(stopwords.words('german'))
#         words = text_without_punctuation.split()
#         filtered_words = [word for word in words if word.lower() not in stop_words]
#         filtered_text = ' '.join(filtered_words)
#
#         # Stem words
#         stemmer = PorterStemmer()
#         tokens = word_tokenize(filtered_text)
#         stemmed_tokens = [stemmer.stem(word) for word in tokens]
#         stemmed_text = ' '.join(stemmed_tokens)
#
#         # Find top N nouns
#         top_nouns = find_top_n_nouns(stemmed_text, N)
#
#         # Character occurrences
#         char_stats = character_occurances()
#
#         # Character replacement
#         modified_document, lines_with_word = characterReplace()
#
#         # Get lines with word
#         lines_containing_word = get_lines_with_word(N, word)
#
#         return render_template('index.html', top_nouns=top_nouns, char_stats=char_stats,
#                                modified_document=modified_document, lines_with_word=lines_with_word,
#                                lines_containing_word=lines_containing_word, N=N, word=word)
#
#     return render_template('index.html')
#
# def find_top_n_nouns(story, n):
#     # Tokenize the story into sentences
#     sentences = sent_tokenize(story)
#
#     # Initialize a list to store all the nouns
#     nouns = []
#
#     # Iterate over the sentences
#     for sentence in sentences:
#         # Tokenize each sentence into words
#         words = word_tokenize(sentence)
#
#         # Perform part-of-speech tagging on the words
#         tagged_words = nltk.pos_tag(words)
#
#         # Extract the nouns from the tagged words
#         nouns.extend([word for word, pos in tagged_words if pos.startswith('N')])
#
#     # Remove stopwords
#     stop_words = set(stopwords.words('german'))
#     nouns = [noun for noun in nouns if noun.lower() not in stop_words]
#
#     # Count the frequencies of the nouns
#     noun_freqs = Counter(nouns)
#
#     # Get the top N most frequent nouns
#     top_nouns = noun_freqs.most_common(n)
#
#     return top_nouns
#
#
# def character_occurances():
#     # Example document
#     # document = """
#     # Es war einmal ein Mann namens Peter. Er lebte in einem kleinen Dorf. Eines Tages traf er eine wunderschöne Frau. Sie war die Prinzessin des Königreichs. Peter verliebte sich sofort in sie. Sie hatten viele Abenteuer zusammen.
#     # """
#     document = story
#     characters = ["a", "i", "ä"]
#
#     # Count the occurrences of each character in the document
#     char_count = Counter(document.lower())
#
#     # Calculate the total number of characters in the document
#     total_chars = sum(char_count.values())
#
#     # Calculate the count and percentage for each character
#     char_stats = []
#     for char in characters:
#         count = char_count[char]
#         percentage = (count / total_chars) * 100
#         char_stats.append({"char": char, "count": count, "percentage": percentage})
#
#     # Print the character statistics
#     for stat in char_stats:
#         print(f"Character: {stat['char']}, Count: {stat['count']}, Percentage: {stat['percentage']}%")
#
#
# def characterReplace():
#     # Example document
#     document = story
#     char_to_replace = "ä"
#     replacement = "ss"
#
#     # Replace the character in the document
#     modified_document = document.replace(char_to_replace, replacement)
#
#     # Get the first 8 lines or sentences of the modified document
#     lines = modified_document.strip().split("\n")[:8]
#
#     # Print the modified document
#     print(modified_document)
#     print_first_8_lines_from_file()
#
#
# def print_first_8_lines_from_file():
#     with open("demoDoc.txt", 'r') as file:
#         lines = file.readlines()[:8]
#         for line in lines:
#             print(line.rstrip())
#
#
# def get_lines_with_word(N, word):
#     lines = []
#     with open('demoDoc.txt', 'r') as file:
#         for line in file:
#             if word in line:
#                 lines.append(line.rstrip())
#                 if len(lines) == N:
#                     break
#     print(lines)
#


# =========================================================================================================================
@app.route("/", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        N = 3
        word = "muÃŸte"

        # Read the story from the file
        # with open('https://abr2435assign1.blob.core.windows.net/quiz1container/demoTXTFILE.txt', 'r', encoding="utf-8") as file:
        #     story = file.read()
        story = ""
        response = requests.get('https://abr2435assign1.blob.core.windows.net/quiz1container/demoTXTFILE.txt')

        if response.status_code == 200:
            content = response.text
            # Process the file content here
            story = content
            print(content)

        # Convert to lowercase
        lower_text = story.lower()

        # Remove punctuations
        translator = str.maketrans('', '', string.punctuation)
        text_without_punctuation = lower_text.translate(translator)

        # Remove stop words
        stop_words = set(stopwords.words('german'))
        words = text_without_punctuation.split()
        filtered_words = [word for word in words if word.lower() not in stop_words]
        filtered_text = ' '.join(filtered_words)

        # Stem words
        stemmer = PorterStemmer()
        tokens = word_tokenize(filtered_text)
        stemmed_tokens = [stemmer.stem(word) for word in tokens]
        stemmed_text = ' '.join(stemmed_tokens)

        # Find top N nouns
        top_nouns = find_top_n_nouns(stemmed_text, N)

        # Character occurrences
        char_stats = character_occurrences(story)

        # Character replacement
        modified_document, lines_with_word = character_replace(story, 'ä', 'ss')

        # Get lines with word
        lines_containing_word = get_lines_with_word(story, N, word)

        return render_template('index.html', top_nouns=top_nouns, char_stats=char_stats,
                               modified_document=modified_document, lines_with_word=lines_with_word,
                               lines_containing_word=lines_containing_word, N=N, word=word)

    return render_template('index.html')

def find_top_n_nouns(story, n):
    sentences = sent_tokenize(story)
    nouns = []
    for sentence in sentences:
        words = word_tokenize(sentence)
        tagged_words = nltk.pos_tag(words)
        nouns.extend([word for word, pos in tagged_words if pos.startswith('N')])
    stop_words = set(stopwords.words('german'))
    nouns = [noun for noun in nouns if noun.lower() not in stop_words]
    noun_freqs = Counter(nouns)
    top_nouns = noun_freqs.most_common(n)
    return top_nouns

def character_occurrences(story):
    characters = ["a", "i", "ä"]
    char_count = Counter(story.lower())
    total_chars = sum(char_count.values())
    char_stats = []
    for char in characters:
        count = char_count[char]
        percentage = (count / total_chars) * 100
        char_stats.append({"char": char, "count": count, "percentage": percentage})
    return char_stats

def character_replace(story, char_to_replace, replacement):
    modified_document = story.replace(char_to_replace, replacement)
    lines_with_word = modified_document.strip().split("\n")[:8]
    return modified_document, lines_with_word

def get_lines_with_word(story, N, word):
    lines = []
    # with open('https://abr2435assign1.blob.core.windows.net/quiz1container/demoTXTFILE.txt', 'r') as file:
    # story = urllib.request.urlopen('https://abr2435assign1.blob.core.windows.net/quiz1container/demoTXTFILE.txt')
    story = ""
    response = requests.get('https://abr2435assign1.blob.core.windows.net/quiz1container/demoTXTFILE.txt')

    if response.status_code == 200:
        content = response.text
        # Process the file content here
        story = content
        print(content)
    for line in story:
        # for line in file:
        if word in line:
            lines.append(line.rstrip())
            if len(lines) == N:
                break
    return lines

@app.route("/search", methods=['GET', 'POST'])
def searchRow():
    search_query = request.form.get('city')
    print('search', search_query)
    cursor = connection.cursor()
    cursor.execute("select * from dbo.[city] where city = ?", search_query)
    data = cursor.fetchall()
    if len(data) > 0:
        cityVal = ValuesOBJ(data[0][0],data[0][1], data[0][2], data[0][3], data[0][4])
        lat = data[0][3]
        long = data[0][4]
    else:
        cityVal = ValuesOBJ("No City","No State","0","9999999","9999999")
        lat = 9999999999
        long = 9999999999
    km = 100
    print("city val =======> ", cityVal.state)
    cursor1 = connection.cursor()
    cursor1.execute("SELECT * FROM dbo.[city] WHERE (6371 * ACOS( COS(RADIANS(?)) * COS(RADIANS(lat)) * COS(RADIANS(lon) - RADIANS(?)) + SIN(RADIANS(?)) * SIN(RADIANS(lat)) )) <= ?", (lat,long,lat,km))
    dataNear = cursor1.fetchall()
    print("data near =========> ", len(dataNear))
    tableVals = []
    for i in range(len(dataNear)):
        if dataNear[i][0] != data[0][0]:
            val = ValuesOBJ(dataNear[i][0],dataNear[i][1], dataNear[i][2], dataNear[i][3], dataNear[i][4])
            tableVals.append(val)
    return render_template('index.html', tableVals=tableVals, cityVal=cityVal)

@app.route("/range", methods=['GET', 'POST'])
def searchN():
    maxLat = request.form.get('number1')
    minLat = request.form.get('number2')
    maxLon = request.form.get('number3')
    minLon = request.form.get('number4')
    print("max and min vals ========> ", maxLat, minLat, maxLon, minLon)
    cursor = connection.cursor()
    cursor.execute("select * from dbo.[city] where (lat <= ? and lat >= ?) and (lon <= ? and lon >= ?)", (maxLat, minLat, maxLon, minLon))

    dataNear = cursor.fetchall()
    print("values of data ======> ", dataNear)
    print("data near =========> ", len(dataNear))
    tableVals2 = []
    for i in range(len(dataNear)):
        val = ValuesOBJ(dataNear[i][0], dataNear[i][1], dataNear[i][2], dataNear[i][3], dataNear[i][4])
        tableVals2.append(val)
    return render_template('index.html', tableVals2=tableVals2)

@app.route("/incrange", methods=['GET', 'POST'])
def incrange():
    maxLat = request.form.get('number1')
    minLat = request.form.get('number2')
    maxLon = request.form.get('number3')
    minLon = request.form.get('number4')
    maxPopu = request.form.get('number5')
    minPopu = request.form.get('number6')
    inc = request.form.get('inc')
    print("max and min vals ========> ", maxLat, minLat, maxLon, minLon)
    cursor = connection.cursor()
    cursor.execute("update dbo.[city] set population = ? + population where (lat <= ? and lat >= ?) and (lon <= ? and lon >= ?) and (population <= ? and population >= ?)", (inc,maxLat, minLat, maxLon, minLon, maxPopu, minPopu))
    connection.commit()
    cursor1 = connection.cursor()
    cursor1.execute("select * from dbo.[city] where (lat <= ? and lat >= ?) and (lon <= ? and lon >= ?) and (population <= ? and population >= ?)", (maxLat, minLat, maxLon, minLon, maxPopu, minPopu))
    dataNear = cursor1.fetchall()
    print("values of data ======> ", dataNear)
    print("data near =========> ", len(dataNear))
    tableVals2 = []
    for i in range(len(dataNear)):
        val = ValuesOBJ(dataNear[i][0], dataNear[i][1], dataNear[i][2], dataNear[i][3], dataNear[i][4])
        tableVals2.append(val)
    return render_template('index.html', tableVals3=tableVals2)

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

@app.route("/upload", methods=['GET', 'POST'])
def up():
    # img = request.form.get('img')
    img = request.files['txtFile']
    name = request.form.get('name')
    # cursor = connection.cursor()
    # msg = upload(img)
    # cursor.execute("update dbo.[people] set Picture=? where Name=?", (img.filename, name))

    return render_template('index.html')


@app.route('/upload123', methods=['POST'])
def search123():
    file = request.files['txtFile']
    query = request.form.get('name')

    if file:
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        index_document(file_path, file.read().decode('utf-8'))

        results = perform_search(file_path, query)
        print("results ========> ", results)
        print("query ========> ", query)

        return render_template('index.html', query=query, resultsVal123=results)
    else:
        return "No file uploaded."

def index_document(file_path, content):
    processed_content = preprocess_text(content)
    words = processed_content.split()

    if file_path not in document_index:
        document_index[file_path] = []

    document_index[file_path].append(words)


def perform_search(file_path, query):
    processed_query = preprocess_text(query)
    query_words = processed_query.split()

    results = []
    if file_path in document_index:
        documents = document_index[file_path]
        for idx, document in enumerate(documents):
            if all(word in document for word in query_words):
                # Store the line number and content of the matching line
                match = {
                    'line_number': idx + 1,  # Add 1 to account for 0-based indexing
                    'content': ' '.join(document)
                }
                results.append(match)

    return results


def preprocess_text(text):
    # Convert to lowercase
    processed_text = text.lower()

    # Remove non-alphanumeric characters
    processed_text = re.sub(r'[^a-z0-9\s]', '', processed_text)

    # Remove extra whitespaces
    processed_text = re.sub(r'\s+', ' ', processed_text)

    # Remove stop words
    processed_text = ' '.join(word for word in processed_text.split() if word not in stop_words)

    # Perform word stemming (you can use a library like nltk.stem for better stemmers)
    processed_text = processed_text  # Placeholder for stemming logic

    return processed_text


# def index_document(file_path, content):
#     processed_content = preprocess_text(content)
#     words = processed_content.split()
#
#     if file_path not in document_index:
#         document_index[file_path] = []
#
#     document_index[file_path].append(words)
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


@app.route('/Question10ab', methods=['GET', 'POST'])
def Question10ab():
    # cursor = connection.cursor()
    inputText = (request.form.get("inputText")).replace(" ", "")
    inputText = inputText.lower()
    all_freq = {}
    all_freq["Alphabet"] = 0
    all_freq["Number"] = 0
    all_freq["Punctuation"] = 0
    print(inputText)
    for element in range(0, len(inputText)):
        i = inputText[element]
        if i.isalpha():
            all_freq["Alphabet"] += 1
        elif i.isdigit():
            all_freq["Number"] += 1
        elif i == "." or i == "," or i == "?" or i == "!" or i == "$" or i == "*":
            all_freq["Punctuation"] += 1
    # print(string_name[element])
    # for i in inputText:

    print("freq is ", all_freq)
    sum = 0
    labels = []
    percentageList = []
    freqCountList = []
    labels = list(all_freq.keys())
    for i in labels:
        sum = sum + all_freq[i]

        freqCountList.append((i, all_freq[i]))
    labellist = []
    for i in range(len(freqCountList)):
        a = (freqCountList[i][1] / sum) * 100
        a = round(a, 2)
        percentageList.append(a)
        labellist.append(labels[i] + " " + str(a) + "%")

    colors = ['#ff6666', '#ffcc99', '#99ff99']
    print("labels", labels)
    print("percentage", percentageList)
    plt.pie(percentageList, labels=labellist, colors=colors)
    figfile = io.BytesIO()
    plt.savefig(figfile, format='jpeg')
    plt.close()
    figfile.seek(0)
    figdata_jpeg = base64.b64encode(figfile.getvalue())
    files = figdata_jpeg.decode('utf-8')
    # plt.show()

    return render_template('index.html', data=freqCountList, count=sum, pieChart=files)


@app.route('/Question11ab', methods=['GET', 'POST'])
def Question1qab():
    # cursor = connection.cursor()
    rangeStart = (request.form.get("rangeStart"))
    rangeEnd = (request.form.get("rangeEnd"))

    cursor = connection.cursor()

    # query_str1 = "select store,sum(num) from f where store>=" + rangeStart + " and store<=" + rangeEnd + " group by store"
    # query_str2 = "select store,sum(num) from f  group by store"
    # cursor.execute(query_str1)
    # data1 = cursor.fetchall()
    # cursor.execute(query_str2)
    # data2 = cursor.fetchall()
    labels1 = ["cat", "dog", "rat", "bat"]
    heights1 = [10,30,20,15]
    labels2 = ["rose", "jasmine", "lotus", "popla"]
    heights2 = [14,30,10,50]
    # for i in data1:
    #     labels1.append(i[0])
    #     heights1.append(i[1])
    #
    # for i in data2:
    #     labels2.append(i[0])
    #     heights2.append(i[1])

    plt.bar(labels1, heights1, color=['blue'])
    plt.xlabel("Stores")
    plt.ylabel("Amount of food")
    plt.title("Total amount of foods for each store in entered range")
    figfile = io.BytesIO()
    plt.savefig(figfile, format='jpeg')
    plt.close()
    figfile.seek(0)
    figdata_jpeg = base64.b64encode(figfile.getvalue())
    files1 = figdata_jpeg.decode('utf-8')

    plt.bar(labels2, heights2, color=['blue'])
    plt.xlabel("Stores")
    plt.ylabel("Amount of food")
    plt.title("Total amount of foods for all in entered range")
    figfile = io.BytesIO()
    plt.savefig(figfile, format='jpeg')
    plt.close()
    figfile.seek(0)
    figdata_jpeg = base64.b64encode(figfile.getvalue())
    files2 = figdata_jpeg.decode('utf-8')

    return render_template('index.html', output1=files1, output2=files2)


@app.route('/Question12ab', methods=['GET', 'POST'])
def Question12ab():
    cursor = connection.cursor()

    # query_str = "select * from p"
    # cursor.execute(query_str)
    # data = cursor.fetchall()
    x = [1, 2, 3, 4, 5, 6, 7 ,8,9]
    y = [5,3,6,9,1,3,5,4,9]
    colors = ["red", "green", "blue","red", "green", "blue","red", "green", "blue"]
    # for i in data:
    #     x.append(i[0])
    #     y.append(i[1])
    #     colors.append(i[2])

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


@app.route('/Question12abc', methods=['GET', 'POST'])
def Question12abc():
    cursor = connection.cursor()

    # query_str = "select * from p"
    # cursor.execute(query_str)
    # data = cursor.fetchall()
    # x = [1, 2, 3, 4, 5, 6, 7 ,8,9]
    # y = [5,3,6,9,1,3,5,4,9]
    # colors = ["red", "green", "blue","red", "green", "blue","red", "green", "blue"]
    # for i in data:
    #     x.append(i[0])
    #     y.append(i[1])
    #     colors.append(i[2])

    # plt.hist(x, y, c=colors)
    data = np.random.randn(1000)
    plt.hist(data, bins=30)

    # Set labels and title
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title('Histogram')
    plt.xlabel("X")

    plt.ylabel("Y")
    plt.title("Graph")
    figfile = io.BytesIO()
    plt.savefig(figfile, format='jpeg')
    plt.close()
    figfile.seek(0)
    figdata_jpeg = base64.b64encode(figfile.getvalue())
    files = figdata_jpeg.decode('utf-8')

    return render_template("index.html", output3=files)
# quiz 5 ================================================>

@app.route('/allAssignment', methods=['GET', 'POST'])
def allAssign():
    # nval = int(request.form.get('task1'))
    with open("static/demoDoc.txt", 'r', encoding="utf-8") as file:
        text = file.read()
    print("Story ======================> "+text)
    # lowercase
    textValue = "Dbs Mäachen ging aurch aie Hintertür nbch aem Gbrten una rief ihr zbhmen Täubchen, ihr Turteltäubchen, bll ihr Vaglein unter aem Himmel, kommt una helft mir lesen, aie guten ins Tapfchen, aie schlechten ins Krapfchen."
    lowerText = textValue.lower()
    print("text in lower case ==============> ", lowerText)
    # remove punctuations
    translator = str.maketrans('', '', string.punctuation)
    text_without_punctuation = lowerText.translate(translator)
    print("Punction removed ==============> ", text_without_punctuation)
    # remove stop_words
    stop_words = set(stopwords.words('german'))

    words = text_without_punctuation.split()
    filtered_words = [word for word in words if word.lower() not in stop_words]
    filtered_text = ' '.join(filtered_words)
    print("filtered text ==============> ", filtered_text)
    # remove stem words like cats -> cat
    stemmer = PorterStemmer()

    tokens = word_tokenize(filtered_text)
    stemmed_tokens = [stemmer.stem(word) for word in tokens]
    stemmed_text = ' '.join(stemmed_tokens)

    print("stemmed text ==============> ", stemmed_text)
    return render_template('task1.html')




def upload(file):
    account_url = "DefaultEndpointsProtocol=https;AccountName=abr2435assign1;AccountKey=vD9scxZxq94P15DKDccDeGj1I10NJJux8Y8Qh6tTdM9ubazSBLqs7QyxVYvIR/ehAhUgmNKgSS3I+AStWiOwEg==;EndpointSuffix=core.windows.net"
    blob_service_client = BlobServiceClient.from_connection_string(account_url)
    container_client = blob_service_client.get_container_client("quiz1container")
    print("File", file)
    blob_client = container_client.upload_blob(name=file.filename, data=file.stream, overwrite=True)
    return "success"
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
