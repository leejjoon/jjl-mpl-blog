# ---
# title: "Matplotlib logo in Cyberpunk style"
# author: "Jae-Joon Lee"
# date: "02/16/2025"
# draft: false
# date-modified: "02/16/2025"
# categories:
#   - showcase
#   - mpl-skia-pathops
#   - mpl-visual-context
# ---

# %% [markdown]
# # Matplotlib logo in Cyberpunk style
#
# In this post, we will recreate the matplotlib logo in Cyberpunk style.
#

# %%
#| warning: false
#| code-fold: true

import matplotlib.pyplot as plt
from matplotlib_logo import make_logo

import mplcyberpunk
from mpl_skia_pathops import PathOpsPathEffect

import mpl_visual_context.patheffects as pe
import mpl_visual_context.image_box as ib
import mpl_visual_context.image_effect as ie

linewidth_scale = 1.5

with plt.rc_context():
    plt.style.use("cyberpunk")
    fig, ax = make_logo(height_px=int(110 * linewidth_scale),
                        lw_bars=0.7*linewidth_scale, lw_grid=0.5*linewidth_scale,
                        lw_border=1*linewidth_scale,
                        rgrid=[1, 3, 5, 7], with_text=True)

    cmap = plt.get_cmap()  # we canche the default cmap of the cyberpunk theme.

fig.patch.set(alpha=1) # The figure patch was set to transparent.
ax.patch.set_alpha(0.3)

tp = fig.axes[0].patches[0]  # The textpath
tp.set_clip_on(False)

# make_logo add a circle (rectangle in polar coordinate) patch, that is larger than
# the axes patch (which is a circle). We will use this circle patch to clip the text.

circle = sorted(ax.patches, key=lambda a: a.get_zorder())[0]
circle.set_visible(False)

union_circle = PathOpsPathEffect.union(circle)
# a path effect that unions the given path with the cricle.

tp.set_path_effects([union_circle])

# glow effect
glow = pe.ImageEffect(ie.Pad(20*linewidth_scale)
                      | ie.GaussianBlur(10, channel_slice=slice(3, 4))
                      | ie.AlphaAxb((2, 0))
                      | ie.Erosion(50*linewidth_scale, channel_slice=slice(0, 3))
                      )

# We will create an imagebox with the colormap of the cyberpunk theme. We need
# to increase the extent so that the image is large enough when we stroke it.
color_gradient_box = ib.ImageBox("right", extent=[-0.1, -0.1, 1.1, 1.1],
                                 coords=tp, axes=ax, cmap=cmap)

stroke_color_gradient = (
    union_circle
    | pe.GCModify(linewidth=3*linewidth_scale, alpha=1)
    | PathOpsPathEffect.stroke2fill()
    | pe.FillImage(color_gradient_box)
)

tp.set_path_effects([
    stroke_color_gradient | glow,
    union_circle | pe.FillImage(color_gradient_box, alpha=0.5),
    stroke_color_gradient
])


# %% [markdown]
# ## Matplotlib logo 
#
# We start with a matplotlib logo. This is adopted from https://matplotlib.org/stable/gallery/misc/logos2.html.
#

# %%
#| output: false
import matplotlib.pyplot as plt
from matplotlib_logo import make_logo

fig, ax = make_logo(height_px=int(110),
                    lw_bars=0.7, lw_grid=0.5,
                    lw_border=1,
                    rgrid=[1, 3, 5, 7], with_text=True)

# %%
#| echo: false
#| warning: false
fig

# %% [markdown]
# ## Cybepunk Style
#
# We will redraw the logo in cybepunk style (using the [cyberpunk package](https://github.com/dhaitz/mplcyberpunk)).
# We will also tweak some aspect of the result.

# %%
#| output: falseimport mplcyberpunk

linewidth_scale = 1.5

with plt.rc_context():
    plt.style.use("cyberpunk")
    fig, ax = make_logo(height_px=int(110 * linewidth_scale),
                        lw_bars=0.7*linewidth_scale, lw_grid=0.5*linewidth_scale,
                        lw_border=1*linewidth_scale,
                        rgrid=[1, 3, 5, 7], with_text=True)

    cmap = plt.get_cmap()  # we canche the default cmap of the cyberpunk theme.

fig.patch.set(alpha=1) # The figure patch was set to transparent.
ax.patch.set_alpha(0.3)

tp = fig.axes[0].patches[0]  # The textpath
tp.set_clip_on(False)

# make_logo add a circle (rectangle in polar coordinate) patch, that is larger than
# the axes patch (which is a circle). We will use this circle patch to clip the text.

circle = sorted(ax.patches, key=lambda a: a.get_zorder())[0]
circle.set_visible(False)


# %%
#| echo: false
#| warning: false
fig

# %% [markdown]
# ## Patheffect to draw the union of two paths
#
# We'd like to merge the text path and the background circular path of the icon.
# We use [mpl_skia_pathops](https://github.com/leejjoon/mpl-skia-pathops). This example is based on 0.3.0 version.
# .

# %%
#| output: false
from mpl_skia_pathops import PathOpsPathEffect

union_circle = PathOpsPathEffect.union(circle)
# a path effect that unions the given path with the cricle.

tp.set_path_effects([union_circle])


# %%
#| echo: false
#| warning: false
fig

# %% [markdown]
# ## Matplotlib logo in Cyberpunk style
#
# We will make it more cyberpunk. The effect is adopted from [cyberpunk example](https://mpl-visual-context.readthedocs.io/en/latest/examples/30-showcase-cyberpunk.html#sphx-glr-examples-30-showcase-cyberpunk-py)
# in the [mpl-visual-context](https://github.com/leejjoon/mpl-visual-context) package.

# %%
#| output: false

import mpl_visual_context.patheffects as pe
import mpl_visual_context.image_box as ib
import mpl_visual_context.image_effect as ie

# glow effect
glow = pe.ImageEffect(ie.Pad(20*linewidth_scale)
                      | ie.GaussianBlur(10, channel_slice=slice(3, 4))
                      | ie.AlphaAxb((2, 0))
                      | ie.Erosion(50*linewidth_scale, channel_slice=slice(0, 3))
                      )

# We will create an imagebox with the colormap of the cyberpunk theme. We need
# to increase the extent so that the image is large enough when we stroke it.
color_gradient_box = ib.ImageBox("right", extent=[-0.1, -0.1, 1.1, 1.1],
                                 coords=tp, axes=ax, cmap=cmap)

stroke_color_gradient = (
    union_circle
    | pe.GCModify(linewidth=3*linewidth_scale, alpha=1)
    | PathOpsPathEffect.stroke2fill()
    | pe.FillImage(color_gradient_box)
)

tp.set_path_effects([
    stroke_color_gradient | glow,
    union_circle | pe.FillImage(color_gradient_box, alpha=0.5),
    stroke_color_gradient
])


# %%
#| echo: false
#| warning: false
fig

# %%
