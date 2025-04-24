import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from crud import get_entry, delete_entry, add_entry, update_entry


class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_path = urlparse(self.path)
        path_parts = parsed_path.path.strip('/').split('/')
        if len(path_parts) != 2:
            self.send_error(404, "Invalid URL format")
            return
        resource, entry_id = path_parts
        try:
            data = get_entry(resource, entry_id)
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(data).encode())
        except Exception as e:
            self.send_error(404, f"{resource} {entry_id} not found")

    def do_POST(self):
        parsed_path = urlparse(self.path)
        path_parts = parsed_path.path.strip('/').split('/')
        if len(path_parts) != 1:
            self.send_error(404, "Invalid URL format")
            return
        resource = path_parts[0]
        content_length = int(self.headers.get('Content-Length', 0))
        post_data = self.rfile.read(content_length)
        try:
            fields = json.loads(post_data)
            if not fields.get("title") or not fields.get("content"):
                raise ValueError("Missing required fields")
            add_entry(resource, fields)
            self.send_response(201)
            self.end_headers()
            self.wfile.write(f"Added {resource}".encode())
        except Exception as e:
            self.send_error(400, f"Failed to add entry: {str(e)}")

    def do_PUT(self):
        parsed_path = urlparse(self.path)
        path_parts = parsed_path.path.strip('/').split('/')
        if len(path_parts) != 2:
            self.send_error(404, "Invalid URL format")
            return
        resource, entry_id = path_parts
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        try:
            fields = json.loads(post_data)
            update_entry(resource, entry_id, fields)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(f"Updated {resource} {entry_id}".encode())
        except Exception as e:
            self.send_error(404, f"{resource} {entry_id} not found")

    def do_DELETE(self):
        parsed_path = urlparse(self.path)
        path_parts = parsed_path.path.strip('/').split('/')
        if len(path_parts) != 2:
            self.send_error(404, "Invalid URL format")
            return
        resource, entry_id = path_parts
        try:
            delete_entry(resource, entry_id)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(f"Deleted {resource} {entry_id}".encode())
        except Exception as e:
            self.send_error(404, f"{resource} {entry_id} not found")


def run(server_class=HTTPServer, handler_class=RequestHandler):
    server_address = ('', 8080)
    httpd = server_class(server_address, handler_class)
    print("Starting HTTP server on port 8081...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped gracefully.")
        httpd.server_close()


if __name__ == '__main__':
    run()
