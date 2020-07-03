def checkIsConsecutiveFourInList(values):
    for i in range(len(values) - 3):
        isEqual = True
        k=0
        for j in range(i, i + 3):
            if values[j] == '0' or values[j] != values[j + 1]:
                isEqual = False
                break
            k+=1
        if isEqual: 
            winner=values[k-1]
            return True
    return False

def isConsecutiveFour(values):
    numberOfRows = len(values)
    numberOfColumns = len(values[0])
    # Check rows
    for i in range(numberOfRows):
        if checkIsConsecutiveFourInList(values[i]):
            return True
    
    
    # Check for columns 
    for j in range(numberOfColumns):
        column = numberOfRows * ['0']
        # Get a column into an array
        for i in range(numberOfRows):
            column[i] = values[i][j]
        
        if checkIsConsecutiveFourInList(column):
            return True
    # Check major diagonal (lower part)
    for i in range(numberOfRows - 3):
        numberOfElementsInDiagonal = min(numberOfRows - i, numberOfColumns)
        diagonal = numberOfElementsInDiagonal * ['0']
        for k in range(numberOfElementsInDiagonal):
            diagonal[k] = values[k + i][k]
        if checkIsConsecutiveFourInList(diagonal):
            return True
    # Check major diagonal (upper part)
    for j in range(1, numberOfColumns - 3):
        numberOfElementsInDiagonal = min(numberOfColumns - j, numberOfRows)
        diagonal = numberOfElementsInDiagonal * ['0']
        for k in range(numberOfElementsInDiagonal):
            diagonal[k] = values[k][k + j]
            if checkIsConsecutiveFourInList(diagonal):
                return True
    # Check sub-diagonal (left part)
    for j in range(3, numberOfColumns):
        numberOfElementsInDiagonal = min(j + 1, numberOfRows)
        diagonal = numberOfElementsInDiagonal * ['0']
        for k in range(numberOfElementsInDiagonal):
            diagonal[k] = values[k][j - k]
            if checkIsConsecutiveFourInList(diagonal):
                return True
    # Check sub-diagonal (right part)
    for i in range(1, numberOfRows - 3):
        numberOfElementsInDiagonal = min(numberOfRows - i, numberOfColumns)
        diagonal = numberOfElementsInDiagonal * ['0']
        for k in range(numberOfElementsInDiagonal):
            diagonal[k] = values[k + i][numberOfColumns - k - 1]
            if checkIsConsecutiveFourInList(diagonal):
                return True
    return False



val=[['1','0','1','1','1'],
     ['0','2','2','2','2'],
     ['1','1','1','0','0'],
     ['1','1','0','0','0'],
     ['1','0','0','0','0']]
        

print(isConsecutiveFour(val))
'''
cols=6
rows=4
data=['0']*rows
for i in range(rows):
    data[i]=['0']*cols
print(data)
'''