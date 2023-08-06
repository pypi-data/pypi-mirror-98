
from setuptools import setup
import ezpip

with ezpip.packager(develop_dir = "./_develop_mult/") as p:
    setup(
        name = "mult",
        version = "0.0.0",
        description = "Parallel Computing Tools (This is a tool to achieve clear and safe management of memory and other resources by separating parallel computations in units of files.)",
        author = "bib_inf",
        author_email = "contact.bibinf@gmail.com",
        url = "https://github.co.jp/",
        packages = p.packages,
        install_requires = ["relpath", "sout"],
        long_description = p.long_description,
        long_description_content_type = "text/markdown",
        license = "CC0 v1.0",
        classifiers = [
            'Programming Language :: Python :: 3',
            'Topic :: Software Development :: Libraries',
            'License :: CC0 1.0 Universal (CC0 1.0) Public Domain Dedication'
        ]
    )
