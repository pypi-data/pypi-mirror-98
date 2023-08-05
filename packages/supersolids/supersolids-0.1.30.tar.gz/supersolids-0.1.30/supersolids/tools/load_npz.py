#!/usr/bin/env python

# author: Daniel Scheiermann
# email: daniel.scheiermann@stud.uni-hannover.de
# license: MIT
# Please feel free to use and modify this, but keep the above information.

"""
Animation for the numerical solver for the non-linear
time-dependent Schrodinger equation for 1D, 2D and 3D in single-core.

"""

import argparse
from pathlib import Path

from mayavi import mlab

from supersolids.Animation.Animation import Animation

from supersolids.Animation import MayaviAnimation


# Script runs, if script is run as main script (called by python *.py)
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Load old simulations of Schrödinger system "
                                                 "and create movie.")
    parser.add_argument("-dir_path", metavar="dir_path", type=str, default="~/supersolids/results",
                        help="Absolute path to load data from")
    parser.add_argument("-dir_name", metavar="dir_name", type=str, default="movie" + "%03d" % 1,
                        help="Name of directory where the files to load lie. "
                             "For example the standard naming convention is movie001")
    parser.add_argument("-filename_schroedinger", metavar="filename_schroedinger", type=str,
                        default="schroedinger.pkl",
                        help="Name of file, where the Schroedinger object is saved")
    parser.add_argument("-filename_steps", metavar="filename_steps",
                        type=str, default="step_",
                        help="Name of file, without enumarator for the files. "
                             "For example the standard naming convention is step_000001.npz, "
                             "the string needed is step_")
    parser.add_argument("-steps_format", metavar="steps_format",
                        type=str, default="%06d",
                        help="Formating string to enumerate the files. "
                             "For example the standard naming convention is step_000001.npz, "
                             "the string needed is percent 06d")
    parser.add_argument("-steps_per_npz", metavar="steps_per_npz",
                        type=int, default=10,
                        help="Number of dt steps skipped between saved npz.")
    parser.add_argument("-frame_start", metavar="frame_start",
                        type=int, default=0,
                        help="Counter of first saved npz.")
    parser.add_argument("--delete_input", default=False, action="store_true",
                        help="If flag is not used, the pictures after "
                             "animation is created and saved.")
    args = parser.parse_args()
    print(f"args: {args}")

    try:
        dir_path = Path(args.dir_path).expanduser()
    except Exception:
        dir_path = args.dir_path

    Anim: Animation = Animation(plot_psi_sol=False,
                                plot_V=False,
                                alpha_psi=0.8,
                                alpha_psi_sol=0.5,
                                alpha_V=0.3,
                                filename="anim.mp4",
                                )

    # mayavi for 3D
    MayAnim = MayaviAnimation.MayaviAnimation(Anim,
                                              dir_path=dir_path,
                                              )

    MayAnimator = MayAnim.animate_npz(dir_path=dir_path,
                                      dir_name=args.dir_name,
                                      filename_schroedinger=args.filename_schroedinger,
                                      filename_steps=args.filename_steps,
                                      steps_format=args.steps_format,
                                      steps_per_npz=args.steps_per_npz,
                                      frame_start=args.frame_start
                                      )
    mlab.show()

    result_path = MayAnim.create_movie(dir_path=MayAnim.dir_path,
                                       input_data_file_pattern="*.png",
                                       delete_input=args.delete_input)
