# ---
# title: "Car crash plot w/ mpl-pe-fancy-bar"
# author: "Jae-Joon Lee"
# date: "03/28/2024"
# draft: false
# date-modified: "03/28/2024"
# categories:
#   - tutorial
#   - mpl-pe-fancy-bar
#   - mpl-visual-context
# ---

# %%
#| warning: false
#| code-fold: true

import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_theme(style="whitegrid")

# Load the example car crash dataset
crashes = sns.load_dataset("car_crashes").sort_values("total", ascending=False).iloc[:10]

# Initialize the matplotlib figure
fig, ax = plt.subplots(num=1, clear=True, figsize=(5, 4))
# fig, ax = plt.subplots(num=1, clear=True, layout="constrained")

# Plot the total crashes
sns.set_color_codes("pastel")
sns.barplot(x="total", y="abbrev", data=crashes,
            label="Total", color="b")

# Plot the crashes where alcohol was involved
sns.set_color_codes("muted")
sns.barplot(x="alcohol", y="abbrev", data=crashes,
            label="Alcohol-involved", color="b")

# Add a legend and informative axis label
ax.legend(ncol=2, loc="lower right", frameon=True,
          bbox_to_anchor=[1, 1])

ax.set(xlim=(0, 24.8),
       ylim=(9.6, -0.6),
       ylabel="",
       xlabel="Automobile collisions per billion miles")

sns.despine(left=True, bottom=True)

import mpl_visual_context.patheffects as pe
from mpl_pe_fancy_bar import BarToRoundBar
from mpl_visual_context.patheffects_shadow import ShadowPath

round_bar = BarToRoundBar(orientation="horizontal", dh=0.5)
shadow = ShadowPath(115, 3)

from svgpath2mpl import parse_path

# car icon from https://fontawesome.com/icons/car?f=classic&s=solid
# 512 x 512
s="M135.2 117.4L109.1 192H402.9l-26.1-74.6C372.3 104.6 360.2 96 346.6 96H165.4c-13.6 0-25.7 8.6-30.2 21.4zM39.6 196.8L74.8 96.3C88.3 57.8 124.6 32 165.4 32H346.6c40.8 0 77.1 25.8 90.6 64.3l35.2 100.5c23.2 9.6 39.6 32.5 39.6 59.2V400v48c0 17.7-14.3 32-32 32H448c-17.7 0-32-14.3-32-32V400H96v48c0 17.7-14.3 32-32 32H32c-17.7 0-32-14.3-32-32V400 256c0-26.7 16.4-49.6 39.6-59.2zM128 288a32 32 0 1 0 -64 0 32 32 0 1 0 64 0zm288 32a32 32 0 1 0 0-64 32 32 0 1 0 0 64z"

icon = parse_path(s)

from mpl_pe_fancy_bar.bar_with_icon import Icon, BarWithIcon

ii = Icon((512, 512), icon)
with_icon = BarWithIcon(ii, orientation="horizontal", scale=0.5, dh=0.6)

pe1 = [
    round_bar,
    round_bar | pe.ClipPathSelf() | shadow | pe.HLSModify(l="60%"),
    with_icon | shadow | pe.HLSModify(l="40%"),
    with_icon | pe.FillColor("w")
]
for p in ax.containers[0]:
    p.set_path_effects(pe1)

pe1 = [
    round_bar | pe.FillOnly(),
    with_icon | pe.FillColor("w")
]
for p in ax.containers[1]:
    p.set_path_effects(pe1)

from mpl_visual_context.axes_panel import InsetDivider, add_panel
from mpl_visual_context.legend_helper import (
    extract_offset_boxes_from_legend,
)
from matplotlib.offsetbox import HPacker
from matplotlib.offsetbox import AnchoredOffsetbox

divider = InsetDivider(ax)

panel = add_panel(divider, "left", "ticklabels", pad=0.0)
legend_panel = add_panel(divider, "top", "empty", pad=0.0)

leg_title, oblist = extract_offset_boxes_from_legend(ax.legend_)

pack = HPacker(pad=0.0, sep=10, children=oblist)
box = AnchoredOffsetbox("upper center", child=pack, pad=0, frameon=False)
ax.legend_.remove()

legend_panel.add_artist(box)
legend_panel.add_to_extent_list(box)
legend_panel.grid(False)

panel.set_axis_off()

fc = "gold"
fig.patch.set_fc(fc)
ax.patch.set_visible(False) # fc(fc)


# %% [markdown]
# We start with a seaborn plot

# %%
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
sns.set_theme(style="whitegrid")

# Load the example car crash dataset
crashes = sns.load_dataset("car_crashes").sort_values("total", ascending=False).iloc[:10]

# Initialize the matplotlib figure
fig, ax = plt.subplots(num=1, clear=True, figsize=(5, 4))
# fig, ax = plt.subplots(num=1, clear=True, layout="constrained")

# Plot the total crashes
sns.set_color_codes("pastel")
sns.barplot(x="total", y="abbrev", data=crashes,
            label="Total", color="b")

# Plot the crashes where alcohol was involved
sns.set_color_codes("muted")
sns.barplot(x="alcohol", y="abbrev", data=crashes,
            label="Alcohol-involved", color="b")

# Add a legend and informative axis label
ax.legend(ncol=2, loc="lower right", frameon=True,
          bbox_to_anchor=[1, 1])

ax.set(xlim=(0, 24.8),
       ylim=(9.6, -0.6),
       ylabel="",
       xlabel="Automobile collisions per billion miles")

sns.despine(left=True, bottom=True)

# %% [markdown]
# `mpl-pe-fancy-bar` module contains patheffects that transform a simple rectangle path to a more complicated one.
# Below, we will use `BarToRoundBar` that transform a rectable to a rounded one.

# %% round with some depth
#| output: false
import mpl_visual_context.patheffects as pe
from mpl_pe_fancy_bar import BarToRoundBar

round_bar = BarToRoundBar(orientation="horizontal", dh=0.5)
shadow = ShadowPath(115, 3)

pe1 = [
    round_bar,
]
for p in ax.containers[0]:
    p.set_path_effects(pe1)

pe2 = [
    round_bar | pe.FillOnly(),
]
for p in ax.containers[1]:
    p.set_path_effects(pe2)

# %%
#| echo: false
#| warning: false
fig

# %% [markdown]
# How about some shadow?

# %%
#| output: false
from mpl_visual_context.patheffects_shadow import ShadowPath

shadow = ShadowPath(115, 3)

pe1 = [
    round_bar,
    round_bar | pe.ClipPathSelf() | shadow | pe.HLSModify(l="60%"),
]
for p in ax.containers[0]:
    p.set_path_effects(pe1)

pe2 = [
    round_bar | pe.FillOnly(),
]
for p in ax.containers[1]:
    p.set_path_effects(pe2)

# %%
#| echo: false
#| warning: false
fig

# %% [markdown]
# Let's add car icons to the bars. There could be different ways. We use `BarWithIcon` class. The advantage of this is that the size of icon will automatically scale relative to the width of the bars.

# %% Add icon
#| output: false
from svgpath2mpl import parse_path

# car icon from https://fontawesome.com/icons/car?f=classic&s=solid
# 512 x 512
s="M135.2 117.4L109.1 192H402.9l-26.1-74.6C372.3 104.6 360.2 96 346.6 96H165.4c-13.6 0-25.7 8.6-30.2 21.4zM39.6 196.8L74.8 96.3C88.3 57.8 124.6 32 165.4 32H346.6c40.8 0 77.1 25.8 90.6 64.3l35.2 100.5c23.2 9.6 39.6 32.5 39.6 59.2V400v48c0 17.7-14.3 32-32 32H448c-17.7 0-32-14.3-32-32V400H96v48c0 17.7-14.3 32-32 32H32c-17.7 0-32-14.3-32-32V400 256c0-26.7 16.4-49.6 39.6-59.2zM128 288a32 32 0 1 0 -64 0 32 32 0 1 0 64 0zm288 32a32 32 0 1 0 0-64 32 32 0 1 0 0 64z"

icon = parse_path(s)

from mpl_pe_fancy_bar.bar_with_icon import Icon, BarWithIcon

ii = Icon((512, 512), icon)
with_icon = BarWithIcon(ii, orientation="horizontal", scale=0.5, dh=0.6)

pe1 = [
    round_bar,
    round_bar | pe.ClipPathSelf() | shadow | pe.HLSModify(l="60%"),
    with_icon | shadow | pe.HLSModify(l="40%"),
    with_icon | pe.FillColor("w")
]
for p in ax.containers[0]:
    p.set_path_effects(pe1)

pe1 = [
    round_bar | pe.FillOnly(),
    with_icon | pe.FillColor("w")
]
for p in ax.containers[1]:
    p.set_path_effects(pe1)

# %%
#| echo: false
#| warning: false
fig

# %% [markdown]
# Let's change the background color and other aspect of the plot. This uses `panel` feature of `mpl_visual_context`, which we won't address its detail. In short, `panel` is an axes that is located next to the main axes, which is meant to display ticks and labels as annotations for more flexibility.

# %%
#| output: false

from mpl_visual_context.axes_panel import InsetDivider, add_panel
from mpl_visual_context.legend_helper import (
    extract_offset_boxes_from_legend,
)
from matplotlib.offsetbox import HPacker
from matplotlib.offsetbox import AnchoredOffsetbox

divider = InsetDivider(ax)

panel = add_panel(divider, "left", "ticklabels", pad=0.0)
legend_panel = add_panel(divider, "top", "empty", pad=0.0)

leg_title, oblist = extract_offset_boxes_from_legend(ax.legend_)

pack = HPacker(pad=0.0, sep=10, children=oblist)
box = AnchoredOffsetbox("upper center", child=pack, pad=0, frameon=False)
ax.legend_.remove()

legend_panel.add_artist(box)
legend_panel.add_to_extent_list(box)
legend_panel.grid(False)

panel.set_axis_off()

fc = "gold"
fig.patch.set_fc(fc)
ax.patch.set_visible(False) # fc(fc)

# %%
#| echo: false
#| warning: false
fig

# %%
