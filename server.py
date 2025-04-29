from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
import json
from crud import get_entry, add_entry, update_entry, delete_entry

PORT = 8081

class SimpleCRUDHandler(BaseHTTPRequestHandler):
    def _set_headers(self, code=200, content_type='application/json'):
        self.send_response(code)
        self.send_header('Content-type', content_type)
        self.end_headers()

    def _parse_post_data(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length).decode('utf-8')
        return parse_qs(body)

    def do_GET(self):
        path_parts = self.path.strip("/").split("/")
        if len(path_parts) != 2:
            self._set_headers(400)
            self.wfile.write(json.dumps({"error": "Invalid GET path"}).encode())
            return
        resource, id = path_parts
        try:
            result = get_entry(resource, id)
            self._set_headers(200)
            self.wfile.write(json.dumps(result).encode())
        except Exception as e:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": str(e)}).encode())

    def do_POST(self):
        path_parts = self.path.strip("/").split("/")
        if len(path_parts) != 1:
            self._set_headers(400)
            self.wfile.write(json.dumps({"error": "Invalid POST path"}).encode())
            return
        resource = path_parts[0]
        try:
            data = self._parse_post_data()
            fields = [v[0] for v in data.values()]
            add_entry(resource, fields)
            self._set_headers(201)
            self.wfile.write(json.dumps({"message": f"{resource} added successfully"}).encode())
        except Exception as e:
            self._set_headers(400)
            self.wfile.write(json.dumps({"error": str(e)}).encode())

    def do_PUT(self):
        path_parts = self.path.strip("/").split("/")
        if len(path_parts) != 2:
            self._set_headers(400)
            self.wfile.write(json.dumps({"error": "Invalid PUT path"}).encode())
            return
        resource, id = path_parts
        try:
            data = self._parse_post_data()
            fields = [v[0] for v in data.values()]
            update_entry(resource, id, fields)
            self._set_headers(200)
            self.wfile.write(json.dumps({"message": f"{resource} {id} updated successfully"}).encode())
        except Exception as e:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": str(e)}).encode())

    def do_DELETE(self):
        path_parts = self.path.strip("/").split("/")
        if len(path_parts) != 2:
            self._set_headers(400)
            self.wfile.write(json.dumps({"error": "Invalid DELETE path"}).encode())
            return
        resource, id = path_parts
        try:
            delete_entry(resource, id)
            self._set_headers(200)
            self.wfile.write(json.dumps({"message": f"{resource} {id} deleted successfully"}).encode())
        except Exception as e:
            self._set_headers(404)
            self.wfile.write(json.dumps({"error": str(e)}).encode())


def run(server_class=HTTPServer, handler_class=SimpleCRUDHandler):
    server_address = ('', PORT)
    httpd = server_class(server_address, handler_class)
    print(f"Server running on port {PORT}")
    httpd.serve_forever()


if __name__ == "__main__":
    run()
