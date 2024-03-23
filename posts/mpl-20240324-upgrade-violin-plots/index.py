# ---
# title: "Upgrade your violinplot with mpl-visual-context"
# author: "Jae-Joon Lee"
# date: "03/24/2024"
# draft: false
# date-modified: "03/24/2024"
# categories:
#   - tutorial
#   - mpl-visual-context
# ---

# %% [markdown]
# In this post, I will introduce [`mpl-visual-context`](https://mpl-visual-context.readthedocs.io/en/latest/index.html) and how you can upgrade your violinplot and make it more fancy.
#
#
# ```shell
# pip install mpl-visual-context
# ```

# %%
#| warning: false
#| code-fold: true


"""
====================
Violing Chart demonstraing various mpl-visual-context features
====================

"""

# import numpy as np
import matplotlib.pyplot as plt
import mpl_visual_context.patheffects as pe
import seaborn

seaborn.set()

tips = seaborn.load_dataset("tips")

# We start from a simple seaborn violin plot
fig, axs = plt.subplots(2, 2, num=1, clear=True, figsize=(8, 6), layout="constrained")
for ax in axs.flat:
    seaborn.violinplot(x='day', y='tip', data=tips, ax=ax,
                       hue='day', palette="deep")

ax = axs[0, 0]
ax.annotate(
    "(a) Original violin plot",
    (0, 1),
    xytext=(5, -5),
    xycoords="axes fraction",
    va="top",
    ha="left",
    textcoords="offset points",  # size=20,
)

# (b) w/ Brighter fill color
ax = axs[0, 1]
# We select violin patches. It seems that collections created by violinplot are
# version dependent. So your mileage may vary.
colls = ax.collections[::]


ax.annotate(
    "(b) Make fill color lighter,\nand stroke with the (original) fill color",
    (0, 1),
    xytext=(5, -5),
    xycoords="axes fraction",
    va="top",
    ha="left",
    textcoords="offset points",  # size=20,
)

pe_list = [
    pe.HLSModify(l=0.8) | pe.FillOnly(),
    pe.StrokeColorFromFillColor() | pe.StrokeOnly(),
]

for x, coll in enumerate(colls):
    coll.set_path_effects(pe_list)

# (c) AlphaGradient
ax = axs[1, 0]
colls = ax.collections[::]

ax.annotate(
    "(c) Fill w/ alpha gradient",
    (0, 1),
    xytext=(5, -5),
    xycoords="axes fraction",
    va="top",
    ha="left",
    textcoords="offset points",  # size=20,
)

pe_list = [
    pe.AlphaGradient("0.8 > 0.2 > 0.8"),
    (pe.StrokeColorFromFillColor() | pe.StrokeOnly()),
]

for x, coll in enumerate(colls):
    coll.set_path_effects(pe_list)

# (4) w/ Light effect
ax = axs[1, 1]
colls = ax.collections[::]

ax.annotate(
    "(d) Light effect and shadow",
    (0, 1),
    xytext=(5, -5),
    xycoords="axes fraction",
    va="top",
    ha="left",
    textcoords="offset points",  # size=20,
)

import mpl_visual_context.image_effect as ie

pe_list = [
    # shadow
    pe.FillOnly()
    | pe.ImageEffect(
        ie.AlphaAxb((0.5, 0))
        | ie.Pad(10)
        | ie.Fill("k")
        | ie.Dilation(3)
        | ie.Gaussian(4)
        | ie.Offset(3, -3)
    ),
    # light effect
    pe.HLSModify(l=0.7)
    | pe.FillOnly()
    | pe.ImageEffect(ie.LightSource(erosion_size=5, gaussian_size=5)),
]

for x, coll in enumerate(colls):
    coll.set_path_effects(pe_list)



# %% [markdown]
# # We will start with a seaborn violinplot example.
#

# %% Starting point


import matplotlib.pyplot as plt
import seaborn

seaborn.set()

tips = seaborn.load_dataset("tips")

fig, ax = plt.subplots(num=1, clear=True, figsize=(4, 3), layout="constrained" )
seaborn.violinplot(x='day', y='tip', data=tips, ax=ax,
                   hue='day', palette="deep")

# %% [markdown]
# While there are other ways to change the fill-colors and edge-colors of the
# patches, in this example, we will use patheffect. There are pros and cons.
# The disadvantages would be that it will increase the runtime performance.
# Advantage would be that it will keep its original color.
#
#

# %% [markdown]
# # Simple patheffect with `mpl-visual-context`: change color
#
# Let's start with a simple example
#
# The default edge color is black, let's sync it to that of the facecolor. We
# will use `mpl-visual-context` module, which implements composable
# patheffects, i.e., it implements various patheffects that can do simple thins
# and the can be pipelined to make complex patheffects.
#

# %%


import mpl_visual_context.patheffects as pe

colls = ax.collections

pe_list = [
    pe.HLSModify(l=0.8) | pe.FillOnly()
]

for coll in colls:
    coll.set_path_effects(pe_list)



# %% [markdown]
# `HLSModify` change the color (both fillcolor and edgecolor) in the HLS space.
# It will set the lightness to 0.8, making the color brighter. And, `FillOnly`
# will fill the path without stroking. By pipelining two patheffects with `|`,
# we create a new pathe effect that fills the path with a lighter color.
#
# Note that we iterate over `ax.collections`, but ax.collections seem to have
# different artists based on the seaborn version. So, you may need to iterate
# over a subset of collections.

# %%
#| echo: false
#| warning: false
fig

# %% [markdown]
# `set_path_effects` takes a list of patheffects. And the same path is drawn
# with different patheffects in sequence. So, let's add another patheffect. The
# default edgecolor was black, and we will change the edgecolor to the original
# fillcolor. `StrokeColorFromFillColor` will set the edgecolor to that of
# fillcolor and `StrokeOnly` will simply stroke the path without filling.
#

# %%
pe_list = [
    pe.HLSModify(l=0.8) | pe.FillOnly(),
    pe.StrokeColorFromFillColor() | pe.StrokeOnly(),
]

for x, coll in enumerate(colls):
    coll.set_path_effects(pe_list)

# %%
#| echo: false
#| warning: false
fig

# %% [markdown]
# mpl-visual-context` contains various patheffects. Check out
# https://mpl-visual-context.readthedocs.io/en/latest/api_path_effect.html for
# the list of available patheffects.

# %% [markdown]
# # Image-based patheffects
#
# `mpl-visual-context` also contains image-base patheffects. Note that these
# effects won't draw the path in vector format. Instead, it will rasterize the
# path and apply filters in image plane then the image is drawn on the canvas.
# Therefore, in most case, these image-base patheffect should be placed at the
# end of the pipeline.
#
# Let's apply some alpha gradient to the fill. `AlphaGradient` will make an
# image of the fill color and adjust the alpha channel of the images. For
# example, '0.8 > 0.2 > 0.8' means alpha horizontal gradient starting from 0.8
# on the left, 0.2 at the center and 0.8 at the right.
#

# %%

pe_list = [
    pe.AlphaGradient("0.8 > 0.4 > 0.8"),
    pe.StrokeColorFromFillColor() | pe.StrokeOnly(),
]

for x, coll in enumerate(colls):
    coll.set_path_effects(pe_list)

# %%
#| echo: false
#| warning: false
fig

# %% [markdown]
# You can also do vertical gradient. Instead of '>' use '^'. For example, '0.8 ^ 0' means alpha of 0.8 at the bottom and 0 at the top. Note that the image is created with extent of the artist.
#

# %%

pe_list = [
    pe.AlphaGradient("0.8 ^ 0"),
    pe.StrokeColorFromFillColor() | pe.StrokeOnly(),
]

for x, coll in enumerate(colls):
    coll.set_path_effects(pe_list)

# %%
#| echo: false
#| warning: false
fig

# %% [markdown]
# `AlphaGradient` is a special case of an `ImageEffect` patheffect. In fact,
# `ImageEffect` implements various effects in image plane that can be pipelined
# (similar to patheffects)
#

# %%
import mpl_visual_context.image_effect as ie

drop_shadow = pe.ImageEffect(
    ie.AlphaAxb((0.3, 0))
    | ie.Pad(10)
    | ie.Fill("k")
    | ie.Dilation(3)
    | ie.Gaussian(3)
    | ie.Offset(3, 3)
)

pe_list = [
    drop_shadow
]

for x, coll in enumerate(colls):
    coll.set_path_effects(pe_list)

# %%
#| echo: false
#| warning: false
fig

# %% [markdown]
# Together with the fill, it could be
#

# %%
pe_list = [
    drop_shadow,
    pe.FillOnly(),
]

for x, coll in enumerate(colls):
    coll.set_path_effects(pe_list)

# %%
#| echo: false
#| warning: false
fig

# %% [markdown]
# To make it more fancy, we can add light effect. It is based on `matplotlib.colors.LightSource`.
# https://matplotlib.org/stable/api/_as_gen/matplotlib.colors.LightSource.html
#

# %%
lighteffect = (pe.HLSModify(l=0.7)
               | pe.FillOnly()
               | pe.ImageEffect(ie.LightSource(erosion_size=5, gaussian_size=5))
               )

pe_list = [
    lighteffect
]

for x, coll in enumerate(colls):
    coll.set_path_effects(pe_list)

# %%
#| echo: false
#| warning: false
fig

# %% [markdown]
# Combining lighteffect with dropshadow,

# %%
pe_list = [
    drop_shadow,
    lighteffect
]

for x, coll in enumerate(colls):
    coll.set_path_effects(pe_list)

# plt.show()

# %%
#| echo: false
#| warning: false
fig

# %%
