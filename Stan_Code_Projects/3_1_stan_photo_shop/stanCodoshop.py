"""
File: stanCodoshop.py
Name: 蔡霖(Michael Tsai)
----------------------------------------------
SC101_Assignment3 Adapted from Nick Parlante's
Ghost assignment by Jerry Liao.
"""

import os
import sys
from simpleimage import SimpleImage


def get_pixel_dist(pixel, red, green, blue):
    """
    Returns a value that refers to the "color distance" between a pixel and a mean RGB value.

    Input:
        pixel (Pixel): the pixel with RGB values to be compared
        red (int): the average red value of the pixels to be compared
        green (int): the average green value of the pixels to be compared
        blue (int): the average blue value of the pixels to be compared

    Returns:
        dist (float): the "color distance" of a pixel to the average RGB value of the pixels to be compared.
    """
    color_dis = ((red-pixel.red) ** 2 + (green-pixel.green) ** 2 + (blue-pixel.blue) ** 2) ** 0.5
    return color_dis


def get_average(pixels):
    """
    Given a list of pixels, finds their average red, blue, and green values.

    Input:
        pixels (List[Pixel]): a list of pixels to be averaged

    Returns:
        rgb (List[int]): a list of average red, green, and blue values of the pixels
                        (returns in order: [red, green, blue])
    """
    r_ttl = g_ttl = b_ttl = 0
    for pixel in pixels:
        r_ttl += pixel.red
        g_ttl += pixel.green
        b_ttl += pixel.blue
    r_avg = r_ttl // len(pixels)
    g_avg = g_ttl // len(pixels)
    b_avg = b_ttl // len(pixels)
    avg_pixel = [r_avg, g_avg, b_avg]
    return avg_pixel


def get_best_pixel(pixels):
    """
    Given a list of pixels, returns the pixel with the smallest "color distance", which has the closest color to the average.

    Input:
        pixels (List[Pixel]): a list of pixels to be compared
    Returns:
        best (Pixel): the pixel which has the closest color to the average
    """
    min_dis = best_pixel = None
    r_avg = get_average(pixels)[0]
    g_avg = get_average(pixels)[1]
    b_avg = get_average(pixels)[2]
    for pixel in pixels:
        color_distance = get_pixel_dist(pixel, r_avg, g_avg, b_avg)
        if min_dis is None:
            min_dis = color_distance
            best_pixel = pixel
        if color_distance < min_dis:
            min_dis = color_distance
            best_pixel = pixel
    return best_pixel



def solve(images):
    """
    Given a list of image objects, compute and display a Ghost solution image
    based on these images. There will be at least 3 images and they will all
    be the same size.

    Input:
        images (List[SimpleImage]): list of images to be processed
    """
    width = images[0].width
    height = images[0].height
    result = SimpleImage.blank(width, height)
    for x in range(result.width):
        for y in range(result.height):
            pixel_lst = []
            for image in images:
                pixel_lst.append(image.get_pixel(x, y))
            new_pixel = result.get_pixel(x, y)
            new_pixel.red = get_best_pixel(pixel_lst).red
            new_pixel.green = get_best_pixel(pixel_lst).green
            new_pixel.blue = get_best_pixel(pixel_lst).blue
    # green_pixel = SimpleImage.blank(20, 20, "green").get_pixel(0, 0)
    # blue_pixel = SimpleImage.blank(20, 20, "blue").get_pixel(0, 0)
    # print(get_average([green_pixel, green_pixel, green_pixel, blue_pixel]))
    print("Displaying image!")
    result.show()


def jpgs_in_dir(dir):
    """
    (provided, DO NOT MODIFY)
    Given the name of a directory, returns a list of the .jpg filenames
    within it.

    Input:
        dir (string): name of directory
    Returns:
        filenames(List[string]): names of jpg files in directory
    """
    filenames = []
    for filename in os.listdir(dir):
        if filename.endswith('.jpg'):
            filenames.append(os.path.join(dir, filename))
    return filenames


def load_images(dir):
    """
    (provided, DO NOT MODIFY)
    Given a directory name, reads all the .jpg files within it into memory and
    returns them in a list. Prints the filenames out as it goes.

    Input:
        dir (string): name of directory
    Returns:
        images (List[SimpleImages]): list of images in directory
    """
    images = []
    jpgs = jpgs_in_dir(dir)
    for filename in jpgs:
        print("Loading", filename)
        image = SimpleImage(filename)
        images.append(image)
    return images


def main():
    # (provided, DO NOT MODIFY)
    args = sys.argv[1:]
    # We just take 1 argument, the folder containing all the images.
    # The load_images() capability is provided above.
    images = load_images(args[0])
    solve(images)


if __name__ == '__main__':
    main()
