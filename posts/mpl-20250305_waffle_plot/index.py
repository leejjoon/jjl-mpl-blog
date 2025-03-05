# %% We start with a waffle plot.

import matplotlib.pyplot as plt
from pywaffle import Waffle

fig, ax = plt.subplots(1, 1, num=1, clear=True)

ax.set_aspect(aspect="equal")

Waffle.make_waffle(
    ax=ax,  # pass axis to make_waffle
    rows=5,
    columns=10,
    values=[30, 16, 4],
    title={"label": "Waffle", "loc": "left"}
)

# %% make it more delicious?

from mpl_visual_context.patheffects import ImageEffect
from mpl_visual_context.image_effect import Pad, LightSourceSharp

pe_waffle1 = ImageEffect(Pad(10) | LightSourceSharp(dist_max=7, azdeg=215, altdeg=70,
                                                    fraction=0.97,
                                                    vert_exag=0.2,
                                                    ))

for p in ax.patches:
    p.set_path_effects([pe_waffle1])

# %% another try.

from mpl_visual_context.image_effect import LightSource

pe_waffle2 = ImageEffect(Pad(10) | LightSource(azdeg=215))

for p in ax.patches:
    p.set_path_effects([pe_waffle2])
