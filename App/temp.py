#temp
import config


with open(config.data_dir+'201801-1-citibike-tripdata.csv') as r:
    liste = []
    l = list(r)
    for idline in range(1, len(l)):
        alb = zip(l[0].split(','),l[idline].split(','))
        for k,v in alb:
            if "start station id" in k: liste.append(v)
            if "end station id" in k: liste.append(v)

    print(len(set(liste)))