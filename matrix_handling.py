def matrix_packaging(values,row,column):
    mat1 = []
    index = 0
    for i in range(row):
        temp = []
        for j in range(column):
            temp.append(values[index])
            index += 1
        mat1.append(temp)
    return mat1


print(matrix_packaging([1,2,3,4,5,6],2,3))

