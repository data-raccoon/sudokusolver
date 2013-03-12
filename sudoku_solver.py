#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""sudoku_solver.py

Solves Sudoku.

"""

__status__ = "Development"

import argparse
import numpy


def vstack(*lists):
    """ vstack(*lists)

    Returns a list of lists, stacking vertically the input lists. Make sure all
    input lists have the same lengths.

    Parameters
    ----------
    *lists: arbitrary number of lists of same length

    Returns
    -------
    out: list of lists

    """
    # check if all lists have the same length
    lengths = set()
    for item in lists:
        lengths.add(len(lists))
    if len(lengths) > 1:
        raise ValueError("lists have different lengths")

    # build vstacked result
    if len(lengths) > 0:
        length = list(lengths)[0]
        res = []
        count = len(lists)
        for i in range(length):
            part = []
            for j in range(count):
                part.append(lists[j][i])
            res.append(part)
    else:
        res = []

    return res


class SudokuNumber(object):
    """Represents one number in sudoku. Holds all additional info."""
    def __init__(self, number):
        """SudokuNumber()
        """
        if number != 0:  # init as filled
            self.solution = number
            self.marked = numpy.ones(9, dtype=bool)
            self.marked[number - 1] = False
        else:  # init as blank
            self.solution = None
            self.marked = numpy.zeros(9, dtype=bool)

    def mark(self, number)
        """mark(number)

        Marks number as not available as solution.

        Parameters
        ----------
        number: int
            The number to mark as not available as solution.

        Returns
        -------
        out: None / int
            Returns an int if solution is found, None otherwise.

        """
        marked = self.marked
        marked[number - 1] = True
        if marked.sum() == 8:
            self.solution = numpy.where(marked == False) + 1
            return self.solution
        return None


class SudokuField(object):
    """Represents the full 9x9 sudoku field."""
    def __init__(self, init_field):
        """SudokuField(field)

        Parameters
        ----------
        field: list of lists or 2d numpy array, of ints
            Holds sudoku numbers or 0 (empty).

        Methods
        -------
        solve()
            Solves the sudoku and returns the solution.
        """
        self.init_field = numpy.array(init_field, dtype=int)
        self.field = numpy.ndarray((9,9), dtype=object)
        vSudokuNumber = numpy.vectorize(SudokuNumber)
        self.field[:,:] = vSudokuNumber(field)

    def show(self, full=False):
        """show()

        Shows the current state of the sudoku. 

        """
        if full:
            pass
        else:
            field = []
            for idx in range(9):
                field.append([])
                for idy in range(9):
                    field[idx].append(self.field[idx, idy].solution)

    def solve(self):
        """solve()

        Solves the sudoku and shows the solution.

        """
        coordxy = numpy.where(self.init_field != 0)
        coordx = list(coordxy[0])
        coordy = list(coordxy[1])
        coord_list = vstack(coordx, coordy)

        # attention: the following list is being extended during runtime
        for coords in coord_list:
            # the number at coords may not occur at the same column, row or
            # sector. mark all those.
            cur_row = coords[0]
            cur_col = coords[1]
            solution = self.field[cur_row, cur_col].solution
            print "marking number", solution, "from" cur_row + 1, cur_col + 1
            # mark within row
            cols = range(9)
            cols.pop(cur_col)
            for col in cols:
                res = self.field[cur_row, col].mark(solution)
                if res:
                    coords.append([cur_row, col])
            # mark within column
            rows = range(9)
            rows.pop(cur_row)
            for row in rows:
                res = self.field[row, cur_col].mark(solution)
                if res:
                    coords.append([row, cur_col])
            # mark within rest of sector (4 coords)
            cur_secnr_row = cur_row / 3
            cur_secnr_col = cur_col / 3
            cur_insec_row = cur_row % 3
            cur_insec_col = cur_col % 3
            insec_rows = range(3)
            insec_rows.pop(insec_row)
            insec_cols = range(3)
            insec_cols.pop(insec_col)
            for insec_row in insec_rows:
                row = cur_secnr_row * 3 + insec_row
                for insec_col in insec_cols:
                    col = cur_secnr_col * 3 + insec_col
                    res = self.field[row, col].mark(solution)
                    if res:
                        coords.append([row, col])

        # show solution
        self.show()


if __name__ == "__main__":
    field = [[0,0,0,9,0,0,7,0,0],
            [5,4,0,0,0,0,0,6,3],
            [0,0,1,6,3,2,0,0,0],
            [1,0,0,0,6,8,2,0,9],
            [9,2,0,0,0,0,0,8,1],
            [4,0,8,2,1,0,0,0,5],
            [0,0,0,3,7,1,4,0,0],
            [3,1,0,0,0,0,0,9,7],
            [0,0,6,0,0,4,0,0,0]]
    myField = SudokuField(field)
    myField.show()
    myField.solve()
    