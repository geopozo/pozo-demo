"""A marimo roadmap showcasing what we plan to do with pozo-py."""

import marimo

__generated_with = "0.18.1"
app = marimo.App()


@app.cell(hide_code=True)
async def _():
    ## The following more advanced code allows this notebook to run everywhere.
    ## Jupyter/marimo offer web-only python, using slightly different pips.
    import sys

    if "pyodide" in sys.modules:  # Are we running pyodide- browser based python?
        try:
            import piplite  # Try the jupyter-style webpip install

            await piplite.install("pozo-demo")
        except ImportError:  # It's not jupyter
            try:
                import micropip  # Try the marimo-style webpip install

                await micropip.install(
                    "/public/pozo_demo-0.0.1-py3-none-any.whl",
                )
            except ImportError:
                pass

    # This is our package that we use to make errors prettier
    # for features that don't work yet
    from pozo_demo import rich_error

    return (rich_error,)


@app.cell
def _(rich_error):
    import marimo as mo  # this notebook

    pozo = type("pozo", (), {})()
    pozo.__version__ = -1
    try:
        import lasio  # reads LAS files
        import pozo  # visualize well logs
    except Exception as e:
        rich_error(e)
    return lasio, mo, pozo


@app.cell(hide_code=True)
def _(mo, pozo):
    mo.md(f"""
    # The Roadmap for pozo-py: Where *Are* We Going?

    This document shows off what we can and what we plan on doing:
    that's why some things work, and some things don't.

    It was build using pozo {pozo.__version__}.

    If you want to make suggestions, you can add an issue to our
    [github](https://github.com/geopozo/pozo-demo/issues) (preferred)
    or send an email to roadmap@geopozo.com with the subject _Feature Suggestion_.

    ## 🏠 Can I run this notebook at home?

    Sure, we recommend [uv](https://docs.astral.sh/uv/):

    ```shell
    uvx pozo roadmap
    ```

    Or with pip:

    ```shell
    pip install pozo
    pozo roadmap
    ```

    Both commands will create a new marimo notebook (this) wherever you run them.

    See the README.md for jupyter instructions.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 📊 How to Import Data

    ### 🪨 LAS 1.2/2.0

    You can use [lasio](www.github.com/kinverity/lasio)
    to read LAS files directly into python.

    First, install it:

    ```shell
    pip install lasio
    # or
    uv add lasio
    ```

    Then, you can use that directly to create a new pozo graph:
    """)
    return


@app.cell
def _(lasio, pozo, rich_error):
    # All of our examples in this demo are wrapped in try/except, but it's
    # not necessary during usage.
    try:
        las = lasio.read("SALADIN.LAS")
        _g = pozo.Graph(las)  # pozo.Graph(las)
        _g.render_sparks()  # render_sparks is one type of render, we'll show more later

    except Exception as e:
        rich_error(e)
    return (las,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔢 Dataframes

    You may already have your data as a dataframe, using a package like pandas,
    polars, or pyarrow or any common datascience dataframe library. The column
    headers will become the mnemonics.

    _Note: dataframes are basically a table with columns and rows_
    """)
    return


@app.cell
def _(df, pozo, rich_error):
    try:
        _g2 = pozo.Graph(df)  # df is the name of your variable
        _g2.render_sparks()

    except Exception as e:
        rich_error(e)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🔢 Series, Tensors, Arrays

    Perhaps you have one or more array-like data objects.
    You can add them inside of a python dictionary.

    ⚠️ You cannot use native python lists `[]` or tuples `()`, those are not
    for data analysis. Look at how I convert them in the example below.
    """)
    return


@app.cell
def _(np, pozo, rich_error):
    try:
        curve1 = np.ndarray([1, 2, 3])  # example data
        curve2 = np.ndarray([4, 5, 6])  # example data
        curves = {"GR": curve1, "CALI": curve2}
        _g3 = pozo.Graph(curves)  # TODO: Depth
        _g3.render_sparks()

    except Exception as e:
        rich_error(e)
    return curve1, curve2, curves


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 📐 Specifying Units

    We use [pint](https://github.com/hgrecco/pint) to specify units. When you
    import a LAS file, we use its unit data to guess the units (see later for
    cleaning data). But when you're importing something *manually* one-by-one,
    its a bit more tedious. You have two options for specifying units:

    See [cleaning data](#cleaning-data) below as well.
    """)
    return


@app.cell
def _(curve1, curve2, curves, pozo, rich_error):
    try:
        # Option 1: You can wrap the curves in the pint.Quantity wrapper:
        ucurve1 = pozo.units.Q(curve1, "gAPI")
        ucurve2 = pozo.units.Q(curve2, "inches")
        ucurves = {"GR": ucurve1, "CALI": ucurve2}
        _g3 = pozo.Graph(ucurves)  # TODO: Depth
        _g3.render_sparks()

        # Option 2: You can specify units in a separate map w/ the original curves
        _g4 = pozo.Graph(
            curves,
            unit_map={
                "GR": "gAPI",
                "CALI": "inches",
            },
        )
        _g4.render_sparks()

    except Exception as e:
        rich_error(e)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 📈 Visualizing the Well Logs

    There are three basic render functions, two simple and one main.

    Note: Usually we call the `render()` function *as the last line of a cell*.
    You don't have to, you can also use the notebook API, if you look it up.

    ### ⚡ Simple Renderers
    """)
    return


@app.cell
def _(las, pozo, rich_error):
    try:
        # This graph is not very customizable, and is only used for a preview.
        pozo.Graph(las).render_spark()
    except Exception as e:
        rich_error(e)
    return


@app.cell
def _(las, pozo, rich_error):
    try:
        # This graph is also a preview, but a bit more interactive.
        # All render functions take an exclude or include argument with a list/tuple
        # of mnemonics, but neve both.
        pozo.Graph(las).render_summary(exclude=["GR"])
    except Exception as e:
        rich_error(e)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🛢️ Main Renderer

    The main renderer produces the largest most interactive graph. Its not
    useful until you customize it, but we'll show it uncustomized first.

    Furthermore, after we talk about these basic customizations and the internal
    structure of our graph, we'll introduce you to **crossplots**, **intervals**
    (annotations and tops), and **making movies** in later sections.
    """)
    return


@app.cell
def _(las, pozo, rich_error):
    try:
        # The main render function will produce the best graph.
        pozo.Graph(las).render()
    except Exception as e:
        rich_error(e)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🎨 Designing your Graph *Layout*

    There a couple ways to customize your graph *layout*. You can specify a template to
    use everytime, or you can modify it bit by bit with functions.

    ### 🧩 Simple Template
    """)
    return


@app.cell
def _(las, pozo, rich_error):
    try:
        # A simple template might group mnemonics onto tracks, and display them in order
        simple = (["CGR", "CALI"], ["LLD", "ILD", "ILM", "LLS"], ["RHOB", "NPHI"])

        # You don't even need groups
        _other_option = ("CGR", "CALI", "LLD", "ILD", "ILM", "LLS", "RHOB", "NPHI")

        # Then create the graph
        pozo.Graph(las, template=simple).render()

    except Exception as e:
        rich_error(e)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🧩🧩 Compound Template
    """)
    return


@app.cell
def _(Path, las, pozo, rich_error):
    try:
        # Or you might produce a more complicated "full service" template:

        # TODO How do we guess units?

        track1 = {
            "axes": {
                "GR": {
                    "mnemonics": [
                        "CGR",
                        "GR",
                        "SGR",
                    ],  # Look for multiple mnemonics, choose the first
                    "optional": False,  # Indicate On the graph if data not found
                    "function": lambda x,
                    _: x,  # See note below for function specifications
                },
                "CALI": {
                    "mnemonics": ["CALI"],
                    "optional": True,  # Hide the axis if the mnemonic can't be found
                    "theme": {
                        ...,  # A custom theme for this axis (see the theming section)
                    },
                },
            },
            "theme": {
                ...,  # set a theme on the whole track.
            },
        }

        track2 = {
            "axes": {
                "LLS": {
                    "mnemonics": ["LLS"],
                    "optional": RuntimeError,  # RuntimeError if data not found
                },
            },
        }

        # Combine the tracks into a dictionary
        template_dict = {
            "tracks": [track1, "y", track2],
            "theme": ...,  # Set a theme on the whole graph
        }

        # Turn the dictionary into a template (verifies structure)
        template = pozo.Template(
            template_dict,
        )

        # You can save it
        template_file = Path("./template.json")
        template_file.dump_text(
            template.to_json(),
        )  # And share it!

        graph = pozo.Graph(
            las,
            template=template_file,  # specify the dict, Template, or JSON path
        )

    except Exception as e:  # or []
        rich_error(e)
    return (graph,)


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 🧮 Specifying Functions in Templates

    If you've specified your template in python, you can use lambda functions and
    regular python functions as values. The functions are passed the entire curve-
    not element by element, and a dict of the other curves if you need them.

    ```python
    def identity(curve, graph): # my function, the identity function f(x) = x
        return curve

    template = {
        ... # axis, theme etc
        "function": identity,
    }

    # or

    template2 = {
        ... # axis, theme etc
         # moving average of 3 samples
        "function": lambda curve, _: np.convolve(curve, np.ones(3)/3, mode="valid")
    }
    ```

    However, if you're using JSON, you can't embed python directly,
    so we use standard PEP621 function specification syntax:

    `module.submodule:functioname`

    Pozo will find the function you want to use by that address. The `module.submodule`
    can be the name of a file that has your math, as long as that file resides in the
    same directory as the notebook. If your file is "extra_math.py" and you have a
    function "drill_filter", you would write `extra_math:drill_filter`.

    You can technically specify functions from other packages: `numpy:some_function`,
    but that assumes it works out-of-the-box and that the user has numpy installed.

    As a last customization, if you pass the string like this: `:functioname`,
    pozo will look for that function in the currently imported *global* environment.
    Therefore, the following two specifications are the same:

    ```python
    template = {
        "function": identity,
        "function": ":identity",
    }
    ```

    ##### Advanced

    Do you need to control the ordering of the math processing or share state
    variables?

    At this point, frankly, you should consider *writing a python package* instead of
    embedding your logic in a JSON, however, you have two helper functions:

    ```python
    def my_function(curve, graph):
        graph.state["my_key"] = "some_value" # accessible to other functions

         # idempotent- every curve function runs only once
        graph.run_curve_function("AxisName")
    ```

    However, you are responsible for ensuring there are no cycles between processing,
    ie that two curves do not depend on each other.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🛠️ Modifying Your Design

    You can also modify the graph object with a *wide* variety of functions.

    #### 🏭 Internal Structure of Graph

    Let's jump right in with an example:
    """)
    return


@app.cell
def _(graph, rich_error):
    try:
        graph.show_config()
        # graph.show_template() will print a template of your graph

    except Exception as e:
        rich_error(e)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    You can use functions to modify each:
    """)
    return


@app.cell
def _(graph, graph_2, rich_error):
    try:
        selector = "CGR"
        # Mnemonics are generally the most common selectors, but you can also
        # use the position index, starting from 0

        graph.get_track(selector)  # gets whole track containing trace CGR
        graph.get_axis(selector)  # gets whole axis container trace CGR
        graph.get_trace(selector)  # gets exact CGR trace

        my_track = graph.pop_track(selector)  # gets but also removes whole track
        my_axis = graph.pop_axis(selector)
        my_trace = graph_2.pop_trace(selector)

        graph.add_track(selector)  # Add a track to the graph
        graph.add_axis(selector)
        graph.add_trace(selector)

        # TODO: don't forget about replace

        graph.remove_track(selector)  # Remove whole track
        graph.remove_axis(selector)
        graph.remove_trace(selector)

    except Exception as e:
        rich_error(e)  # So now it has tracks, it has axes
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🖌️ Set a Theme

    **TODO: EXPAND THIS SECTION AS YOU RE-ADD THE MODULE**
    """)
    return


@app.cell
def _(axis, pozo, rich_error, trace, track):
    try:
        track.get_theme()
        axis.set_theme()
        trace.set_theme()

        pozo.new_theme()  # <-- return blank dictionary
        # what can the theme work on?

        # what about using plotly traces
    except Exception as e:
        rich_error(e)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🧹 Cleaning Data

    This is boring, but necessary.

    Your LAS file or other data may come to you in a weird way:

    1. Broken non-sensical data and curves
    2. Non-standard unit abbreviations
    3. A whole bad LAS file with missing data

    There is las_check package which can verify a las file, you can also open the
    LAS files and fix simple things (it's a text file).

    ### 🔬 Unit Analysis
    """)
    return


@app.cell
def _(las, pozo, rich_error):
    try:
        pozo.units.check_las(las)
    except Exception as e:
        rich_error(e)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### ⚖️ Adding Units

    **TODO EXPAND THIS MODULE AS YOU READD THE MODULE**
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 📊 More Advanced Visualization

    #### ⚔️ CrossPlots
    """)
    return


@app.cell
def _(graph, pozo, rich_error):
    try:
        # Create a cross plot
        xp = pozo.CrossPlot(
            x=graph.get_trace("NPHI"),
            y=graph.get_trace("RHOB"),
            colors={"depth": graph.get_trace("GR").get_depth()},
            xrange=(45, -15),  # should take units
            yrange=(1.95, 2.945),  # should take units
            size=800,
            depth_range=(1100, 1300),
        )
        xp.render()
    except Exception as e:
        rich_error(e)
    return (xp,)


@app.cell
def _(graph, rich_error, xp):
    try:
        # You can add it as a track
        graph.add_track(xp)
        graph.render()
    except Exception as e:
        rich_error(e)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### ↔️ Intervals
    """)
    return


@app.cell
def _(axis, graph, pozo, rich_error, track):
    try:
        segment1 = {
            "interval": 1105,
            "line": {"color": "#00FFFFF"},
            "text": "Mardie Greensand",
        }
        segment2 = {
            "interval": (1115, 1125),
            "line": {"color": "green"},
            "text": "Mardie Greensand",
        }
        segment3 = {
            "interval": (1125, None),  # None goes to end
            "line": {"color": "#FFFFF00"},
            "text": "Other",
        }
        intervals_dict = [segment1, segment2, segment3]
        intervals = pozo.Intervals(intervals_dict)  # this will verify your dictionary
        graph.add_intervals(
            intervals,
        )  # Add to whole graph, can also add an intervals_dict
        track.add_intervals(intervals)  # Add to one track, sames rules as above
        axis.add_intervals(
            intervals,
        )  # Stays with axis, but looks like added to one track, same rules as above
        graph.add_track(intervals)  # Add a tops-like track, must be an interval object
        # Change width w/ a theme
    except Exception as e:
        rich_error(e)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### Videos

    Warning: videos cannot be rendered in the online environment, please see [choose
    your datascience adventure](where) to set up pozo on your own computer.

    TODO: Put here when you readd module
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## 🧮 Manipulating Data

    There are lots of datascience libraries, and while we won't be doing a tutorial
    on how to use each one, we'll be showing you here patterns you can use to
    interact with some of the common ones.

    ### 🐍 Numpy

    Numpy sometimes modifies data in-place, sometimes creates a copy. Its best to
    use a reference document or talk to AI so you know.
    """)
    return


@app.cell
def _(graph, np, rich_error):
    try:
        data = graph.get_trace("MNEMONIC").get_data()

        data += 10
        # the graph is now changed!

        graph.render_spark(include=["MNEMONIC"])

        # Some numpy functions modify data in place, and we just did
        # But a lot of current opinion is that making data-science pipelines
        # like this is sloppy, even if slightly more memorize optimized. Let's go back:

        data -= 10  # undo the + 10

        # Lets redo it in a more popular style:

        norm = (
            graph.get_trace("MNEMONIC").get_data().copy()
        )  # it's a numpy array, we can call copy()

        norm /= np.maxnan(norm) - np.minnan(
            norm,
        )  # we know have a normalized ratio between 0 and 1

        graph.get_trace("MNEUMONIC").set_data(
            norm,
        )  # replace the data we use on that trace
    except Exception as e:
        rich_error(e)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 🔬 Comparing Curves

    Sometimes its useful to compare curves,and maybe you want to do it in
    different ways.

    **First, lets make some modified data:**
    """)
    return


@app.cell
def _(graph, np, rich_error):
    try:
        original_trace = graph.get_trace("MNEMONIC")  # get the trace

        # lets smooth the curve
        smoothed = np.convolve(  # convolve always return a copy
            original_trace.get_data(),
            np.ones(3) / 3,
            mode="valid",
        )
    except Exception as e:
        rich_error(e)
    return original_trace, smoothed


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ##### 🧑‍🔬🧑‍🔬 Side-By-Side
    """)
    return


@app.cell
def _(graph, rich_error, smoothed):
    try:
        # Create a copy of the track so we can see the new data in context
        t = graph.get_track("MNEMONIC")  # get the whole track
        t_new = t.lazy_copy()

        # Set data on the copy
        t_new.get_trace("MNEMONIC").set_data(smoothed)
        graph.render(include=[t, t_new])  # render a bit modified
    except Exception as e:
        rich_error(e)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    #### 📊 Same Axis
    """)
    return


@app.cell
def _(graph, original_trace, pozo, rich_error, smoothed):
    try:
        a_new = pozo.Axis(  # Create a single axis with a trace and a copy
            original_trace,
            original_trace.lazy_copy(),
        )
        a_new[1].set_data(smoothed)  # Change the copy's data

        graph.render(include=[a_new])
    except Exception as e:
        rich_error(e)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ### 🐼 Dataframe (Polars/Pandas)

    I want to use the graph as if it were a dataframe, how do we get there?
    We would generally then create a *second graph structure*.
    Take one table (original) and make a new table (modified).
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Index Analysis

    We we can generally plot data with different y-axes as long as they all use the
    same units. If you're adding data in feet and meters, you have to to manually
    do a conversion.

    ```python
    # TODO: show conversion
    ```

    But since you have to keep track of the y-axis to do a lot of math, we provide
    a few utility functions to help you understand the state of your y-axis:

    ```python
    graph.config(y_stats=True)
    ```

    This will show you you what data is using the same y-axis array, what data
    is using interval data, and what data has evenly sampled y-axis data.
    """)
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""
    ## Export

    TODO: show
    """)
    return


if __name__ == "__main__":
    app.run()
