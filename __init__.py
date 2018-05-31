import sys

def Q1(input):
    if input[0] == 1:
        return Q3(input)
    else:
        return False

def Q3(input):
    if (input[1] == 1 and input[2] == 1):
        return False
    elif (input[1] == 1 and input[2] == 0):
        return Q4(input)
    elif (input[1] == 0 and input[2] == 1):
        return Q4(input)
    else:
        return False
        
def Q4(input):
    if input[3] == 1:
        return Q5(input)
    else:
        return False

def Q5(input):
    if input[4] == 1:
        return True
    else:
        return False

def decisionTree(input):
    isChanged = Q1(input)
    return isChanged

def main():
    n = 5
    print("Input")
    with open('question.input', 'r') as f:
        input = [int(line[0]) for line in f]
    with open('question.input', 'r') as f:    
        for line in f:
            answer = "Yes"
            if int(line[0]) == 0:
                answer = "No"
            print(line[2:], answer)
    result = decisionTree(input)
    print("Output")
    if result == True:
        print("Opinion Changed!")
    else:
        print("Nah, Opinion NOT changed")

if __name__ == "__main__":
    main()

