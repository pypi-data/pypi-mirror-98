import logging
from pathlib import Path

import numpy as np
from skimage.transform import AffineTransform, warp

from astropy.io import fits

from vtfcal.reconstruction.speckle import calc_fried_param, run_speckle


def reconstruct(asdf_file):
    logger = logging.getLogger(__name__)
    # Not sure if I should be doing this one per modstate or not?

    r0 = calc_fried_param()
    # Things that should change here:
    # - autoget width and height (from a previous image I guess, or from run metadata)
    # - separate files into bursts (by timestamps? burst metadata) and repeat below for each burst
    # - autoget burst size from number of files
    # - use burst min/max timestamps to sort AO data for r0 calculation
    specframe = run_speckle(
        width=1024,
        height=1024,
        burst_directory="vtfTestImages",
        burst_prefix="cssSim_1024x1024",
        burst_suffix=".raw",
        burst_size=99,
        fixed_width=3,
        gpus=0,
        fried_parameter=r0,
    )

    outdir = asdf_file["support"]["data_dir"]
    fname = Path(outdir) / f"speckle-output.FITS"

    logger.warning(
        "Speckle images do not match size of simulated VTF data - scaling to match."
    )
    specframe = warp(
        specframe,
        AffineTransform(matrix=np.array([[0.5, 0, 0], [0, 0.5, 0], [0, 0, 1]])).inverse,
        output_shape=(512, 512),
        cval=specframe.mean(),
    )
    fits.writeto(fname, specframe, overwrite=True)

    return asdf_file
