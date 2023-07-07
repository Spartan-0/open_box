if __name__ == '__main__':
    students=[]
    final=[]
    for _ in range(int(input())):
        name = input()
        score = float(input())
        students.append([name,score])
    students = sorted(students,key = lambda x: (x[1],x[0]))
    min_score = min(students,key = lambda x: (x[1],x[0]))
    min_score  = min_score[1]
    for i in students:
        if i[1] == min_score:
            #print("Min score:" ,min_score)
            #print(i[1])
            continue
        else:
            final.append(i)
    #print(final)
    mins = min(final,key = lambda x: (x[1],x[0]))
    mins = mins[1]
    for j in final:
        if j[1] == mins:
            print(j[0])
