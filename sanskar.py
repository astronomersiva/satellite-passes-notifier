from itertools import chain, combinations
import collections
def powerset(s):
  return chain.from_iterable( combinations(s,n) for n in range(len(s)+1) )
def anydup(thelist):
  seen = set()
  for x in thelist:
    if x in seen: return False
    seen.add(x)
  return True
T = int(raw_input())
for t in xrange(T):
    N, K = map(int, raw_input().split())
    A = map(int, raw_input().split())
    v = collections.defaultdict(list)
    sumDic = {}
    for subset in powerset(A):
        s = sum(subset)
        sumDic[(subset)] = s
    keys = sumDic.keys()
    for x in keys:
        temp = sumDic[x]
    for key, value in sorted(sumDic.iteritems()):
        v.setdefault(value, []).append(key)
    t = 0
    for sumOf, subsets in v.items():
      #print sumOf, subsets
      flag = False
      if len(subsets) == K:
        place = list(chain(*subsets))
        flag = anydup(place)
        #print flag
      if flag == True:
        print 'yes'
        t = 1
        break
    if t == 0:
      print 'no'
        
              
          
            
                
