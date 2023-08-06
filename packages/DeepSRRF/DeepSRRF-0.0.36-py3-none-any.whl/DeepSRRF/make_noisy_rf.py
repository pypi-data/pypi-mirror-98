import sys
from sys import argv
from os import  makedirs, rename
from os.path import isfile, join, exists, splitext, abspath, basename, dirname, isdir
import numpy as np
import utils

from PIL import Image
from tqdm import tqdm

from scipy.io import loadmat, savemat
from skimage.util import random_noise


path = r"D:\calisma\projeler\SR on RF\dataset\test"

subdir = r"noisy"

modes= ["speckle", "gaussian"]

bmode = True
bmode_range = 80
log_coef = 20

image_extentions = ["*.bmp", "*.BMP", "*.jpg", "*.JPG", "*.png", "*.PNG", "*.jpeg", "*.JPEG", "*.TIFF", "*.tiff", '*.mat']

def save_mat_file(file_path, img):

    rf = {"rf": img}

    savemat(file_path, rf)


def load_mat_file(file):

    pic = loadmat(file)
    keys = pic.keys()

    if 'rf' in keys:
        rf = pic['rf']

    elif 'signals_matrix' in keys:
        rf = pic['signals_matrix']

    else:
        print('Unknown rf variable name please check the file ', file)
        return None
    return rf


test_files = utils.get_files(
    path, image_extentions, remove_extension=False, full_path=True)
test_file_names = [splitext(basename(x))[0] for x in test_files]

# for each test images
for i in tqdm(range(len(test_files))):
    f = test_files[i]

    file_name = basename(f)
    file_short_name = splitext(file_name)[0]
    # print(f)

    _im = load_mat_file(f)

    for mode in modes:

        if mode =="gaussian":
            variances = [0.00001, 0.00005, 0.0001, 0.0005, 0.001]
        else: # speckle
            variances = [1, 5, 10, 25, 50]

        for variance in variances:

            noisy_img = random_noise(_im, mode=mode, mean=0, var=variance)

            new_dir = join(path, subdir, mode, str(variance))

            if not exists(new_dir):
                makedirs(new_dir)

            new_file = join(new_dir, file_name)

            # img_org = utils.RF_to_Bmode(_im, bmode, bmode_range, log_coef, True)
            # Image.fromarray(img_org).save(join(new_dir, file_short_name + "_original_.png"))

            save_mat_file(new_file, noisy_img)

            img = utils.RF_to_Bmode(noisy_img, bmode, bmode_range, log_coef)

            new_dir = join(path, subdir, mode, str(variance), "80dB")

            if not exists(new_dir):
                makedirs(new_dir)

            new_file = join(new_dir, file_short_name + ".png")

            img = Image.fromarray(img).save(new_file)



def make_noisy(mode="gaussian", mean=0, var=1e-3):
    pass
