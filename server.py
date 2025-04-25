import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from crud import get_entry, delete_entry, add_entry, update_entry, ResourceNotFoundError


class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        parsed_path = urlparse(self.path)
        path_parts = parsed_path.path.strip('/').split('/')
        if len(path_parts) != 2:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Invalid URL format")
            return
        _, id = path_parts
        try:
            entry = get_entry('user', id)
            self.send_response(200)
            self.send_header("Content-type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps(entry).encode())
        except ResourceNotFoundError as e:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(str(e).encode())  # Message clair
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Server error: {str(e)}".encode())

    def do_POST(self):
        parsed_path = urlparse(self.path)
        path_parts = parsed_path.path.strip('/').split('/')
        if len(path_parts) != 1:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Invalid URL format")
            return
        resource = path_parts[0]  # Not used but still part of the URL structure
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        fields = json.loads(post_data)
        try:
            add_entry(resource, fields)
            self.send_response(201)  # Created
            self.end_headers()
            self.wfile.write(f"Added {resource}".encode())
        except Exception as e:
            self.send_response(400)  # Bad request
            self.end_headers()
            self.wfile.write(f"Failed to add entry: {str(e)}".encode())

    def do_PUT(self):
        parsed_path = urlparse(self.path)
        path_parts = parsed_path.path.strip('/').split('/')
        if len(path_parts) != 2:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Invalid URL format")
            return
        _, id = path_parts  # We don't need 'resource' anymore
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        fields = json.loads(post_data)
        try:
            updated_entry = update_entry('user', id, fields)  # 'user' is a placeholder
            self.send_response(200)
            self.end_headers()
            self.wfile.write(f"Updated user {id}".encode())
        except ResourceNotFoundError:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(f"User with ID {id} not found".encode())
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Server error: {str(e)}".encode())

    def do_DELETE(self):
        parsed_path = urlparse(self.path)
        path_parts = parsed_path.path.strip('/').split('/')
        if len(path_parts) != 2:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Invalid URL format")
            return
        _, id = path_parts  # We don't need 'resource' anymore
        try:
            message = delete_entry('user', id)  # 'user' is a placeholder
            self.send_response(200)
            self.end_headers()
            self.wfile.write(message.encode())
        except ResourceNotFoundError:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(f"User with ID {id} not found".encode())
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Server error: {str(e)}".encode())


def run(server_class=HTTPServer, handler_class=RequestHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Starting HTTP server on port {port}...")
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped gracefully.")
        httpd.server_close()


if __name__ == '__main__':
    run()
