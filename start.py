# choose how to run the game for this run of the program

from ui.ui import UI

""" AI idea: 
find a point where the plane is hit
compute all the possible ways the plane can be positioned
    -> for every possible way found, increment with 1 the squares of that plane in an auxiliary matrix
find the median among the non-zero values in the auxiliary matrix; this is the balance between hitting
    the most likely point and missing the least likely point, both eliminating only a few possibilities 
hit there
repeat from computing all the ways the plane can be positioned until there is only one left
"""

UI()