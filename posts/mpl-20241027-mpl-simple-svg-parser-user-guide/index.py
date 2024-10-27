# ---
# title: "Rendering SVG with Matplotlib"
# author: "Jae-Joon Lee"
# date: "10/27/2024"
# draft: false
# date-modified: "10/27/2024"
#
# ---

# %% [markdown]
# # A guide to render SVG in your Matplotlib plot as vector format.
#
# This tutorial demonstrates how one can include svg in Matplotlib, as vector format (i.e.g, Matplotlib's paths). While you can rasterize the svg into an image and include them, we will read the svg file and produce matplotlib path objects. 
#
# We will use (mpl-simple-svg-parser)[https://mpl-simple-svg-parser.readthedocs.io/en/latest/index.html] package. Note that this package is not fully-featured SVG parser. Instead, it uses (cariosvg)[https://cairosvg.org/] and (picosvg)[https://github.com/googlefonts/picosvg] to convert the input svg into a more manageable svg and then read them with the help of (svgpath2mpl)[https://github.com/nvictus/svgpath2mpl]. The package does support gradient in a very ad hoc way. It uses (Skia)[https://skia.org/] to produce gradient image and include them in the matplotlib plot.
#
# While this is not ideal (and not very efficient), this let you render a good fraction of svg wit matlotlib. On the other hand, features like filters are not supported.
#
# Here is an example of annotating your plot with svg.

# %%
#| warning: false
#| code-fold: true

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from matplotlib.offsetbox import AnnotationBbox
from mpl_simple_svg_parser import SVGMplPathIterator


# TIOBE score from https://spectrum.ieee.org/the-top-programming-languages-2023

l = [
    ("Python", 1),
    ("Java", 0.588),
    ("C++", 0.538),
    ("C", 0.4641),
    ("JavaScript", 0.4638),
    ("C#", 0.3973)
]

df = pd.DataFrame(l, columns=["Language", "Score"])


sns.set_color_codes("muted")
sns.set(font_scale = 1.5)

fig, ax = plt.subplots(num=1, clear=True, layout="constrained")

sns.barplot(x="Score", y="Language", data=df,
            label="Tiobe Score 2023", color="b",
            legend=False)

ax.yaxis.label.set_visible(False)
ax.set_title("TIOBE Score 2023")
ax.set_xlim(0, 1.13)

ylabels = [l.get_text() for l in ax.get_yticklabels()] # save it to use with svg icons later
bars = ax.containers[0] # list of rectangles for the bars.

for bar, l in zip(bars, ylabels):
    ax.annotate(l, xy=(0, 0.5), xycoords=bar, va="center", ha="left",
               xytext=(10, 0), textcoords="offset points", color="w")

ax.tick_params(axis="y",labelleft=False)
# ax.tick_params(axis="x",direction="in")

ax.set_xlim(0, 1.2) # to make a room for svg annotattion.

import toml
icons = toml.load(open("svg_icons.toml"))

def get_da(b, ax, wmax=64, hmax=64):
    svg_mpl_path_iterator = SVGMplPathIterator(b)
    da = svg_mpl_path_iterator.get_drawing_area(ax, wmax=wmax, hmax=hmax)
    return da

for l, bar in zip(ylabels, bars):
    da = get_da(icons[l].encode("ascii"), ax, wmax=32, hmax=32)
    ab = AnnotationBbox(da, (1., 0.5), xycoords=bar, frameon=False,
                        xybox=(5, 0), boxcoords="offset points",
                        box_alignment=(0.0, 0.5))
    ax.add_artist(ab)

plt.show()



# %% [markdown]
# # Using `SVGMplPathIterator` from mpl_simple_svg_parser
#
# Let's start with a simple example. The base class is `SVGMplPathIterator`. It reads the svg string, and produces a list of matplotlib's path object. If you want to render the svg in the axes' data coordinate, you may simply use the `draw` method.
#

# %%
import matplotlib.pyplot as plt
from mpl_simple_svg_parser import SVGMplPathIterator

fig, ax = plt.subplots(num=1, clear=True)
ax.set_aspect(1)
fn = "homer-simpson.svg"
svg_mpl_path_iterator = SVGMplPathIterator(open(fn, "rb").read())
svg_mpl_path_iterator.draw(ax)

# %% [markdown]
# You can offset and scale it.

# %%
# First let's check the viewbox of the svg.

svg_mpl_path_iterator.viewbox # This is the size defined in the svg file.

# %%
fig, ax = plt.subplots(num=2, clear=True)
ax.set_aspect(1)
ax.plot([0, 1000], [0, 1000])

fn = "homer-simpson.svg"
svg_mpl_path_iterator = SVGMplPathIterator(open(fn, "rb").read())
svg_mpl_path_iterator.draw(ax, xy=(600, 100), scale=0.7)

# %% [markdown]
# The package mpl-simple-svg-parser processes the input svg content using cairosvg to produce simplified svg. There are some caveats of drawing the result with matplotlib. For example, linewidth in Matplotlib cannot be specified in the data coordinate. In the example below, 
# the arms and legs of the robot is too thin because of this issue.

# %%
fig, ax = plt.subplots(num=3, clear=True)
ax.set_aspect(1)
fn = "android.svg"
svg_mpl_path_iterator = SVGMplPathIterator(open(fn, "rb").read())
svg_mpl_path_iterator.draw(ax)


# %% [markdown]
# Besides the stroke width issue, the package does not handle clipping.
#
# Turning on the option "pico=True" can solve some of the issues. With this option, the svg is further processed by picosvg which converts strokes to fills and clips the paths. Running pico has its own caveats though. You may check this (page)[https://leejjoon.github.io/mpl-simple-svg-parser/gallery/] and check the results.

# %%
fig, ax = plt.subplots(num=4, clear=True)
ax.set_aspect(1)
fn = "android.svg"
svg_mpl_path_iterator = SVGMplPathIterator(open(fn, "rb").read(), pico=True)
svg_mpl_path_iterator.draw(ax)


# %% [markdown]
# The package does support gradient. While the result is reasonable, the implementation is quite naive and not efficient. It uses Skia (or Cairo) to produce gradient image, and let the
# matplotlib's backends to clip it.

# %%
fig, ax = plt.subplots(num=5, clear=True)
ax.set_aspect(1)
fn = "python.svg"
svg_mpl_path_iterator = SVGMplPathIterator(open(fn, "rb").read())
svg_mpl_path_iterator.draw(ax)


# %% [markdown]
# Sometimes, the viewbox size in the svg can be incorrect. You can set datalim_mode='path' to ignore the viewbox,
# and try to let matplotlib guess its extent based on extent of individual patches (this can be incorrect sometime.)

# %%
fig, ax = plt.subplots(num=6, clear=True)
ax.set_aspect(1)
fn = "tiger.svg"
svg_mpl_path_iterator = SVGMplPathIterator(open(fn, "rb").read(), pico=True)
svg_mpl_path_iterator.draw(ax, datalim_mode="path")

# %% [markdown]
# And we can render Matplotlib logo!

# %%
fig, ax = plt.subplots()
ax.set_aspect(1)
fn = "matplotlib-original-wordmark.svg"
svg_mpl_path_iterator = SVGMplPathIterator(open(fn, "rb").read(), pico=True)
svg_mpl_path_iterator.draw(ax, datalim_mode="path")

ax.tick_params(labelleft=False, labelbottom=False)


# %% [markdown]
# # DrawingArea
#
# For the examples so far, we draw the svg in Matplotlb's data coordinates. Often, you want your svg rendering results, behaves like text, whose size is set in points, independent of data coordinates.
#
# Instead of drawing it direcly on the axes, it is recommented to draw it on DrawingArea -- derived from [OffsetBox]( https://matplotlib.org/stable/api/offsetbox_api.html) -- and use [AnnotationBbox](https://matplotlib.org/stable/gallery/text_labels_and_annotations/demo_annotation_box.html) to place it on the axes similar to annotation.
#

# %%
from matplotlib.offsetbox import AnnotationBbox

fig, ax = plt.subplots(num=7, clear=True)
fn = "python.svg"
svg_mpl_path_iterator = SVGMplPathIterator(open(fn, "rb").read())
da = svg_mpl_path_iterator.get_drawing_area(ax, wmax=64)

ab = AnnotationBbox(da, (0.5, 0.5), xycoords="data")
ax.add_artist(ab)

# %% [markdown]
# # Annotation Example
#
# Let's make a barplot and annotate it with svgs.
#
# We start with a boxplot

# %%
#| echo: false
#| warning: false
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

from matplotlib.offsetbox import AnnotationBbox
from mpl_simple_svg_parser import SVGMplPathIterator

# TIOBE score from https://spectrum.ieee.org/the-top-programming-languages-2023
l = [
    ("Python", 1),
    ("Java", 0.588),
    ("C++", 0.538),
    ("C", 0.4641),
    ("JavaScript", 0.4638),
    ("C#", 0.3973)
]

df = pd.DataFrame(l, columns=["Language", "Score"])

sns.set_color_codes("muted")
sns.set(font_scale = 1.5)

fig, ax = plt.subplots(num=1, clear=True, layout="constrained")

sns.barplot(x="Score", y="Language", data=df,
            label="Tiobe Score 2023", color="b",
            legend=False)

ax.yaxis.label.set_visible(False)
ax.set_title("TIOBE Score 2023")

ylabels = [l.get_text() for l in ax.get_yticklabels()] # save it to use with svg icons later
bars = ax.containers[0] # list of rectangles for the bars.

for bar, l in zip(bars, ylabels):
    ax.annotate(l, xy=(0, 0.5), xycoords=bar, va="center", ha="left",
               xytext=(10, 0), textcoords="offset points", color="w")

ax.tick_params(axis="y",labelleft=False)
# ax.tick_params(axis="x",direction="in")

ax.set_xlim(0, 1.2) # to make a room for svg annotattion.

# %% [markdown]
#
# We annotate the plot with svg in drawing_area.

# %%
# We will use svg icons downloaded from (devicons)[https://github.com/devicons/devicon]

import toml
icons = toml.load(open("svg_icons.toml"))
icons["Python"]


# %%
def get_da(b, ax, wmax=64, hmax=64):
    svg_mpl_path_iterator = SVGMplPathIterator(b)
    da = svg_mpl_path_iterator.get_drawing_area(ax, wmax=wmax, hmax=hmax)
    return da

for l, bar in zip(ylabels, ax.containers[0]):

    da = get_da(icons[l].encode("ascii"), ax, wmax=32, hmax=32)
    ab = AnnotationBbox(da, (1., 0.5), xycoords=bar, frameon=False,
                        xybox=(5, 0), boxcoords="offset points",
                        box_alignment=(0.0, 0.5))
    ax.add_artist(ab)

# %%
#| echo: false
#| warning: false
fig

# %% [markdown]
# # Accessing the parsed results
#
# Once can access the parsed results. The base methods would be 'iter_path_attrib' and 'iter_mpl_path_patch_prop'.

# %%
fn = "python.svg"
svg_mpl_path_iterator = SVGMplPathIterator(open(fn, "rb").read())


# %%
list(svg_mpl_path_iterator.iter_path_attrib())

# %%
list(svg_mpl_path_iterator.iter_mpl_path_patch_prop())
