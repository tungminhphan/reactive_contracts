if __name__ == '__main__':
    from compute_realizability import *
else:
    from contracts.compute_realizability import *

if len(sys.argv) > 2:
    i = int(sys.argv[1])
    j = int(sys.argv[2])
    synthesize_by_ij(i,j)
elif sys.argv[1] == 'all':
    check_all()
else:
    print('Nothing happened')
