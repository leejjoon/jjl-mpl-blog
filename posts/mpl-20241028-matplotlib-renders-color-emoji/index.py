# ---
# title: "Rendering ColorEmoji with Matplotlib"
# author: "Jae-Joon Lee"
# date: "10/28/2024"
# draft: false
# date-modified: "10/28/2024"
#
# ---

# %% [markdown]
# # Using ColorEmoji in Matplotlib
#
# In previous post, we introduced [mpl-simple-svg-parser](https://github.com/leejjoon/mpl-simple-svg-parser) package that lets you render svg. You can further use this to render color emoji.
#
# You will need a color emoji font with COLR table. For example, Noto Color Emoji can be downaloaded from https://fonts.google.com/noto/specimen/Noto+Color+Emoji
#
# You can transform the glyphs in the font to SVG, and uses mpl-simple-svg-parser, for example, to render it with matplotlib.
#
# [mpl-colr2svg](https://github.com/leejjoon/mpl-colr2svg) is a package that does this.
# To convert emoji to svg, it uses [nanoemoji](https://github.com/googlefonts/nanoemoji).
# Altenatively, it can use [blackrenderer](https://github.com/BlackFoundryCom/black-renderer)
# to render emoji font to svg.

# %%
#| warning: false
#| code-fold: true

import matplotlib.pyplot as plt
import pandas as pd

emoji_popularity = [["😂", 223.94],
                    ["🤣", 170.29],
                    ["❤️", 95.02],
                    ["🙏", 116.92],
                    ["😭", 95.02],
                    ["😍", 77.3],
                    ["✨", 76.34],
                    ["🔥", 71.52],
                    ["😊", 70.15],
                    ["🥰", 67.35],
                    ]

df = pd.DataFrame(emoji_popularity, columns=["Emoji", "Popularity"])

import seaborn as sns
sns.set_color_codes("muted")
sns.set(font_scale = 1.5)

fig, ax = plt.subplots(1, 1, figsize=(7, 4), clear=True, num=2, layout="constrained")

sns.barplot(x="Emoji", y="Popularity", data=df,
            label="Emoji Popularity", color="b")

from mpl_colr2svg import ColorEmoji

ftname = "NotoColorEmoji-Regular.ttf"
fontsize = 25

emoji = ColorEmoji(ftname)

for l in ax.get_xticklabels():
    c = l.get_text()
    xy = l.get_position()

    l.set_visible(False)

    emoji.annotate(ax, c, xy, xycoords=("data", "axes fraction"),
                   box_alignment=(0.5, 1), fontsize=fontsize,
                   annotation_clip=True)

ax.xaxis.labelpad = fontsize * 1.7

plt.show()


# %% [markdown]
# Let's start with a simple example. 
#

# %%
import matplotlib.pyplot as plt
from mpl_colr2svg import ColorEmoji


ftname = "NotoColorEmoji-Regular.ttf"
emoji = ColorEmoji(ftname)
c = "🤩"

fig, axs = plt.subplots(1, 2, figsize=(10, 5), clear=True, num=1)
ax1 = axs[0]
ax1.set_title("draw in data coordinate")

emoji.draw(ax1, c, size=128)

ax2 = axs[1]

emoji.annotate(ax2, c, (0.5, 0.5), fontsize=128)
ax2.set_title("drawing_area with annotate")

plt.show()

# %% [markdown]
# You may use blackrender. The default `ColorEmoji` only support a sing glyph, but the blackrenderer version supports string of multiple charaters.

# %%

import matplotlib.pyplot as plt
from mpl_colr2svg.color_emoji_blackrenderer import ColorEmojiBlackrenderer

ftname = "seguiemj.ttf"
emoji = ColorEmojiBlackrenderer(ftname)
textString = "L❤️VE"

fig, ax = plt.subplots(1, 1, clear=True, num=1)

emoji.annotate(ax, textString, (0.5, 0.5), fontsize=128)

plt.show()



# %% [markdown]
# Here is a more useful example. We start with a seabron plot of emoji popularity.

# %%
import matplotlib.pyplot as plt
import pandas as pd

emoji_popularity = [["😂", 223.94],
                    ["🤣", 170.29],
                    ["❤️", 95.02],
                    ["🙏", 116.92],
                    ["😭", 95.02],
                    ["😍", 77.3],
                    ["✨", 76.34],
                    ["🔥", 71.52],
                    ["😊", 70.15],
                    ["🥰", 67.35],
                    ]

df = pd.DataFrame(emoji_popularity, columns=["Emoji", "Popularity"])

import seaborn as sns
sns.set_color_codes("muted")
sns.set(font_scale = 1.5)

fig, ax = plt.subplots(1, 1, figsize=(7, 4), clear=True, num=2, layout="constrained")

sns.barplot(x="Emoji", y="Popularity", data=df,
            label="Emoji Popularity", color="b")

# %% [markdown]
# Don't worry if you see tofus. We will replace the x-tick labels with color emoji.

# %%
from mpl_colr2svg import ColorEmoji

ftname = "NotoColorEmoji-Regular.ttf"
fontsize = 25

emoji = ColorEmoji(ftname)

for l in ax.get_xticklabels():
    c = l.get_text()
    xy = l.get_position()

    l.set_visible(False)

    emoji.annotate(ax, c, xy, xycoords=("data", "axes fraction"),
                   box_alignment=(0.5, 1), fontsize=fontsize,
                   annotation_clip=True)

ax.xaxis.labelpad = fontsize * 1.7


# %%
#| echo: false
#| warning: false
fig

# %%
