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

from .arguments import get_arguments
from .exceptions import InvalidArguments, InvalidPassword
from .login import login, logout
from .prometheus import prometheus
from .scrape import scrape_xdsl, scrape_ifconfig
from .server import serve

__version__ = "0.5.5"
