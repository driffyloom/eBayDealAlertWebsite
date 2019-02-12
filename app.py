from flask import Flask, render_template, request
import pymongo
from eBayAPISearch import eBaySearch
import os


#templates are for html
#static folder is for js files
app = Flask(__name__, static_folder="./", template_folder="./")

port = int(os.environ.get('PORT', 5000))
#for connecting to localhost
#client = pymongo.MongoClient("mongodb://%s:%s@localhost:27017/"% ("AustinAdmin", "test"))

client = pymongo.MongoClient("mongodb://%s:%s@ds057862.mlab.com:57862/dealalertdb"%("AustinAdmin", "testPassword1"))

#localhost version
#mydb = client["eBaySearchData"]
#test
mydb = client["dealalertdb"] 

@app.route("/")
@app.route("/home")
def index():
    return render_template("index.html")

@app.route('/setPreferences', methods = ["PUT","GET"])
def setPreferences():
    search = request.args.get('searchBar','')
    priceLimit = request.args.get('priceLimit','')
    eBayAPIPoller = eBaySearch("AustinCh-DealAler-PRD-63939d325-5fa4cbe2")
    bestMatches = eBayAPIPoller.findBestMatch(eBayAPIPoller.search(search,priceLimit),search,priceLimit)
    return  render_template("setPreferences.html",bestMatches = bestMatches)

@app.route('/notifyComplete', methods = ["GET", "POST"])
def addPreferencesToDB():
    if(request.method == "POST"):
        username = request.form['username']
        email = request.form['email']
        prefArray = [int(i) for i in request.form.getlist("chosen")]
        eBayAPIPoller = eBaySearch("AustinCh-DealAler-PRD-63939d325-5fa4cbe2")
        eBayAPIPoller.addPrefItemsToDB(username,email,prefArray)
        mydb["tempPreferences"].drop()
        return  render_template("dealAlertCompletion.html")

@app.route('/searchResults' , methods = ["GET"])
def searchResults():
    if(request.method == "GET"):
        search = request.args.get('searchBar','')
        priceLimit = request.args.get('priceLimit','')
        print(search)
        print(priceLimit)
        eBayAPIPoller = eBaySearch("AustinCh-DealAler-PRD-63939d325-5fa4cbe2")
        eBayAPIPoller.addResultsToDB(eBayAPIPoller.search(search,priceLimit))
        collectionName = search + priceLimit
        mycol = mydb[collectionName]
        data = mycol.find().limit(20)
    return  render_template("searchResults.html",data = data)

@app.route("/hello")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run()