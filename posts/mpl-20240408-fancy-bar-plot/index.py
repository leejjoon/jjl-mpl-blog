# ---
# title: "Introducing mpl-pe-fancy-bar"
# author: "Jae-Joon Lee"
# date: "05/31/2024"
# draft: false
# date-modified: "05/31/2024"
# categories:
#   - tutorial
#   - mpl-pe-fancy-bar
#   - mpl-visual-context
# ---

# %% [markdown]
# # mpl-pe-fancy-bar
#
# `mpl-pe-fancy-bar` is a module that includes patheffect classes that can be applied to bar plots created by Matplotlib which will transform the rectangles to other shapes.
#
# The source code is available at [github](https://github.com/leejjoon/mpl-pe-fancy-bar) and it is pip installable.
#
# > pip install mpl-pe-fancy-bar
#
# This was originally meant to be used with a collection of path from SVG, e.g., [this example](https://mpl-pe-fancy-bar.readthedocs.io/en/latest/examples/demo_ribbonbox.html#sphx-glr-examples-demo-ribbonbox-py).
#
# This tutorial won't cover usage of SVGs. It will focus on simpler bars focusing on the usage of the module. The example below show the bars you can create with this module, and the rest of the post will provide a tutorial.

# %%
#| warning: false
#| code-fold: true

import numpy as np
import matplotlib.pyplot as plt

# Fixing random state for reproducibility
np.random.seed(19680)

# Example data
n = 4
x_pos = np.arange(n)
performance = 5 * np.random.rand(n)
colors = [f"C{i}" for i in range(n)]

from matplotlib.path import Path
import mpl_visual_context.patheffects as pe
from mpl_pe_fancy_bar import BarToArrow, BarToRoundBar
from mpl_pe_fancy_bar.bar_with_icon import Icon, BarWithIcon

fig, axs = plt.subplots(2, 2, num=2, clear=True)

pe0 = []

pe1 = [(pe.RoundCorner(10, i_selector=lambda i: i in [2, 3])
        | pe.AlphaGradient("0.2 ^ 1."))]

pe2 = [BarToArrow() | pe.AlphaGradient("0.2 ^ 1.")]

circle = Path.unit_circle()
icon_circle = Icon((-1, -1, 2, 2), circle)
bar_with_circle = BarWithIcon(icon_circle, scale=0.6, dh=0.5)

pe3 = [
    BarToRoundBar() | pe.AlphaGradient("0.2 ^ 1."),
    bar_with_circle | pe.FillColor("w"),
]

for ax, patheffects in zip(axs.flat, [pe0, pe1, pe2, pe3]):
    bars = ax.bar(x_pos, performance, align='center', alpha=0.7, color=colors)

    for p in bars:
        p.set_path_effects(patheffects)


# %% [markdown]
# # MPL's own bar plot
#
# We will set the stage with a simple bar plot.

# %%
#| output: false
import numpy as np
import matplotlib.pyplot as plt

# Fixing random state for reproducibility
np.random.seed(19680)

# Example data
n = 4
x_pos = np.arange(n)
performance = 5 * np.random.rand(n)
colors = [f"C{i}" for i in range(n)]

fig, ax = plt.subplots(1, 1, num=1, clear=True, figsize=(4, 3))

bars = ax.bar(x_pos, performance, align='center', color=colors)

# %%
#| echo: false
#| warning: false
fig

# %% [markdown]
# The idea of `mpl-pe-fancy-bar` is to use patheffects to transform the simple rectangle path, created by matplotlib, to another path. The idea is similar to `FancyBox` and `FancyArrow` in matplotlib.
#
# We will start with `mpl_visual_context` module (which is required by `mpl-pe-fancy-arrow`). `mpl_visual_context` already contains some patheffects that you can use, and the patheffects of `mpl-pe-fancy-bar` are compatible with patheffects of `mpl_visual_context`. For example, `mpl_visual_context.patheffects.RoundCorner` can be applied to the rectangle path of the bar chart (`RoundCorner` itself can be applied to any path as far as they are not bezier spline).

# %%
#| output: false
import mpl_visual_context.patheffects as pe

patheffects = [
    (pe.RoundCorner(10, i_selector=lambda i: i in [2, 3]) # 2nd, and 3rd corners will be rounded.
     | pe.AlphaGradient("0.2 ^ 0.8")) # the path will be filled with gradient image whose alpha is 0.2
                                     # at the bottom and 1 at the top.
]
for p in bars:
    p.set_path_effects(patheffects)

# %%
#| echo: false
#| warning: false
fig

# %% [markdown]
# # mpl-pe-fancy-bar
#
# `mpl-pe-fancy-bar` module includes simple patheffects (mostly for demonstration purpose). 
#
#

# %%
#| output: false
from mpl_pe_fancy_bar import BarToRoundBar

patheffects = [BarToRoundBar() | pe.AlphaGradient("0.2 ^ 0.8")]
for p in bars:
    p.set_path_effects(patheffects)

# %%
#| echo: false
#| warning: false
fig

# %%
#| output: false
from mpl_pe_fancy_bar import BarToArrow

patheffects = [BarToArrow() | pe.AlphaGradient("0.2 ^ 0.8")]
for p in bars:
    p.set_path_effects(patheffects)

# %%
#| echo: false
#| warning: false
fig

# %% [markdown]
# # Making Custom Shape
#
# The included shapes are very limited. You are recommended to creat your own shape.
# We provide a `BarTransformBase` class. The key method is `_get_surface` which will take a single argument of bar height. The width of the bar is assumed to be 1 and the scaling will be taken care of automatically.
#
# The example below will draw a circle near the top of the rectangle.

# %%
#| output: false
from mpl_pe_fancy_bar import BarTransformBase, BarToRoundBar
from matplotlib.path import Path

class CustomBar(BarTransformBase):
    def __init__(self, radius=0.3,
                 orientation="vertical"):
        super().__init__(orientation=orientation)
        self._radius = radius

    def _get_surface(self, h):
        circle = Path.circle(center=(0., h-0.5), radius=0.3)
        return circle

patheffects = [
    BarToRoundBar() | pe.AlphaGradient("0.2 ^ 0.8"),
    CustomBar() | pe.FillColor("w"),
]
for p in bars:
    p.set_path_effects(patheffects)

# %%
#| echo: false
#| warning: false
fig

# %% [markdown]
# # Adding Icon
#
# Annotating a bar plot with an icon (simple path in this case) seems to be a frequent pattern, so `mpl-pe-fancy-bar` has its own support for adding an icon (its size will be proportional to the bar width).

# %%
#| output: false
from mpl_pe_fancy_bar.bar_with_icon import Icon, BarWithIcon

circle = Path.unit_circle()
icon_circle = Icon((-1, -1, 2, 2), circle) # the extent of the circle has 
                                           # lower-left boundary of (-1, -1)
                                           # and size of (2, 2)
bar_with_circle = BarWithIcon(icon_circle, scale=0.6, dh=0.5)

patheffects = [
    BarToRoundBar() | pe.AlphaGradient("0.2 ^ 0.8"),
    bar_with_circle | pe.FillColor("w"),
]
for p in bars:
    p.set_path_effects(patheffects)

# %%
#| echo: false
#| warning: false
fig

# %% [markdown]
# Horizontal bars are also supported, but you need to specify the orientation explictly when creating the patheffetcs.

# %%
#| output: false

fig, ax = plt.subplots(1, 1, num=2, clear=True, figsize=(4, 3))

y_pos = x_pos
bars = ax.barh(y_pos, performance, align='center', color=colors)

orientation= "horizontal"

bar_with_circle = BarWithIcon(icon_circle, scale=0.6, dh=0.5, orientation=orientation)

patheffects = [
    BarToRoundBar(orientation=orientation) | pe.AlphaGradient("0.2 > 0.8"),
    bar_with_circle | pe.FillColor("w"),
]
for p in bars:
    p.set_path_effects(patheffects)

# %%
#| echo: false
#| warning: false
fig

# %%
