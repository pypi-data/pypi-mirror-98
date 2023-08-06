# ##############################################################################
#  Author: echel0n <echel0n@sickrage.ca>
#  URL: https://sickrage.ca/
#  Git: https://git.sickrage.ca/SiCKRAGE/sickrage.git
#  -
#  This file is part of SiCKRAGE.
#  -
#  SiCKRAGE is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#  -
#  SiCKRAGE is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  -
#  You should have received a copy of the GNU General Public License
#  along with SiCKRAGE.  If not, see <http://www.gnu.org/licenses/>.
# ##############################################################################


import datetime
import os
import posixpath
import re

import sickrage
from sickrage.core.helpers import bs4_parser
from sickrage.core.websession import WebSession


class imdbPopular(object):
    def __init__(self):
        """Gets a list of most popular TV series from imdb"""

        # Use akas.imdb.com, just like the imdb lib.
        self.url = 'http://www.imdb.com/search/title'

        self.params = {
            'at': 0,
            'sort': 'moviemeter',
            'title_type': 'tv_series',
            'year': '%s,%s' % (datetime.date.today().year - 1, datetime.date.today().year + 1)
        }

    def fetch_popular_shows(self):
        """Get popular show information from IMDB"""

        popular_shows = []

        data = WebSession().get(self.url, headers={'Referer': 'http://www.imdb.com/'}, params=self.params)
        if not data or not data.text:
            sickrage.app.log.debug("No data returned from IMDb")
            return

        with bs4_parser(data.text) as soup:
            for row in soup.find_all("div", {"class": "lister-item"}):
                show = {}
                image_div = row.find("div", {"class": "lister-item-image"})
                if image_div:
                    image = image_div.find("img")
                    show['image_url_large'] = self.change_size(image['loadlate'], 3)
                    show['imdb_tt'] = image['data-tconst']
                    show['image_path'] = posixpath.join('images', 'imdb_popular',
                                                        os.path.basename(show['image_url_large']))
                    self.cache_image(show['image_url_large'])

                content = row.find("div", {"class": "lister-item-content"})
                if content:
                    header = row.find("h3", {"class": "lister-item-header"})
                    if header:
                        a_tag = header.find("a")
                        if a_tag:
                            show['name'] = a_tag.get_text(strip=True)
                            show['imdb_url'] = "http://www.imdb.com" + a_tag["href"]
                            show['year'] = header.find("span",
                                                       {"class": "lister-item-year"}).contents[0].split(" ")[0][1:5]

                    imdb_rating = row.find("div", {"class": "ratings-imdb-rating"})
                    show['rating'] = imdb_rating['data-value'] if imdb_rating else None

                    votes = row.find("span", {"name": "nv"})
                    show['votes'] = votes['data-value'] if votes else None

                    outline = content.find_all("p", {"class": "text-muted"})
                    if outline and len(outline) >= 2:
                        show['outline'] = outline[1].contents[0].strip("\"")
                    else:
                        show['outline'] = ''

                    popular_shows.append(show)

            return popular_shows

    @staticmethod
    def change_size(image_url, factor=3):
        match = re.search("^(.*)V1_(.{2})(.*?)_(.{2})(.*?),(.*?),(.*?),(.\d?)_(.*?)_.jpg$", image_url)

        if match:
            matches = match.groups()
            os.path.basename(image_url)
            matches = list(matches)
            matches[2] = int(matches[2]) * factor
            matches[4] = int(matches[4]) * factor
            matches[5] = int(matches[5]) * factor
            matches[6] = int(matches[6]) * factor
            matches[7] = int(matches[7]) * factor

            return "{}V1._{}{}_{}{},{},{},{}_.jpg".format(matches[0], matches[1], matches[2], matches[3], matches[4],
                                                          matches[5], matches[6], matches[7])
        else:
            return image_url

    def cache_image(self, image_url):
        """
        Store cache of image in cache dir
        :param image_url: Source URL
        """
        path = os.path.abspath(os.path.join(sickrage.app.cache_dir, 'images', 'imdb_popular'))

        if not os.path.exists(path):
            os.makedirs(path)

        full_path = os.path.join(path, os.path.basename(image_url))

        if not os.path.isfile(full_path):
            WebSession().download(image_url, full_path)
