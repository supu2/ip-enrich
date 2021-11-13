from flask import Flask, jsonify, Response, request, redirect
import maxminddb
from datetime import datetime
import json
import time
app = Flask(__name__)

ireader =  maxminddb.open_database('mmdb/GeoIP2-ISP.mmdb')
greader =  maxminddb.open_database('mmdb/GeoIP2-City.mmdb')
starttime = time.time()
usage = "usage: get /enrich?ip=8.8.8.8  post /enrich?keys=ip_src_addr&keys=ip_dst_addr&type=isp&type=geo"
@app.route("/")
def route():
    return redirect("/enrich", code=302)
@app.route("/status", methods = ['GET'])
def status():
    resp = {}
    now = time.time()
    resp["uptime"] = int(now - starttime)
    if resp["uptime"] > 86400:
        return Response(json.dumps(resp), status=500, mimetype="application/json")
    else:
        return Response(json.dumps(resp), status=200, mimetype="application/json") 


@app.route("/enrich", methods = ['GET', 'POST'])
def main():
    if request.method == 'GET':
        try:
            ip = request.args['ip']
        except:
            return Response(usage,status=403)
        return str(greader.get(ip))
    if request.method == 'POST':
        readertype = request.args.getlist('type')
        if not readertype:
            return Response(usage,status=403)        
        keys = request.args.getlist('keys')
        if not keys:
            return Response(usage,status=403)
        resp = []
        lines = request.data.splitlines()
        for line in lines:
            ll = line.decode("utf-8")
            curr = json.loads(ll)
            if isinstance(curr, dict):
                resp.append(enrich(curr, keys, readertype))
            else:
                for row in curr:
                    resp.append(enrich(row, keys, readertype))
        return Response(json.dumps(resp), status=200, mimetype="application/json")

def enrich(row, _keys, readertype):
    if not row.get('enrich'):
        row['enrich'] = {}
    
    for k in _keys:
        if not k in row['enrich'].keys():
            row['enrich'][k] = {}
        try:
            for  _type in readertype:
                if _type == "isp":
                    row['enrich'][k]['isp'] = ireader.get(row[k])
                else:
                    geo = greader.get(row[k])
                    row['enrich'][k]['geo'] = str(geo.get('location').get('latitude')) +","+str(geo.get('location').get('longitude'))
        except:
            pass
    return cleanNullTerms(dict(row))

def cleanNullTerms(d):
    clean = {}
    for k, v in d.items():
        if isinstance(v, dict):
            nested = cleanNullTerms(v)
            if len(nested.keys()) > 0:
                clean[k] = nested
        elif v is not None:
            clean[k] = v
    return clean
