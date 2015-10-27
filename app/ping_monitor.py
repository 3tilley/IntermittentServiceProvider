import os
import sys
import sqlite3

from flask import Flask, render_template, jsonify

fields = [  
    ("timestamp", "datetime"),
    ("host",      "number"),
    ("iswifi",    "boolean"),
    ("count",     "number"),
    ("lost",      "number"),
    ("min",       "number"),  
    ("max",       "number"),
    ("mean",      "number"),
    ("median",    "number"),
    ("stdev",      "number")
]

fieldsAndIndices = [ (i, v[0], v[1]) for i, v in enumerate(fields)]

def makeCells(dbResults, columns):
    
    filteredCols = [ (i, n, t) for i, n, t in fieldsAndIndices if n in columns ]
    inds = [ i for (i, n, t) in filteredCols]
    
    
    cols = [{ "id": n, "type": t} for i, n, t in filteredCols]
    
    rows = [{ "c" : [{"v": row[i]} for i in inds]} for row in dbResults]

    return {"cols": cols, "rows": rows}
    
    
    
app = Flask(__name__)

@app.route('/')
def index():
    print "Loading index"
    return render_template("index.html")
    
@app.route('/pings')
def pings():
    con = None
    try:
        print "Connecting to db"
        con = sqlite3.connect(os.path.join("..","data.db"))
        print "Connected"
        cur = con.cursor()
        
        cur.execute("select * from ping")
        
        data = cur.fetchall()
        print "Fetched data"
        return jsonify(makeCells(data, ["timestamp", "min", "max", "mean"]))
    except sqlite3.Error, e:
        
        print "Error %s:" % e.args[0]
        
    finally:
        
        if con:
            con.close()
        
    
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
    #pings()