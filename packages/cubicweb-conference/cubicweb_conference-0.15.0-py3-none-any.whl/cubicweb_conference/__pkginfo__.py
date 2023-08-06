# pylint: disable-msg=W0622
"""cubicweb-conference application packaging information"""

import sys
from os import listdir as _listdir
from os.path import join, isdir
from glob import glob

modname = "conference"
distname = "cubicweb-%s" % modname

numversion = (0, 15, 0)
version = ".".join(str(num) for num in numversion)

license = "LGPL"
description = "conference component for the CubicWeb framework"
author = "Logilab"
author_email = "contact@logilab.fr"
web = "https://www.cubicweb.org/project/%s" % distname

classifiers = [
    "Environment :: Web Environment",
    "Framework :: CubicWeb",
    "Programming Language :: Python",
    "Programming Language :: JavaScript",
]

__depends__ = {
    "cubicweb": ">= 3.26.19,<3.27",
    "cubicweb-addressbook": None,
    "cubicweb-card": ">= 0.4.0,<0.6",
    "cubicweb-comment": None,
    "cubicweb-file": None,
    "cubicweb-tag": None,
    "cubicweb-seo": ">=0.3" if sys.version_info.major >= 3 else "<0.3",
    "six": None,
}

# packaging ###

THIS_CUBE_DIR = join("share", "cubicweb", "cubes", modname)


def listdir(dirpath):
    return [
        join(dirpath, fname)
        for fname in _listdir(dirpath)
        if fname[0] != "."
        and not fname.endswith(".pyc")
        and not fname.endswith("~")
        and not isdir(join(dirpath, fname))
    ]


data_files = [
    # common files
    [THIS_CUBE_DIR, [fname for fname in glob("*.py") if fname != "setup.py"]],
]
# check for possible extended cube layout
for dirname in (
    "entities",
    "views",
    "sobjects",
    "hooks",
    "schema",
    "data",
    "i18n",
    "migration",
    "wdoc",
):
    if isdir(dirname):
        data_files.append([join(THIS_CUBE_DIR, dirname), listdir(dirname)])
# Note: here, you'll need to add subdirectories if you want
# them to be included in the debian package
