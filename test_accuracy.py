with open('accuracy.txt', 'r') as f:
    mylist = [float(x) for x in f.readline().split(',') if x != '']
    print(sum(mylist)/len(mylist))