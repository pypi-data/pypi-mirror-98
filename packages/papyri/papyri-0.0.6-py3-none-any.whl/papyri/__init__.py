"""
Papyri – in progress

Here are a couple of documents, or docstrings that are of interest to see how
papyri works, generally because they crashed papyri at some point during the
developement, and/or do not work yet.:: 


Installation
------------

pip install papyri

Usage
-----

  $ papyri gen <module name>

  $ papyri ingest ...

  $ papyri render

  $ papyri browse ....

  $ papyri serve


Of Interest
-----------

`dask.delayed.delayed`
    one of the parameter of the docstring has multiple paragraphs.

`IPython.core.display.Video.__init__`
    Block Verbatim in params ?

`IPython.core.interactiveshell.InteractiveShell.complete`
    contain a `DefListItem`

`matplotlib.transforms.Bbox`
    parsing of example is completely incorrect.

`matplotlib.axes._axes.Axes.text`
    misparse example as well.

`IPython.core.completer.Completion`
    item list

`matplotlib.figure.Figure.add_subplot` 
    custom double dot example

`matplotlib.colors`
    unnumbered list with indent.

`matplotlib.colors` 
    contain a reference via ``.. _palettable: value`` and autolink ``paletable_``.

`numpy.npv`
    hase warning sections.

`scipy.signal.ltisys.bode`
    contains multiple figure

`scipy.signal.barthann`
    multiple figures

`numpy.where`
    The Parameter section have a pair of parameter separated with the coma in
    the name field; and those parameter should be properly detected as local
    references in the rest of the docstrings.

`numpy.polynomial.laguerre.lagfit`
    should have plenty of math items


`numpy.polyfit`
    The see also section links to `scipy.interpolate.UnivariateSpline` which
    will not resolve (yet) as the fully qualified name is
    `scipy.interpolate.fitpack2.UnivariateSpline`; this should be fixed at some
    points via aliases; in the intro one link as a ``name <value>`` syntax which
    is also not yet recognized.

`scipy.signal.filter_design.zpk2sos`:
    multi blocks in enumerated list

`scipy.signal.filter_design.zpk2sos`:
    blockquote insted of enumerate list (to fix upstream)

`scipy.optimize._lsq.trf`:
    has lineblocks, which I belive is wrong. 

`scipy.signal.exponential`:
    multiple figures

`numpy.einsum`:
    one of the longest numpy docstring/document, or at least one of the longest to render, with
    `scipy.signal.windows.windows.dpss` , `scipy.optimize._minimize.minimize` and
    `scipy.optimize._basinhopping.basinhopping`


"""


from pathlib import Path
from typing import List
from . import examples
from functools import lru_cache

import zipfile
import io


import typer

__version__ = "0.0.6"

logo = r"""
  ___                    _
 | _ \__ _ _ __ _  _ _ _(_)
 |  _/ _` | '_ \ || | '_| |
 |_| \__,_| .__/\_, |_| |_|
          |_|   |__/
"""

app = typer.Typer(
    help="""

Generate Rich documentation for IPython, Jupyter, and publish online.

Generating Docs:

    To generate documentation IR for publishing.

    $ papyri gen numpy

    Will generate in CWD the folder `numpy_$numpyversion`.

Ingesting Docs:

    To crosslink a given set of IR with current existing documentation IRs

    $ papyri ingest numpy_$numpyversion [....]

Generating standalone HTML for all the known docs

    $ papyri render

To start a server that generate html on the fly

    $ papyri serve

View w given function docs in text with ansi coloring

    $ papyri ascii numpy.linspace


"""
)


def _intro():
    print(logo)
    print(__version__)


def main():
    app()


@app.command()
def ingest(paths: List[Path], check: bool = False):
    _intro()
    from . import crosslink as cr

    for p in paths:
        cr.main(Path(p), check)
    cr.relink()


@app.command()
def install(names: List[str], check: bool = False):

    from tempfile import TemporaryDirectory
    from . import crosslink as cr

    _intro()

    @lru_cache
    def get(name):
        import requests

        r = requests.get(f"https://pydocs.github.io/pkg/{name}.zip")
        return r.content

    for name in names:
        data = get(name)
        print(len(data))

        zf = zipfile.ZipFile(io.BytesIO(data), "r")
        with TemporaryDirectory() as d:
            zf.extractall(d)
            cr.main(next(iter([x for x in Path(d).iterdir() if x.is_dir()])), check)
    cr.relink()


@app.command()
def relink():
    _intro()
    from . import crosslink as cr

    cr.relink()


@app.command()
def gen(
    names: List[str],
    infer: bool = typer.Option(
        True, help="Whether to run type inference on code examples."
    ),
    exec: bool = typer.Option(
        False, help="Whether to attempt to execute doctring code."
    ),
):
    """
    Generate documentation for a given package.

    First item should be the root package to import, if subpackages need to be
    analyzed  but are not accessible from the root pass them as extra arguments.

    """
    _intro()
    from papyri.gen import gen_main

    gen_main(names, infer=infer, exec_=exec)


@app.command()
def render(ascii: bool = False, html: bool = True, dry_run: bool = False):
    _intro()
    import trio

    from .render import main as m2

    trio.run(m2, ascii, html, dry_run)


@app.command()
def ascii(name: str):
    _intro()
    import trio

    from .render import ascii_render

    trio.run(ascii_render, name)


@app.command()
def serve():
    _intro()
    from .render import serve

    serve()


@app.command()
def serve_static():
    import http.server
    import socketserver

    PORT = 8000
    from papyri.config import html_dir

    class Handler(http.server.SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(html_dir), **kwargs)

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print(f"serving at http://localhost:{PORT}")
        httpd.serve_forever()


@app.command()
def browse(qualname: str):

    from papyri.browser import main as browse

    browse(qualname)


@app.command()
def open(qualname: str):
    _intro()
    import webbrowser

    from .config import html_dir

    path = html_dir / (qualname + ".html")
    if not path.exists():
        import sys

        sys.exit("No doc for " + qualname + f" ({path})")
    print("opening", str(path))
    webbrowser.get().open("file://" + str(path), new=1)


if __name__ == "__main__":
    main()
