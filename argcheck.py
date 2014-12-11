import sys
import collections
arg_names = ['arg0','directory', 'indentation', 'newLine']
args = dict(zip(arg_names, sys.argv))
Arg_list = collections.namedtuple('Arg_list', arg_names)
args = Arg_list(*(args.get(arg, None) for arg in arg_names))
print args[0]
