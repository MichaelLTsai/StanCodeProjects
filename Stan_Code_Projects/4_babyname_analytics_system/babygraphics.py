"""
File: babygraphics.py
Name: 蔡霖(Michael Tsai)
--------------------------------
SC101 Baby Names Project
Adapted from Nick Parlante's Baby Names assignment by
Jerry Liao.
"""

import tkinter
import babynames
import babygraphicsgui as gui

FILENAMES = [
    'data/full/baby-1900.txt', 'data/full/baby-1910.txt',
    'data/full/baby-1920.txt', 'data/full/baby-1930.txt',
    'data/full/baby-1940.txt', 'data/full/baby-1950.txt',
    'data/full/baby-1960.txt', 'data/full/baby-1970.txt',
    'data/full/baby-1980.txt', 'data/full/baby-1990.txt',
    'data/full/baby-2000.txt', 'data/full/baby-2010.txt'
]
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 600
YEARS = [1900, 1910, 1920, 1930, 1940, 1950,
         1960, 1970, 1980, 1990, 2000, 2010]
GRAPH_MARGIN_SIZE = 20
COLORS = ['red', 'purple', 'green', 'blue']
TEXT_DX = 2
LINE_WIDTH = 2
MAX_RANK = 1000


def get_x_coordinate(width, year_index):
    """
    Given the width of the canvas and the index of the current year
    in the YEARS list, returns the x coordinate of the vertical
    line associated with that year.

    Input:
        width (int): The width of the canvas
        year_index (int): The index where the current year is in the YEARS list
    Returns:
        x_coordinate (int): The x coordinate of the vertical line associated
                            with the current year.
    """
    interval = (width-GRAPH_MARGIN_SIZE-GRAPH_MARGIN_SIZE)/len(YEARS)
    x_coordinate = GRAPH_MARGIN_SIZE + interval * year_index

    return x_coordinate


def draw_fixed_lines(canvas):
    """
    Draws the fixed background lines on the canvas.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.
    """
    canvas.delete('all')            # delete all existing lines from the canvas

    # ----- Write your code below this line ----- #

    canvas.create_line(GRAPH_MARGIN_SIZE, GRAPH_MARGIN_SIZE, CANVAS_WIDTH-GRAPH_MARGIN_SIZE, GRAPH_MARGIN_SIZE)
    canvas.create_line(GRAPH_MARGIN_SIZE, CANVAS_HEIGHT-GRAPH_MARGIN_SIZE, CANVAS_WIDTH-GRAPH_MARGIN_SIZE, CANVAS_HEIGHT-GRAPH_MARGIN_SIZE)
    # canvas.create_line(GRAPH_MARGIN_SIZE, 0, GRAPH_MARGIN_SIZE, CANVAS_HEIGHT)
    # canvas.create_line(CANVAS_WIDTH-GRAPH_MARGIN_SIZE, 0, CANVAS_WIDTH-GRAPH_MARGIN_SIZE, CANVAS_HEI
    for i in range(len(YEARS)):
        x = get_x_coordinate(CANVAS_WIDTH, i)
        canvas.create_line(x, 0, x, CANVAS_HEIGHT)
        canvas.create_text(x+TEXT_DX, CANVAS_HEIGHT-GRAPH_MARGIN_SIZE, text=str(YEARS[i]), anchor=tkinter.NW)
    # The first solution comes in my mind, proved to work
    # gap = 0
    # interval = (CANVAS_WIDTH-GRAPH_MARGIN_SIZE-GRAPH_MARGIN_SIZE) / len(YEARS)
    # for year in YEARS:
    #     canvas.create_line(GRAPH_MARGIN_SIZE+gap, 0, GRAPH_MARGIN_SIZE+gap, CANVAS_HEIGHT)
    #     canvas.create_text(GRAPH_MARGIN_SIZE+gap+TEXT_DX, CANVAS_HEIGHT-GRAPH_MARGIN_SIZE,
    #                        text=str(year), anchor=tkinter.NW)
    #     gap += interval


def draw_names(canvas, name_data, lookup_names):
    """
    Given a dict of baby name data and a list of name, plots
    the historical trend of those names onto the canvas.

    Input:
        canvas (Tkinter Canvas): The canvas on which we are drawing.
        name_data (dict): Dictionary holding baby name data
        lookup_names (List[str]): A list of names whose data you want to plot

    Returns:
        This function does not return any value.
    """
    draw_fixed_lines(canvas)        # draw the fixed background grid

    # ----- Write your code below this line ----- #
    height_interval = (CANVAS_HEIGHT-GRAPH_MARGIN_SIZE-GRAPH_MARGIN_SIZE) / MAX_RANK
    c = 0
    for name in lookup_names:
        color = COLORS[c]
        if c >= len(COLORS)-1:
            c -= len(COLORS)-1
        else:
            c += 1
        for i in range(len(YEARS)):
            year = str(YEARS[i])
            if i <= 0:
                xs = get_x_coordinate(CANVAS_WIDTH, i)
                if year not in name_data[name]:
                    rank = "*"
                    ys = CANVAS_HEIGHT-GRAPH_MARGIN_SIZE
                else:
                    rank = name_data[name][year]
                    ys = GRAPH_MARGIN_SIZE + height_interval * int(rank)
                canvas.create_text(xs + TEXT_DX, ys, text=f"{name} {rank}", anchor=tkinter.SW, fill=color)
            else:
                xe = get_x_coordinate(CANVAS_WIDTH, i)
                if year not in name_data[name]:
                    rank = "*"
                    ye = CANVAS_HEIGHT-GRAPH_MARGIN_SIZE
                else:
                    rank = name_data[name][year]
                    ye = GRAPH_MARGIN_SIZE + height_interval * int(rank)
                canvas.create_line(xs, ys, xe, ye, width=LINE_WIDTH, fill=color)
                canvas.create_text(xe + TEXT_DX, ye, text=f"{name} {rank}", anchor=tkinter.SW, fill=color)
                xs = xe
                ys = ye


# main() code is provided, feel free to read through it but DO NOT MODIFY
def main():
    # Load data
    name_data = babynames.read_files(FILENAMES)

    # Create the window and the canvas
    top = tkinter.Tk()
    top.wm_title('Baby Names')
    canvas = gui.make_gui(top, CANVAS_WIDTH, CANVAS_HEIGHT, name_data, draw_names, babynames.search_names)

    # Call draw_fixed_lines() once at startup so we have the lines
    # even before the user types anything.
    draw_fixed_lines(canvas)

    # This line starts the graphical loop that is responsible for
    # processing user interactions and plotting data
    top.mainloop()


if __name__ == '__main__':
    main()
