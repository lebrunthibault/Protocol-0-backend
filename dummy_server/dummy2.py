import SimpleHTTPServer
import SocketServer

PORT = 8000

class Server(SimpleHTTPServer.SimpleHTTPRequestHandler):
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


httpd = SocketServer.TCPServer(("", PORT), Server)

print "serving at port", PORT
httpd.serve_forever()