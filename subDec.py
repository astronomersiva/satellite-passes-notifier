from itertools import chain, combinations

def powerset(s):
  return chain.from_iterable( combinations(s,n) for n in range(len(s)+1) )

T = int(raw_input())
for t in xrange(T):
    N, K = map(int, raw_input().split())
    A = map(int, raw_input().split())
    maxF = 0
    for subset in powerset(A):
        print subset
        exOr = 0
        if len(subset) != 0:
            for element in subset:
                exOr ^= element
        print K ^ exOr
        if K ^ exOr > maxF:
            maxF = K ^ exOr
            #print maxF
    #print maxF
    
