# -*- coding: utf-8 -*-
"""Servidor local que aplica las mismas cabeceras de _headers, para probar el CSP."""
import http.server
import socketserver
import os

ROOT = r"C:\Users\usuario\dos-casas"
PORT = 8891

CSP = ("default-src 'self'; base-uri 'self'; object-src 'none'; frame-ancestors 'none'; "
       "form-action 'self'; img-src 'self' data: https://cdn.shopify.com; "
       "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
       "font-src 'self' https://fonts.gstatic.com; script-src 'self' 'unsafe-inline'; "
       "media-src 'self'; connect-src 'self'; upgrade-insecure-requests")

HEADERS = {
    "Content-Security-Policy": CSP,
    "X-Frame-Options": "DENY",
    "X-Content-Type-Options": "nosniff",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Permissions-Policy": "geolocation=(), microphone=(), camera=(), payment=(), usb=(), interest-cohort=()",
    "Cross-Origin-Opener-Policy": "same-origin",
    "X-Permitted-Cross-Domain-Policies": "none",
}

class H(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *a, **k):
        super().__init__(*a, directory=ROOT, **k)
    def end_headers(self):
        for k, v in HEADERS.items():
            self.send_header(k, v)
        super().end_headers()
    def log_message(self, *a):
        pass

socketserver.TCPServer.allow_reuse_address = True
with socketserver.TCPServer(("", PORT), H) as httpd:
    print("secure server on", PORT)
    httpd.serve_forever()
