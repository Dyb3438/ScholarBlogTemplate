from http.server import BaseHTTPRequestHandler
import os
import json
import requests
from .vercel_blob import blob_store

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.end_headers()

        blobs = blob_store.list({'prefix': 'scholar_info.json'})

        if len(blobs['blobs']) == 0:
            self.wfile.write(json.dumps({'result': 0}).encode('utf-8'))
        else:
            content_url = blobs['blobs'][0]['url']
            content = requests.get(content_url).json()
            self.wfile.write(json.dumps({'result': 1, 'data': content}).encode('utf-8'))
        return
    

