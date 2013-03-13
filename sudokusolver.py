#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""sudokusolver.py

Solves easy sudoku.

"""

__status__ = "Development"

import argparse
import numpy
import pprint


def vstack(*lists):
    """ vstack(*lists)

    Returns a list of lists, stacking vertically the input lists. Make sure
    all input lists have the same lengths.

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
        lengths.add(len(item))
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


def check(solution, org_field=None):
    """check(solution, org_field=None):

    Checks if solution indeed is a solved sudoku. If org_field is given,
    additionally checks if no alterations were made.

    Parameters
    ----------
    solution: list of lists or 2d numpy array, of ints / SudokuField
        Assumed solution of a sudoku / of the sudoku org_field.
    org_field: optional, list of lists or 2d numpy array, of ints
        Original sudoku which should be solved by solution. Defaults to None.

    Returns
    -------
    out: bool
        If solution is indeed a sudoku solution or the sudoku solution to
        org_field.
    """
    if not type(solution) == numpy.ndarray:
        solution = numpy.array(solution, dtype=int)

    ref = numpy.arange(1,10)
    # check rows
    for row in solution:
        row = numpy.copy(row)
        row.sort()
        if not (row == ref).all():
            return False
    # check cols
    for col in solution.transpose():
        col = numpy.copy(col)
        col.sort()
        if not (col == ref).all():
            return False
    # check sectors
    for idx in range(3):
        for idy in range(3):
            sec = solution[0 + idx * 3:3 + idx * 3,
                0 + idy * 3:3 + idy * 3].flatten()
            sec.sort()
            if not (sec == ref).all():
                return False

    # check original
    if not org_field is None:
        if not type(org_field) == numpy.ndarray:
            org_field = numpy.array(org_field, dtype=int)
        coords = numpy.where(org_field != 0)
        if not (org_field[coords] == solution[coords]).all():
            return False

    return True

class SudokuNumber(object):
    """Represents one number in sudoku. Holds all additional info."""
    def __init__(self, number):
        """SudokuNumber()

        """
        self.solution = number
        if number != 0:  # init as filled
            self.mask = numpy.zeros(9, dtype=bool)
            self.mask[number - 1] = True
        else:  # init as blank
            self.mask = numpy.ones(9, dtype=bool)

    def mark(self, number):
        """mark(number)

        Marks number as not available as solution and returns if that led to
        finding a solution (all but one number marked).

        Parameters
        ----------
        number: int
            The number to mark as not available as solution.

        Returns
        -------
        out: bool
            Returns if a solution was found.

        """
        mask = self.mask
        if self.solution == 0:
            mask[number - 1] = False
            if mask.sum() == 1:
                self.solution = numpy.where(mask == True)[0][0] + 1
                return True
            return False


class SudokuField(object):
    """Represents the full 9x9 sudoku field."""
    def __init__(self, init_field):
        """SudokuField(init_field)

        Parameters
        ----------
        init_field: list of lists or 2d numpy array, of ints
            Holds sudoku numbers or 0 (empty).

        Methods
        -------
        solve()
            Solves the sudoku and returns the solution.
        """
        self.init_field = numpy.array(init_field, dtype=int)
        self.field = numpy.ndarray((9, 9), dtype=object)
        vec_sudoku_number = numpy.vectorize(SudokuNumber)
        self.field[:, :] = vec_sudoku_number(init_field)

    def get_current_field(self):
        """get_current_field()"""
        field = []
        for idx in range(9):
            part = []
            for idy in range(9):
                entry = self.field[idx, idy].solution
                part.append(entry)
            field.append(part)
        return field

    def get_current_state(self):
        """get_current_state()"""
        # TODO yet to write
        pass

    def __repr__(self):
        """String representation of SudokuField."""
        # TODO change to current_state
        return self.get_current_field().__repr__()

    def show(self, full=False):
        """show()

        Shows the current state of the sudoku.

        """
        if full:
            # TODO current_state
            pass
        else:
            pp = pprint.PrettyPrinter()
            pp.pprint(self.get_current_field())

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
            # TODO build up coords to check first, then do one loop

            # the number at coords may not occur at the same column, row or
            # sector. mark all those.
            cur_row = coords[0]
            cur_col = coords[1]
            solution = self.field[cur_row, cur_col].solution
            # mark within row
            cols = range(9)
            cols.pop(cur_col)
            for col in cols:
                res = self.field[cur_row, col].mark(solution)
                if res:
                    coord_list.append([cur_row, col])
            # mark within column
            rows = range(9)
            rows.pop(cur_row)
            for row in rows:
                res = self.field[row, cur_col].mark(solution)
                if res:
                    coord_list.append([row, cur_col])
            # mark within rest of sector (4 coords)
            cur_secnr_row = cur_row / 3
            cur_secnr_col = cur_col / 3
            cur_insec_row = cur_row % 3
            cur_insec_col = cur_col % 3
            insec_rows = range(3)
            insec_rows.pop(cur_insec_row)
            insec_cols = range(3)
            insec_cols.pop(cur_insec_col)
            for insec_row in insec_rows:
                row = cur_secnr_row * 3 + insec_row
                for insec_col in insec_cols:
                    col = cur_secnr_col * 3 + insec_col
                    res = self.field[row, col].mark(solution)
                    if res:
                        coord_list.append([row, col])

        return self.get_current_field()


if __name__ == "__main__":
    # example field
    FIELD = [[0, 0, 0, 9, 0, 0, 7, 0, 0],
             [5, 4, 0, 0, 0, 0, 0, 6, 3],
             [0, 0, 1, 6, 3, 2, 0, 0, 0],
             [1, 0, 0, 0, 6, 8, 2, 0, 9],
             [9, 2, 0, 0, 0, 0, 0, 8, 1],
             [4, 0, 8, 2, 1, 0, 0, 0, 5],
             [0, 0, 0, 3, 7, 1, 4, 0, 0],
             [3, 1, 0, 0, 0, 0, 0, 9, 7],
             [0, 0, 6, 0, 0, 4, 0, 0, 0]]
    """
    [[6, 8, 3, 9, 4, 5, 7, 1, 2],
     [5, 4, 2, 1, 8, 7, 9, 6, 3],
     [7, 9, 1, 6, 3, 2, 8, 5, 4],
     [1, 3, 5, 7, 6, 8, 2, 4, 9],
     [9, 2, 7, 4, 5, 3, 6, 8, 1],
     [4, 6, 8, 2, 1, 9, 3, 7, 5],
     [8, 5, 9, 3, 7, 1, 4, 2, 6],
     [3, 1, 4, 8, 2, 6, 5, 9, 7],
     [2, 7, 6, 5, 9, 4, 1, 3, 8]]
    """
    #FIELD = [[8, 0, 5, 0, 0, 2, 0, 0, 0],
             #[1, 0, 0, 4, 0, 0, 9, 0, 0],
             #[0, 0, 7, 1, 0, 0, 0, 0, 0],
             #[2, 0, 3, 0, 0, 0, 0, 0, 1],
             #[0, 0, 1, 5, 0, 9, 8, 0, 0],
             #[5, 0, 0, 0, 0, 0, 6, 0, 2],
             #[0, 0, 0, 0, 0, 5, 4, 0, 0],
             #[0, 0, 6, 0, 0, 3, 0, 0, 8],
             #[0, 0, 0, 7, 0, 0, 2, 0, 3]]
    SUDOKU = SudokuField(FIELD)
    SUDOKU.show()
    SUDOKU.solve()
