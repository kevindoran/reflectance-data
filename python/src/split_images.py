#!/bin/python 

import PIL
import PIL.Image
import typer
import pathlib
import logging

"""Annoyingly, the dataset accompanying the paper doesn't have the 
matching photos of the specimen as separate files, so here we cut apart the 
single image containing the sub-images."""

NUM_IMAGES = 359

app = typer.Typer(name='split_images', add_completion=True, 
        help='Separate the single image from the paper into separate images')


def extract_img(idx, orig_img):
    orig_width, orig_height = orig_img.size
    sub_H = orig_height / NUM_IMAGES
    # (x「, y「, x」, y」)
    box = (0, idx * sub_H, orig_width, (idx+1)*sub_H)
    logging.info(box)
    sub_img = orig_img.crop(box)
    return sub_img


def img_filename(idx):
    return f'{idx}.png'


@app.command()
def split_images(in_path, out_dir):
    in_img = PIL.Image.open(in_path)

    # Out
    o_path = pathlib.Path(out_dir)
    o_path.mkdir(parents=False, exist_ok=True)
    for i in range(NUM_IMAGES):
        img = extract_img(i, in_img)
        img.save(o_path / pathlib.Path(img_filename(i)))


if __name__ == "__main__":
    #logging.getLogger().setLevel(logging.INFO)
    app()

