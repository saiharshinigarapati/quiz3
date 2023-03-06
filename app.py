
#sai harshini garapati
#1002027780
#quiz3
from collections import Counter
import json
from flask import Flask, render_template, request
import time
import redis
import sqlite3
import hashlib
import pickle
import random
app = Flask(__name__)

r=redis.Redis()

redis_host="harshinig7780.redis.cache.windows.net"
redis_port=6380
redis_password="MHj89nmet8F3c2B5aPMKQ3zZhLxwI9TIyAzCaCMSZQs="

r = redis.StrictRedis(host=redis_host, port=redis_port, password=redis_password, ssl=True)

r.ping()


@app.route('/')
def home():
	return render_template("home.html")



@app.route('/q1',methods=["POST","GET"])
def q1():
    rows=[]
    if(request.method=="POST"):
        minv=request.form["minv"]
        maxv=request.form["maxv"]
        conn = sqlite3.connect('dsi.db')
        cur = conn.cursor()
        time1=time.time()
        querry="select d.id,d.net,d1.nst,d.place from dsi d,ds d1 where d.id=d1.id and d1.nst between ? and ? "
        parameters=(minv,maxv)
        cur.execute(querry,parameters)
        time2=time.time()
        row = cur.fetchall()
        conn.close()
       
        rows=[]
        for i in row:
            rows.append(i)
        
        tt=time2-time1
        return render_template('q11.html',tt=tt,rows=rows)
    else:
        return render_template('q1.html')

@app.route('/q2', methods=['POST', 'GET'])
def q2():
    if request.method == 'POST':
        no_of_queries = int(request.form['no_of_queries'])
        netv=request.form["netv"]
        times=[]
        conn = sqlite3.connect('dsi.db')
        conn1 = sqlite3.connect('ds.db')
        cur = conn.cursor()
        
        query_times = []
        results = []
        t1=time.time()
        result = "select d.id,d.net,d1.nst,d.place from dsi d,ds d1 where d.id=d1.id and  d.net= ? "
        parameters=(netv,)
        cur.execute(result,parameters)
        t2=time.time()
        row = cur.fetchall()
        for i in row:
            results.append(i)
        r=random.choices(results,k=no_of_queries)    
        times.append(t2-t1)
        return render_template('q22.html', times=times,results=r)
    else:
        return render_template('q2.html')

@app.route('/q3', methods=['POST', 'GET'])
def q3():
    if request.method == 'POST':
        n = int(request.form['no_of_times'])
        no_of_queries = int(request.form['no_of_queries'])
        netv=request.form["netv"]
        minv=request.form["minv"]
        maxv=request.form["maxv"]
        time1=time.time()
        conn = sqlite3.connect('dsi.db')
        conn1 = sqlite3.connect('ds.db')
        cur = conn.cursor()
        resultq=[]
        times=[]
        query_times = []
        results = []
        resultq1=[]
        times1=[]
        for i in range(0,n):
            t1=time.time()
            result = "select d.id,d.net,d1.nst,d.place from dsi d,ds d1 where d.id=d1.id and  d.net= ? "
            parameters=(netv,)
            cur.execute(result,parameters)
            t2=time.time()
            row = cur.fetchall()
            for i in row:
                results.append(i)
            r=random.choices(results,k=no_of_queries) 
            times.append(t2-t1)
            for i in range(len(r)):
                resultq.append(r)
        for i in range(0,n):
            t1=time.time()
            result = "select d.id,d.net,d1.nst,d.place from dsi d,ds d1 where d.id=d1.id and d1.nst between ? and ? "
            parameters=(minv,maxv)
            cur.execute(result,parameters)
            t2=time.time()
            row = cur.fetchall()
            for i in row:
                results.append(i)
            r=random.choices(results,k=no_of_queries) 
            times1.append(t2-t1)
            for i in range(len(r)):
                resultq1.append(r)
        return render_template('q33.html', times=times,results=resultq,r=resultq1,times1=times1)    
    else:
        return render_template('q3.html')        


@app.route('/q4',methods=['POST','GET'])
def withredis():
    if request.method == 'POST':
        n = int(request.form['no_of_times'])
        no_of_queries = int(request.form['no_of_queries'])
        netv=request.form["netv"]
        minv=request.form["minv"]
        maxv=request.form["maxv"]
        time1=time.time()
        result=[]
        times=[]
        times1=[]
        total=0
        conn=sqlite3.connect('dsi.db')
        cur=conn.cursor()
        querry="select d.id,d.net,d1.nst,d.place from dsi d,ds d1 where d.id=d1.id and  d.net= ? "
        parameters=(netv,)
        hash=hashlib.sha256(querry.encode('utf-8')).hexdigest()
        key="redis_cache:"+hash
        count=0
        for i in range(0,n):
            count=count+1

            t1=time.time()
            cur.execute(querry,parameters)
            rows=cur.fetchall()
            r.set(key,pickle.dumps(rows))
            r.expire(key,36)
            t2=time.time()
            total=(t2-t1)/100
            times.append(total)    
        querry1="select d.id,d.net,d1.nst,d.place from dsi d,ds d1 where d.id=d1.id and d1.nst between ? and ? "
        parameters1=(minv,maxv)
        hash=hashlib.sha256(querry.encode('utf-8')).hexdigest()
        key="redis_cache:"+hash
        for i in range(0,n):

            t1=time.time()
            cur.execute(querry1,parameters1)
            rows1=cur.fetchall()
            r.set(key,pickle.dumps(rows1))
            r.expire(key,36)
            t2=time.time()
            total1=(t2-t1)/100
           
            times1.append(total1)            
        return render_template('q44.html',times=times,times1=times1)
    else:
        return render_template('q4.html')   
@app.route('/q5',methods=["POST","GET"])
def q5():
    rows=[]
    if(request.method=="POST"):
        minv=request.form["minv"]
        maxv=request.form["maxv"]
        conn = sqlite3.connect('dsi.db')
        cur = conn.cursor()
        time1=time.time()
        querry="select d.net,d1.nst from dsi d,ds d1 where d.id=d1.id and d1.nst between ? and ? "
        parameters=(minv,maxv)
        cur.execute(querry,parameters)
        time2=time.time()
        row = cur.fetchall()
        conn.close()
       
        rows=[]
        for i in row:
            rows.append(i)
        l1=[]
        l2=[]
        for item in rows:
            l1.append(item[0])
           
        c = Counter(l1)
        l2=list(c.values())
        print(dict(c))
        tt=time2-time1
        return render_template('q55.html',tt=tt,data=dict(c))
    else:
        return render_template('q5.html')
       

if __name__=="__main__":
    app.debug=True
    app.run()