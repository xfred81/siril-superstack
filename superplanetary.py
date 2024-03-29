#!/usr/bin/env python3

from seqselector import QuickSelector
import os


path = '/media/fred/Red2T/Captures/Jup/090124/'
seq = 'Jup_195330.seq'
ser = seq.replace(".seq", ".ser")

def my_input(label: str, default: float):
    r = input(f"{label} (default: {default}): ")
    if r == '':
        r = default

    return r

def planetary(S: QuickSelector, seq_fname: str, from_idx: int, step: int, window: int, ratio: float, wavelets: list, rmgreen: str,
              sat_amount: float, sat_bg: float, asinh_stretch: float, asinh_bp: float):
    lines = ['requires 1.2.0\n']

    for idx in range(from_idx, S.image_count - window, step):
        lines += S.output_as_script(seq_fname, idx, int(idx/step), window, ratio, wavelets, rmgreen, sat_amount, sat_bg,
                                    asinh_stretch, asinh_bp)

    with open(f'{os.getenv("HOME")}/.siril/scripts/Superstack-planetary.ssf', 'w') as out_file:
        out_file.writelines(lines)

path = input("Path to .seq file: ")

print("\nPlease indicate the filename of the Siril sequence.\nSequence needs to be aligned!")
print("All selected frames will be used, and best ones will be kept.\n")
seq = input("Filename (including the .seq extension): ")
S = QuickSelector(path, seq)
print(f"Images in sequence: {S.image_count}")

img_path = f"{path}/img"
if not os.path.exists(img_path):
    os.makedirs(img_path)

from_idx = int(my_input("Starting frame", 0))
window = int(my_input("Window - consecutive frames to consider for a single final image", 2000))
ratio = float(my_input("Ratio of frames to be kept in window", 0.15))
step = int(my_input("Step - number of frames to shift window within SEQ file", int(S.image_count/100)))

wavelets = my_input("Give coefficients for wavelets (leave empty for no wavelet)", '')
wavelets = wavelets.split(" ")

rmgreen = my_input("Remove green noise", 'y')

sat_amount = float(my_input("Saturation amount - 0.0 to ignore", 0.0))
sat_bg = float(my_input("Saturation background - 0.0 to ignore", 0.0))

asinh_stretch = float(my_input("asinh stretch - 0.0 to ignore", 0.0))
asinh_bp = float(my_input("asinh's black point - 0.0 to ignore", 0.0))

print(f"\n{(S.image_count-window)/step} images to be generated through script.")
planetary(S, seq, from_idx, step, window, ratio, wavelets, rmgreen, sat_amount, sat_bg, asinh_stretch, asinh_bp)

print("\nGo in Siril, and use command 'reloadscripts' to detect and use the Superstack-planetary.ssf on target sequence")