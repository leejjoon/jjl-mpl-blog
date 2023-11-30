# ---
# title: "Introducing mpl-speech-bubble"
# author: "Jae-Joon Lee"
# date: "11/30/2023"
# draft: false
# date-modified: "11/30/2023"
# image: https://mpl-speech-bubble.readthedocs.io/en/latest/_images/demo_annotati_bubble.png
#
# jupyter:
#   jupytext:
#     cell_metadata_filter: title,-all
#     formats: ipynb,py:percent
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.15.2
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown]
# In this post, I will introduce mpl-speech-bubble package.
#
# You can install it by
#
# > pip install mpl-speech-bubble
#
# And the source code can be found at https://github.com/leejjoon/mpl-speech-bubble and documentation at https://mpl-speech-bubble.readthedocs.io/ (documentation is far from complete)
#
# With `mpl-speech-bubble`, you can annotate you Matplotlib plot with speech bubbles, like this
#
#
# <img src="https://mpl-speech-bubble.readthedocs.io/en/latest/_images/demo_annotati_bubble.png">
#

# %% [markdown]
# Let's start with a Matplotlib's annotate example. Note that we use "wedge" arrow style. 

# %%
# %matplotlib inline

# %% We start with a Matplotlib's original annotation
import matplotlib.pyplot as plt

fig, ax = plt.subplots(num=1, clear=True)

xy = (0.2, 0.5)
ax.plot([xy[0]], [xy[1]], "o")

annotate_kwargs = dict(
    ha="center", va="bottom",
    size=20,
    bbox=dict(boxstyle="round, pad=0.2",
              fc="w", ec="k"),
    arrowprops=dict(
        arrowstyle="wedge, tail_width=0.5",
        fc="y",
        patchA=None, # by default, annotate set patchA to the bbox.
    )
)

t = ax.annotate(
    text="Default",
    xy=xy, xycoords='data',
    xytext=(-0., .9), textcoords="offset fontsize",
    **annotate_kwargs
)

ax.set_xlim(0, 1)


# %% [markdown]
# `mpl-speech-bubble` has a function `annotate_merged`. This fucntion is mostly identical to MPL's annotate, and at the drawing time, it will merge the bbox patch and the arrow patch. Behind the scence, it uses `skia-pathops` to merge bezier paths. The properties of merged patch will inherid from the bbox patch.

# %% annotate_merge is similar to annotate. But it will combine the bbox patch and arrow.
from mpl_speech_bubble import annotate_merged

xy = (0.5, 0.5)
ax.plot([xy[0]], [xy[1]], "o")

t = annotate_merged(
    ax,
    text="Merged",
    xy=xy, xycoords='data',
    xytext=(-0., .9), textcoords="offset fontsize",
    **annotate_kwargs
)


# %%
#| echo: false
#| warning: false
fig

# %% [markdown]
# In addtion, it provides `annotate-bubble` function. It has slghtly different call signature from `annotate`, but has an advantage of better handling of things like rotation.
#
# Instead of `xytext` and `textcoords`, you should use `loc` and `dist`. The unit of `dist` is fontsize.

# %% annotate_bubble is slightly different. You should use `loc` and `dist`.
from mpl_speech_bubble import annotate_bubble

xy = (0.8, 0.5)
ax.plot([xy[0]], [xy[1]], "o")

t = annotate_bubble(
    ax,
    text="Bubble",
    xy=xy, xycoords='data',
    loc="up", dist=1.,
    size=20,
)




# %%
#| echo: false
#| warning: false
fig

# %%
t = annotate_bubble(
    ax,
    text="Bubble 2",
    xy=xy, xycoords='data',
    loc="down", dist=1.,
    size=20, rotation=30,
)


# %%
#| echo: false

fig

# %% [markdown]
# `annotate_bubble` is a simple wrapper around `AnnotationBubble` class. Please take a look at the example [here](https://mpl-speech-bubble.readthedocs.io/en/latest/examples/speechbuble_test2.html#sphx-glr-examples-speechbuble-test2-py)
