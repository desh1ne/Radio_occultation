import numpy as np
import pandas as pd

def parse_rocc(path_file):
    with open(path_file, 'r') as file:
        # skip date loading
        next(file)

        # read date observation
        raw_line = file.readline().split()
        date_observation = raw_line[2].replace('/', '_')
        num_obsr = int(raw_line[-1])

        # skip comment
        next(file), next(file)

        # read statistics    
        def create_stat_df(names_colm, names_rows):            
            result = pd.DataFrame(columns = names_colm)
            for name in names_rows:
                if (name == 'Pmax') or (name == 'CutOff'):
                    result.loc[name] = list(map(int, file.readline().split()[2:]))
                    continue

                result.loc[name] = list(map(int, file.readline().split()[1:]))

            return result

        names_colm = ('Sum', *list(map(lambda x: 'h' + str(x), range(24))))
        names_rows = ['Total', 'LessLevel', 'Between', 'MoreLevel', 'Retreiv', 'Ion.cor', 'Pmax', 'CutOff']

        stat = create_stat_df(names_colm, names_rows)

        # skip comment
        next(file)

        # read Geo Graph
        def create_graph_df(names_colm, names_rows):
            result = pd.DataFrame(columns = names_colm)
            for name in names_rows:
                result.loc[name] = list(map(int, file.readline().split()[1:]))

            return result

        names_colm = ('Sum', *range(18))
        names_rows = ['LAT_G', 'LAT_B', 'LAT_R']

        geo_graph = create_graph_df(names_colm, names_rows)

        # skip comment
        next(file)

        #read coordinates
        def create_coord_df(num_rows, names_colm):
            result = pd.DataFrame(np.zeros((num_rows, len(names_colm))), columns = names_colm)
            #result = pd.DataFrame(columns = names_colm)

            count = 0
            for line in file:
                raw_colm = line.split()
                result.loc[count] = raw_colm[:(len(names_colm) - 1)] + [' '.join(raw_colm[(len(names_colm) - 1):])]
                count += 1

            return result

        names_colm = file.readline().split()
        coord_df = create_coord_df(num_obsr, names_colm)

    return (stat, geo_graph, coord_df, date_observation)


def parse_hurricane(path_file):
    with open(path_file, 'r') as file:
        # skip date loading
        next(file), next(file)

        # read statistics    
        def create_hurr_df(names_colm):            
            result = pd.DataFrame(columns = names_colm)
            
            count = 0
            for line in file:
                line = line.split()
                result.loc[count] = line[:6] + [' '.join(line[6:])]
                count += 1
                
            return result

        names_colm = file.readline().split()
        hurr_df = create_hurr_df(names_colm)

    return hurr_df
