import os
import sys

from importlib import resources
from zipfile import ZipFile


def download_lato_font(verbose=False):

    RUNNING_IN_COLAB = "google.colab" in sys.modules

    if not RUNNING_IN_COLAB:
        if verbose:
            print(
                """
                Not running in Google Colab. For best results ensure you have
                the Lato font installed on your system.
                """
            )
        return

    # if we are running in Google Colab, we need to install the correct font
    # from https://www.1001freefonts.com/d/5722/lato.zip to the right place:
    mpl_fonts = "/usr/local/lib/python3.6/dist-packages/matplotlib/mpl-data/fonts/ttf/"

    if verbose:
        print("... extracting lato.zip contents to mpl-data/fonts ...")

    font_file = resources.path("apol_dataviz", "fonts/lato.zip")

    with ZipFile(font_file, "r") as zip:
        zip.extractall(mpl_fonts)

    if verbose:
        print("... cleaning up ...")

    os.remove(mpl_fonts + "OFL.txt")

    if verbose:
        print("... complete.")
