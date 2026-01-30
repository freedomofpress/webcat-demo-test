#!/usr/bin/env python3
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import os

PORT = 1234

# CSP MUST stay byte-for-byte identical
DEFAULT_CSP = (
    "object-src 'none'; default-src 'self'; "
    "script-src 'self' 'wasm-unsafe-eval'; "
    "style-src 'self'; frame-src 'none'; worker-src 'self';"
)

ERROR_PAGE = "error.html"


class MyHTTPRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Content-Security-Policy", DEFAULT_CSP)
        super().end_headers()

    def send_error(self, code, message=None, explain=None):
        if not os.path.exists(ERROR_PAGE):
            return super().send_error(code, message, explain)

        try:
            with open(ERROR_PAGE, "rb") as f:
                body = f.read()

            self.send_response(code)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.send_header("Content-Security-Policy", DEFAULT_CSP)
            self.end_headers()

            # Respect HEAD requests
            if self.command != "HEAD":
                self.wfile.write(body)

        except Exception:
            # Fallback to default error handling if something goes wrong
            super().send_error(code, message, explain)


if __name__ == "__main__":
    httpd = ThreadingHTTPServer(("", PORT), MyHTTPRequestHandler)
    print(f"Serving current directory on http://localhost:{PORT} (multithreaded)")
    httpd.serve_forever()

