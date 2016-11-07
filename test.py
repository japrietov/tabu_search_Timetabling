import itertools
list1=[1,2,3]
list2=[1,2]
print [zip(x,list2) for x in itertools.permutations(list1,len(list2))]