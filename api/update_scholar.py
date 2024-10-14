from http.server import BaseHTTPRequestHandler
import json
from .vercel_blob import blob_store
import os
from scholarly import scholarly

class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.end_headers()

        scholar_id = os.environ.get('GOOGLE_SCHOLAR_ID')
        if scholar_id is None:
            raise Exception('GOOGLE_SCHOLAR_ID environment variable not set')
        
        author: dict = scholarly.search_author_id(scholar_id)
        scholarly.fill(author, sections=['basics', 'indices', 'counts', 'publications'])
        _ = blob_store.put('scholar_info.json', json.dumps(author, ensure_ascii=False).encode('utf-8'), {
            "addRandomSuffix": "false",
        })

        # self.wfile.write(json.dumps(resp).encode('utf-8'))
        self.wfile.write(json.dumps({'success': 1}).encode('utf-8'))
        return
    