# -*- coding: utf-8 -*-
"""
    pygments.styles.bw
    ~~~~~~~~~~~~~~~~~~

    Simple black/white only style.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""

from testflows._core.contrib.pygments.style import Style
from testflows._core.contrib.pygments.token import Keyword, Name, Comment, String, Error, \
     Operator, Generic


class BlackWhiteStyle(Style):

    background_color = "#ffffff"
    default_style = ""

    styles = {
        Comment:                   "italic",
        Comment.Preproc:           "noitalic",

        Keyword:                   "bold",
        Keyword.Pseudo:            "nobold",
        Keyword.Type:              "nobold",

        Operator.Word:             "bold",

        Name.Class:                "bold",
        Name.Namespace:            "bold",
        Name.Exception:            "bold",
        Name.Entity:               "bold",
        Name.Tag:                  "bold",

        String:                    "italic",
        String.Interpol:           "bold",
        String.Escape:             "bold",

        Generic.Heading:           "bold",
        Generic.Subheading:        "bold",
        Generic.Emph:              "italic",
        Generic.Strong:            "bold",
        Generic.Prompt:            "bold",

        Error:                     "border:#FF0000"
    }
