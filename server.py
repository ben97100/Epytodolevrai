import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from crud import get_entry, delete_entry, add_entry, update_entry, ResourceNotFoundError

def run(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler):
    server_address = ('', 8080)
    httpd = server_class(server_address, handler_class)
    httpd.serve_forever()

if __name__ == '__main__':
    run()
