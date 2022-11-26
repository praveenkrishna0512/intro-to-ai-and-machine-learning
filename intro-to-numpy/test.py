import copy

def row_mult_scalar(row, c):
  """
  Multiplies row by a scalar c.
  """
  return list(map(lambda value : c * value, row))

def add_rows(rowA, rowB):
  """
  Adds row B to row A.
  """
  if len(rowA) != len(rowB):
    raise Exception('A and B cannot be added as they have incompatible dimensions!')

  return list(map(lambda valA, valB: valA + valB, rowA, rowB))

def mult_matrices(A, B):
  """
  Multiplies matrix A by matrix B, giving AB.
  """
  if len(A[0]) != len(B):
    raise Exception('Incompatible dimensions for matrix multiplication of A and B')
  
  if len(A) == 0:
      return []
  
  rowsA = len(A)
  colsA = len(A[0])
  rowsB = len(B)
  colsB = len(B[0])
  
  resultRow = [None for x in range(colsB)]
  result = [resultRow.copy() for y in range(rowsA)]
  
  for i in range(rowsA):
    for j in range(colsB):
        result[i][j] = 0
        for z in range(colsA):
            result[i][j] += A[i][z] * B[z][j]
            
  return result

def invert_matrix(A):
  """
  Finds the inverse of matrix A, if it exists; otherwise, an exception is
  thrown.
  """
  if len(A[0]) != len(A):
    raise Exception('Non-square matrices cannot be inverted')

  rows = len(A)
  cols = len(A[0])

  # Form adjacency matrix
  result = copy.deepcopy(A)
  for rowIndex in range(rows):
    row = result[rowIndex]
    for i in range(cols):
      if i == rowIndex:
        row.append(1)
      else:
        row.append(0)

  # Form RREF matrix
  for colIndex in range(cols):
    foundRow = False
    for rowIndex in range(colIndex, len(result)):
      if result[rowIndex][colIndex] == 0:
        continue
      foundRow = True
      selectedRow = result[rowIndex].copy()
      if rowIndex != colIndex:
        result[rowIndex] = result[colIndex]
      selectedValue = selectedRow[colIndex]
      selectedRow = row_mult_scalar(selectedRow, 1 / selectedValue)
      result[colIndex] = selectedRow
      for resultRowIndex in range(len(result)):
        row = result[resultRowIndex]
        multiple = row[colIndex]
        if multiple == 0 or resultRowIndex == colIndex:
          continue
        minusRow = row_mult_scalar(selectedRow, -1 * multiple)
        result[resultRowIndex] = add_rows(minusRow, row)
    if not foundRow:
      raise Exception("Matrix is not invertible")
  
  # Extract inverse matrix
  inverse = []
  for row in result:
    newRow = []
    for colIndex in range(cols, cols * 2):
      newRow.append(row[colIndex])
    inverse.append(newRow)

  return inverse

import random
import time

import numpy as np



# print(invert_matrix([[4, 4, 0], [0, 1, 0], [0, 9, 0]]))