# ---
# title: "Alphabet frequency plot"
# author: "Jae-Joon Lee"
# date: "03/25/2024"
# draft: false
# date-modified: "03/25/2024"
# categories:
#   - tutorial
#   - mpl-poormans-3d
#   - mpl-visual-context
# ---
# %% [markdown]
# We will creat plot of alphabet frequency. We will use `mpl-poormans-3d` package. The package can give your 2d plot some (but limited) 3d feel.

# %%
#| warning: false
#| code-fold: true

import numpy as np
from pathlib import Path
from matplotlib.font_manager import FontProperties

from matplotlib.colors import LightSource
from mpl_poormans_3d import BarToCharPrism
import mpl_visual_context.patheffects as pe
import mpl_visual_context.image_effect as ie

import matplotlib.pyplot as plt

from SecretColors import Palette

fig, axs = plt.subplots(2, 1, num=1, clear=True, figsize=(15, 8), layout="constrained")

# alphabet frequency data from wikipedia : https://en.wikipedia.org/wiki/Letter_frequency

abcd = [chr(ord("A") + i) for i in range(26)]  # A - Z
freq = [8.2, 1.5, 2.8, 4.3, 12.7, 2.2, 2.0, 6.1, 7.0, 0.15, 0.77, 4.0, 2.4, 6.7, 7.5, 1.9,
        0.095, 6.0, 6.3, 9.1, 2.8, 0.98, 2.4, 0.15, 2.0, 0.074]

ax = axs[0]

x = np.arange(len(abcd))
ax.bar(x, freq)
ax.set_xticks(x, abcd)
ax.set_ylim(-1.5, 15)
ax.set_ylabel("Frequency [%]")

ls = LightSource(azdeg=25+90)

fp = FontProperties("sans serif")

import seaborn as sns
cc = sns.color_palette("husl", 26)

rs = np.random.RandomState(8)
idx = rs.choice(len(cc), len(cc), replace=False)
cc = np.array(cc)[idx]

for p, fc, c in zip(ax.patches, cc, abcd):
    # p.set_fc(color)
    bar_to_prism = BarToCharPrism(ls, c,
                                  ratio=0.6,
                                  rotate_deg=10,
                                  fraction=0.5,
                                  scale=1.2,
                                  # fontprop=fp,
                                  distance_mode=np.mean)

    p.set_path_effects([#pe.FillOnly(),
        (bar_to_prism.get_pe_face(0)
         | pe.FillColor("k")
         | pe.ImageEffect(ie.Pad(20) | ie.Fill("k") | ie.GaussianBlur(5))),
        pe.FillColor(fc) | bar_to_prism,
        (bar_to_prism.get_pe_face(1)
         | pe.FillColor("w")
         ),
    ])

# from https://story.pxd.co.kr/958, w/o double consonant
hangul_consonant = "ㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊㅋㅌㅍㅎ"
hangul_freq = [11.3, 7.3, 8.0, 6.6, 5.6, 4.8, 9.1, 21.4, 8.3, 2.3, 1.6, 2.2, 1.5, 6.8]

ax = axs[1]

import mplfonts
from mplfonts.conf import FONT_DIR # , RC_DIR
from pathlib import Path
# fname = Path(FONT_DIR) / "NotoSansMonoCJKsc-Regular.otf"
fname = Path(FONT_DIR) / "NotoSerifCJKsc-Regular.otf"
# fname = Path(FONT_DIR) / "SourceHanSerifSC-Regular.otf"
fp = FontProperties(fname=fname)

x = np.arange(len(hangul_consonant))
ax.bar(x, hangul_freq)
ax.set_xticks(x, hangul_consonant, fontproperties=fp)
ax.set_ylim(-3, 25)
ax.set_ylabel("Frequency [%]")

ls = LightSource(azdeg=25+90)

import seaborn as sns

palette = Palette("material")
cnames = list(c for c in palette.colors.keys() if c not in ["black", "white"])
rs = np.random.RandomState(8)
cnames = rs.choice(cnames, len(cnames), replace=False)

for p, cn, c in zip(ax.patches, cnames, hangul_consonant):
    cc = [palette.get(cn, shade=shade) for shade in np.linspace(20, 90, 50)]
    segment_params = (ax, 25, cc, None)

    bar_to_prism = BarToCharPrism(ls, c,
                                  ratio=0.6,
                                  rotate_deg=10,
                                  fraction=0.5,
                                  scale=1.2,
                                  fontprop=fp,
                                  segment_params=segment_params,
                                  distance_mode=np.mean)

    p.set_path_effects([#pe.FillOnly(),
        (bar_to_prism.get_pe_face(0)
         | pe.FillColor("k")
         | pe.ImageEffect(ie.Pad(20) | ie.Fill("k") | ie.GaussianBlur(10))),
        pe.FillColor(fc) | bar_to_prism,
        (bar_to_prism.get_pe_face(1)
         | pe.FillColor("w")
         ),
    ])

plt.show()



# %% [markdown]
# `mpl-poormans-3d` is available at [github](https://github.com/leejjoon/mpl-poormans-3d). It can be installed via
#
# ```sh
# pip install mpl-poormans-3d
# ```

# %% [markdown]
# We will start with a data.

# %%
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
# alphabet frequency data from wikipedia : https://en.wikipedia.org/wiki/Letter_frequency

abcd = [chr(ord("A") + i) for i in range(26)]  # A - Z
freq = [8.2, 1.5, 2.8, 4.3, 12.7, 2.2, 2.0, 6.1, 7.0, 0.15, 0.77, 4.0, 2.4, 6.7, 7.5, 1.9,
        0.095, 6.0, 6.3, 9.1, 2.8, 0.98, 2.4, 0.15, 2.0, 0.074]

# %% [markdown]
# For the clairty, we will create a sample plot focusing on the first 4 bars. We adjusted y-range also to have enough room for 3d effects.

# %%
#| output: false
fig, ax = plt.subplots(1, 1, num=1, clear=True, figsize=(4, 2.5), layout="constrained")

x = np.arange(len(abcd))
ax.bar(x, freq)
ax.set_xticks(x, abcd)
ax.set_ylabel("Frequency [%]")
ax.set_xlim(-0.6, 3.6)
ax.set_ylim(-1.5, 10)

# %%
#| echo: false
#| warning: false
fig

# %% [markdown]
#
# `mpl-poormasn-3d` provide a way to convert your bars to 3d. We will first try
# `BarToPrism` class. You create it by setting the lightsource and number of
# vertices of the shape. Its instance is callable object and can be used as a
# patheffect. The lightsource should be an instance of `matplotlib.colors.LightSource`.

# %%
from matplotlib.colors import LightSource
from mpl_poormans_3d import BarToPrism

lightsource = LightSource(azdeg=25+90)

p = ax.patches[0]

numVertices = 4
bar_to_prism = BarToPrism(lightsource, numVertices)

p.set_path_effects([bar_to_prism])


# %%
#| echo: false
#| warning: false
fig

# %% [markdown]
#
# `BarToPrism` takes several keyword arguments. `ratio` is for aspect ratio,
# i.e., smaller ratio will give you flat shape. The meaning of `scale` and
# `rotate_deg` should be self-explanatory.

# %%
p = ax.patches[1]

numVertices = 8
bar_to_prism = BarToPrism(lightsource, numVertices, ratio=0.2, scale=0.8, rotate_deg=30)

p.set_path_effects([bar_to_prism])

# %%
#| echo: false
#| warning: false
fig

# %% [markdown]
#
# BarToCylinder will creat a cylinder.

# %%
from mpl_poormans_3d import BarToCylinder
p = ax.patches[2]

bar_to_prism = BarToCylinder(lightsource, ratio=0.4)

p.set_path_effects([bar_to_prism])

# %%
#| echo: false
#| warning: false
fig

# %% [markdown]
#
# `BarToCharPrism` will creat a 3d-bar using the character path and
# `BarToPathPrism` will do the same using an arbitrary path.

# %%
from mpl_poormans_3d import BarToCharPrism
p = ax.patches[3]

bar_to_prism = BarToCharPrism(lightsource, "d")

p.set_path_effects([bar_to_prism])

# %%
#| echo: false
#| warning: false
fig

# %% [markdown]
#
# The instance of `BarToPrism` and its siblings have a `get_pe_face` method
# which returns a patheffect that only show the face of the prism at a given
# position. 0 means bottom, 1 means top. Note that an instance of `BarToPrism`
# renders multiple paths and cannot be combined with other patheffects. On the
# other hand, return value of `get_pe_face` method can be combine with other
# patheffects, e.g., patheffects from `mpl-visual-context`.

# %%
import mpl_visual_context.patheffects as pe

bar_to_prism = BarToCharPrism(lightsource, "d")

p.set_path_effects([
    bar_to_prism,
    bar_to_prism.get_pe_face(1) | pe.FillColor("w") | pe.StrokeColor("r")
])

# %%
#| echo: false
#| warning: false
fig

# %% [markdown]
#
# We can further add a simple shadow to the bar.

# %%
import mpl_visual_context.image_effect as ie

blur_effect = pe.ImageEffect(ie.Pad(20) | ie.Fill("k") | ie.GaussianBlur(5))

p.set_path_effects([
    bar_to_prism.get_pe_face(0) | pe.FillColor("k") | blur_effect,
    bar_to_prism,
    bar_to_prism.get_pe_face(1) | pe.FillColor("w") | pe.StrokeColor("r")
])


# %%
#| echo: false
#| warning: false
fig

# %% [markdown]
#
# Now, let's create a plot of full character set and show alphabet frequency. We will set the
# facolor of bars using the te `husl` color palette.

# %%
#| output: false

fig, ax = plt.subplots(1, 1, num=2, clear=True, figsize=(12, 4), layout="constrained")

x = np.arange(len(abcd))
ax.bar(x, freq)
ax.set_xticks(x, abcd)
ax.set_ylabel("Frequency [%]")

import seaborn as sns
cc = sns.color_palette("husl", 26)

rs = np.random.RandomState(8)
idx = rs.choice(len(cc), len(cc), replace=False)
cc = np.array(cc)[idx]

for p, fc in zip(ax.patches, cc):
    p.set_fc(fc)

ax.set_ylim(-1.5, 15)


# %%
#| echo: false
#| warning: false
fig

# %% [markdown]
#
# We will use `BarToCharPrism` to represent the alphabet. We will add some
# shadow and make the top face white.

# %%
lightsource = LightSource(azdeg=25+90)
blur_effect = pe.ImageEffect(ie.Pad(10) | ie.Fill("k") | ie.GaussianBlur(3))

for p, fc, c in zip(ax.patches, cc, abcd):
    bar_to_prism = BarToCharPrism(lightsource, c,
                                  ratio=0.6,
                                  rotate_deg=10,
                                  fraction=0.5,
                                  scale=1.2,
                                  distance_mode=np.mean)

    p.set_path_effects([#pe.FillOnly(),
        (bar_to_prism.get_pe_face(0) | pe.FillColor("k") | blur_effect),
        bar_to_prism,
        (bar_to_prism.get_pe_face(1) | pe.FillColor("w"))
    ])

# %%
#| echo: false
#| warning: false
fig

# %% [markdown]
#
# We will create another plot, showing frequncy of Hangul characters (Korean
# characters) We need specify a font with Korean characters. For the example,
# we will us korean fonts included in the `mplfoints` package, but any Korean
# font should work.
#
# from https://story.pxd.co.kr/958, w/o double consonant

# %%
#| output: false
hangul_consonant = "ㄱㄴㄷㄹㅁㅂㅅㅇㅈㅊㅋㅌㅍㅎ"
hangul_freq = [11.3, 7.3, 8.0, 6.6, 5.6, 4.8, 9.1, 21.4, 8.3, 2.3, 1.6, 2.2, 1.5, 6.8]

fig, ax = plt.subplots(1, 1, num=3, clear=True, figsize=(12, 4), layout="constrained")

from mplfonts.conf import FONT_DIR
from pathlib import Path
from matplotlib.font_manager import FontProperties

fname = Path(FONT_DIR) / "NotoSerifCJKsc-Regular.otf"
fp = FontProperties(fname=fname)

x = np.arange(len(hangul_consonant))
ax.bar(x, hangul_freq)
ax.set_xticks(x, hangul_consonant, fontproperties=fp)
ax.set_ylim(-3, 25)
ax.set_ylabel("Frequency [%]")

# %%
#| echo: false
#| warning: false
fig

# %% [markdown]
#
# We want the prism to have varuing shades. For that, we will use `material`
# palette. We will pick up the palette from the `SecretColors` package althoug
# the original palette is from google's matrial design.
#
# `Prism` instances can be created using the semenet_params.

# %%
from SecretColors import Palette
import seaborn as sns

lightsource = LightSource(azdeg=25+90)

palette = Palette("material")
cnames = list(c for c in palette.colors.keys() if c not in ["black", "white"])
rs = np.random.RandomState(8)
cnames = rs.choice(cnames, len(cnames), replace=False)

blur_effect = pe.ImageEffect(ie.Pad(10) | ie.Fill("k") | ie.GaussianBlur(3))

for p, cn, c in zip(ax.patches, cnames, hangul_consonant):
    cc = [palette.get(cn, shade=shade) for shade in np.linspace(20, 90, 50)]
    segment_params = (ax, 25, cc, None)

    bar_to_prism = BarToCharPrism(lightsource, c,
                                  ratio=0.6,
                                  rotate_deg=10,
                                  fraction=0.5,
                                  scale=1.4,
                                  fontprop=fp,
                                  segment_params=segment_params,
                                  )

    p.set_path_effects([
        bar_to_prism.get_pe_face(0) | pe.FillColor("k") | blur_effect,
        bar_to_prism,
        bar_to_prism.get_pe_face(1) | pe.FillColor("w"),
    ])


# %%
#| echo: false
#| warning: false
fig

# %%
