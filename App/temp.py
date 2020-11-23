#temp
import config

"""with open(config.data_dir+'201801-1-citibike-tripdata-small.csv') as r:
    l = list(r)
    for idline in range(1, len(l)):
        for k,v in zip(l[0].split(','),l[idline].split(',')):
            k = k[:-1] if k.endswith('\n') else k
            v = v[:-1] if v.endswith('\n') else v
            if ('start station' in k or 'end station' in k) and (' latitude' not in k and ' longitude' not in k):
                print(f'{k}><{v}', end=',')
        print()"""

minimum = float('inf')
maximum = float('-inf')

print(minimum, maximum)

print(9>1)
