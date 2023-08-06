# -*- encoding: utf-8 -*-
#
# (c) 2021 David Garcia (@dgarcia360)
# This code is licensed under MIT license (see LICENSE.md for details)

from sphinx.application import Sphinx
from typing import Any, Dict, List
import re

from bs4 import BeautifulSoup, Tag

from navigation_icons.utils import split_list_by_commas


class IconsNavigationTree():

    def __init__(self, toctree_html: str):
        self.toctree_html = toctree_html

    def build_html(self) -> str:
        """Returns the given navigation tree with icons."""
        if not self.toctree_html:
            return self.toctree_html

        soup = BeautifulSoup(self.toctree_html, "html.parser")

        for element in soup.find_all("a", recursive=True):
            content = element.string

            icon_match = re.search(r'^_icon\[(.*?)\]', content)

            if icon_match:
                icon = icon_match.group(0)
                icon_classes = split_list_by_commas(
                    icon.replace('_icon[', '').replace(']', ''))
                icon_tag = soup.new_tag("i", attrs={"class": icon_classes})
                element.string = element.string.replace(icon, '')
                element.insert(0, icon_tag)
        return str(soup)


def get_navigation_icons_tree(
    app: Sphinx,
    pagename: str,
    templatename: str,
    context: Dict[str, Any],
    doctree: Any,
) -> None:

    if "toctree" in context:
        toctree = context["toctree"]
        toctree_html = toctree(
            collapse=False,
            titles_only=True,
            maxdepth=-1,
            includehidden=True)
    else:
        toctree_html = ""

    icons_navigation_tree = IconsNavigationTree(toctree_html).build_html()
    context["icons_navigation_tree"] = icons_navigation_tree


def setup(app):
    app.connect('html-page-context', get_navigation_icons_tree)

    return {
        'version': '0.1',
        'parallel_read_safe': True,
        'parallel_write_safe': True,
    }
