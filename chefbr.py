from itertools import chain, combinations

def powerset(s):
  return chain.from_iterable( combinations(s,n) for n in range(len(s)+1) )

N = int(raw_input())
A = map(int, raw_input().split())
count = 0
for subset in powerset(A):
    current = list(subset)
    for element in range(len(subset) - 2):
       print current[element], current[element + 1] 
