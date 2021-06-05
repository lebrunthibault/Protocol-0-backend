#!/usr/bin/env python
from http.server import HTTPServer, BaseHTTPRequestHandler


class Server(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def _html(self, message):
        """This just generates an HTML document that includes `message`
        in the body. Override, or re-write this do do more interesting stuff.
        """
        content = "<html><body><h1>%s</h1></body></html>" % message
        return content.encode("utf8")  # NOTE: must return a bytes object!

    def do_GET(self):
        self._set_headers()
        print(self.path)
        self.wfile.write(self._html("hi!"))

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        self.wfile.write(self._html("POST!"))

    @staticmethod
    def run(server_class=HTTPServer, addr="localhost", port=8000):
        server_address = (addr, port)
        httpd = server_class(server_address, Server)

        print("Starting httpd server on %s:%s" % (addr, port))
        httpd.serve_forever()


Server.run()
