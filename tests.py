#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""tests.py

Tests for sudoku_solver.py.
Examples taken from www.websudoku.com.

"""

import unittest
import sudokusolver

class SudokuFieldTests(unittest.TestCase):

    def test_solve_easy_xxx(self):
        field = [[0, 0, 0, 9, 0, 0, 7, 0, 0],
                 [5, 4, 0, 0, 0, 0, 0, 6, 3],
                 [0, 0, 1, 6, 3, 2, 0, 0, 0],
                 [1, 0, 0, 0, 6, 8, 2, 0, 9],
                 [9, 2, 0, 0, 0, 0, 0, 8, 1],
                 [4, 0, 8, 2, 1, 0, 0, 0, 5],
                 [0, 0, 0, 3, 7, 1, 4, 0, 0],
                 [3, 1, 0, 0, 0, 0, 0, 9, 7],
                 [0, 0, 6, 0, 0, 4, 0, 0, 0]]
        sudoku = sudokusolver.SudokuField(field)
        solution = sudoku.solve()
        self.assertEqual(True, sudokusolver.check(solution, field))

    def test_solve_easy_5638580930(self):
        field = [[7, 2, 3, 1, 9, 6, 0, 0, 8],
                 [0, 0, 0, 0, 0, 0, 6, 2, 0],
                 [0, 0, 6, 8, 0, 0, 0, 1, 7],
                 [0, 0, 0, 2, 4, 0, 0, 0, 0],
                 [8, 7, 0, 3, 0, 9, 0, 5, 2],
                 [0, 0, 0, 0, 1, 7, 0, 0, 0],
                 [3, 8, 0, 0, 0, 5, 9, 0, 0],
                 [0, 4, 7, 0, 0, 0, 0, 0, 0],
                 [1, 0, 0, 9, 2, 3, 7, 8, 4]]
        sudoku = sudokusolver.SudokuField(field)
        solution = sudoku.solve()
        self.assertEqual(True, sudokusolver.check(solution, field))

    def test_solve_medium_2180302949(self):
        field = [[0, 0, 0, 0, 8, 0, 6, 0, 7],
                 [0, 0, 0, 1, 5, 4, 0, 3, 0],
                 [0, 2, 0, 0, 7, 0, 0, 0, 4],
                 [0, 0, 0, 0, 0, 3, 7, 0, 0],
                 [1, 4, 0, 0, 0, 0, 0, 5, 2],
                 [0, 0, 3, 9, 0, 0, 0, 0, 0],
                 [4, 0, 0, 0, 2, 0, 0, 7, 0],
                 [0, 6, 0, 4, 3, 7, 0, 0, 0],
                 [3, 0, 2, 0, 9, 0, 0, 0, 0]]
        sudoku = sudokusolver.SudokuField(field)
        solution = sudoku.solve()
        self.assertEqual(True, sudokusolver.check(solution, field))

    def test_solve_hard_6532826723(self):
        field = [[0, 6, 0, 0, 8, 9, 4, 3, 0],
                 [2, 0, 1, 4, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 2, 0, 6, 0],
                 [0, 0, 0, 0, 0, 0, 0, 9, 4],
                 [0, 0, 6, 0, 1, 0, 8, 0, 0],
                 [3, 7, 0, 0, 0, 0, 0, 0, 0],
                 [0, 5, 0, 7, 0, 0, 0, 0, 0],
                 [0, 0, 0, 0, 0, 1, 3, 0, 6],
                 [0, 4, 9, 3, 5, 0, 0, 1, 0]]
        sudoku = sudokusolver.SudokuField(field)
        solution = sudoku.solve()
        self.assertEqual(True, sudokusolver.check(solution, field))

    def test_solve_evil_7167033650(self):
        field = [[8, 4, 1, 0, 0, 7, 6, 0, 0],
                 [0, 0, 0, 0, 0, 4, 0, 0, 0],
                 [7, 0, 0, 0, 2, 0, 0, 1, 0],
                 [0, 0, 0, 0, 0, 2, 0, 3, 0],
                 [9, 0, 0, 0, 4, 0, 0, 0, 5],
                 [0, 1, 0, 8, 0, 0, 0, 0, 0],
                 [0, 2, 0, 0, 8, 0, 0, 0, 3],
                 [0, 0, 0, 2, 0, 0, 0, 0, 0],
                 [0, 0, 6, 1, 0, 0, 7, 5, 2]]
        sudoku = sudokusolver.SudokuField(field)
        solution = sudoku.solve()
        self.assertEqual(True, sudokusolver.check(solution, field))


if __name__ == "__main__":
    unittest.main()
