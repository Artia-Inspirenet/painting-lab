from http.server import HTTPServer, BaseHTTPRequestHandler
from http import HTTPStatus
import os, shutil

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        # self.wfile.write(bytes("<html><body><h1>hi!</h1></body></html>", "utf-8"))

        try:
            f = open(os.path.join(os.getcwd(),"index.html"), 'rb')
        except OSError:
            self.send_error(HTTPStatus.NOT_FOUND, "File not found")
            return None

        shutil.copyfileobj(f, self.wfile)

        f.close()

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        # Doesn't do anything with posted data
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        self._set_headers()
        self.wfile.write(bytes("<html><body><h1>POST!</h1>%s</pre></body></html>" % post_data, "utf-8"))

def run(server_class=HTTPServer, handler_class=S, port=8888):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print("Starting Web Server @%s" % port.__str__())
    print("You can access through web brouser URL:http://localhost:port\n" +
          "Default port number is 8888 but this can be customized by adding port number like below.\n" +
          "\t$ python server-run.py 8000")
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    if len(argv) == 2:
        run(port=int(argv[1]))

    else:
        run()
