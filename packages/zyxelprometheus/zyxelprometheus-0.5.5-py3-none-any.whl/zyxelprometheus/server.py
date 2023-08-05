# zyxelprometheus
# Copyright (C) 2020 Andrew Wilkinson
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from datetime import datetime
import http.server

from .login import login, logout
from .prometheus import prometheus
from .scrape import scrape_ifconfig, scrape_xdsl


class Scraper:
    def __init__(self, args):
        self.args = args
        self.session = None

    def scrape(self):
        if self.session is None:
            self.session = login(self.args.host,
                                 self.args.user,
                                 self.args.passwd)

        xdsl = scrape_xdsl(self.session) \
            if not self.args.ifconfig_only else None
        ifconfig = scrape_ifconfig(self.session) \
            if not self.args.xdsl_only else None

        return xdsl, ifconfig


class Handler(http.server.BaseHTTPRequestHandler):
    scraper = None

    def do_GET(self):
        if self.path == "/":
            self.send_index()
        elif self.path == "/metrics":
            self.send_metrics()
        else:
            self.send_error(404)

    def send_index(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write("""
<html>
<head><title>Zyxel Prometheus</title></head>
<body>
<h1>Zyxel Prometheus</h1>
<p><a href="/metrics">Metrics</a></p>
</body>
</html>""".encode("utf8"))

    def send_metrics(self):
        xdsl, ifconfig = self.scraper.scrape()

        self.send_response(200)
        self.end_headers()
        self.wfile.write(prometheus(xdsl, ifconfig).encode("utf8"))


def serve(args):  # pragma: no cover
    Handler.scraper = Scraper(args)
    server = http.server.HTTPServer(args.bind, Handler)
    server.serve_forever()
