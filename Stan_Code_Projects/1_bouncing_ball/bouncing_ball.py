"""
File: Bouncing_ball.py
Name: 蔡霖(Michael Tsai)
-------------------------
This file shows a bouncing ball animation
by campy library
"""

from campy.graphics.gobjects import GOval, GLabel
from campy.graphics.gwindow import GWindow
from campy.gui.events.timer import pause
from campy.gui.events.mouse import onmouseclicked

# Vertical speed
VX = 3

# This set the pause time (in millisecond) for animation
DELAY = 12
GRAVITY = 1
SIZE = 20
REDUCE = 0.9

# Here are the starting point of the bouncing ball
START_X = 30
START_Y = 40
window = GWindow(800, 500, title='bouncing_ball.py')

# Create a point in global area
point = GOval(SIZE, SIZE)
point.filled = True

# Set a variable (count) to count the clicking times
# Set a initial horizontal speed (vy) in 0
count = vy = 0

# Set a switch(True = Open; False = Close) to control the clicking() function
# Default False(Close)
switch_on = False

# Additional counting board to show remain clicking.
count_board = GLabel("Click to start (Total 3 times)")


def main():
    """
    This program simulates a bouncing ball at (START_X, START_Y)
    that has VX as x velocity and 0 as y velocity. Each bounce reduces
    y velocity to REDUCE of itself.
    """
    global switch_on
    window.add(point, x=START_X, y=START_Y)
    onmouseclicked(clicking)

    # add count_board with 30 font
    count_board.font = "-30"
    window.add(count_board, x=0, y=count_board.height+10)


def clicking(hit):
    global vy, count, switch_on

    # Every click can turn the switch to True(open)
    switch_on = True
    while count < 3 and switch_on is True:
        count_board.text = f"{2 - count} Time Left"
        point.move(VX, vy)

        # to avoid point stock below window.height,
        # Set a condition vy > 0.
        if point.y + SIZE >= window.height and vy > 0:
            vy = -vy * REDUCE
        vy += GRAVITY
        pause(DELAY)
        if point.x >= window.width:
            count += 1
            window.add(point, x=START_X, y=START_Y)
            switch_on = False
            break
    if count == 3:
        count_board.text = "The end. Thanks for playing!"


if __name__ == "__main__":
    main()
