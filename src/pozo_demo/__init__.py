"""Internal tools for pozo-demo notebooks."""

from __future__ import annotations

from io import StringIO
from typing import TYPE_CHECKING

from IPython import get_ipython  # type: ignore[reportPrivateImportUsage]
from rich.console import Console
from rich.traceback import Traceback

if _in_jupyter := bool(get_ipython()):
    from IPython.display import HTML, display
else:
    import marimo as mo

if TYPE_CHECKING:
    ...


def _html(c: Console):
    o = c.export_html()
    if _in_jupyter:
        display(HTML(o))  # type: ignore[reportPossiblyUnboundVariable]
    else:
        mo.output.append(mo.Html(o))  # type: ignore[reportPossiblyUnboundVariable]


# would be better to use filestreems with new consoles
_c = Console(record=True, file=StringIO(), force_jupyter=False)


def rich_error(e):
    """Print an error nicely."""
    tb = Traceback.from_exception(type(e), e, e.__traceback__)

    _c.print(tb)
    _html(_c)
