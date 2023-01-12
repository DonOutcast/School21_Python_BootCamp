cpdef mul(list first_matrix, list second_matrix):
    if len(first_matrix) > 100 or len(second_matrix) > 100 or len(
            first_matrix) == 0 or len(second_matrix) == 0:
        raise ValueError('Matrix must be less than 100 and more than 0')
    if len(first_matrix[0]) != len(second_matrix):
        raise ValueError('The number of columns of the 1st matrix'
                         ' must equal the number of rows of the 2nd matrix')
    cdef int row_first_matrix = len(first_matrix)
    cdef int colm_second_matrix = len(second_matrix[0])
    cdef int i
    cdef int j
    cdef int k
    cdef int temp
    cdef list result = []
    for i in range(row_first_matrix):
        result.append([0] * colm_second_matrix)
        for j in range(colm_second_matrix):
            temp = 0
            for k in range(len(second_matrix)):
                temp = first_matrix[i][k] * second_matrix[k][j] + temp
            result[i][j] = temp
    return result
