
import time

from general_utility.util import *

def parse_MRT(directory=r'D:\2021_ICARUS_dev\data\enviroment\MRT Data\MRT',
              parsing_type='class'):  # parse MRT requires 17-20 minutes
    mrts = {}
    # read MRT files as DataFrame, then merge.
    start = time.time()
    csvfiles = read_files_in_dir(directory)
    
    in_df = pd.read_csv(csvfiles[0], usecols=[' MRT', ' Time'])
    t_name = functions.get_time(in_df[' Time'][0])
    time_column = [t_name]

    in_df = in_df[[' MRT']].rename(columns={" MRT": t_name}, inplace=False)  # change dataframe field name.
    for csvfile in csvfiles[1:]:
        temp_df = pd.read_csv(csvfile, usecols=[' Time', ' MRT'])
        t_name = functions.get_time(temp_df[' Time'][0])
        time_column.append(t_name)
        in_df[t_name] = temp_df[' MRT']

        del temp_df
    in_df['MRT'] = in_df[time_column].to_dict(orient='records')
    in_df = in_df.drop(columns=time_column)
    in_df.index.name = 'idx'
    in_df = in_df.reset_index()
    # load GSV
    for idx, mrt in zip(*[in_df[col] for col in in_df]):
        if parsing_type == 'array':  # save most of the RAM space
            mrts[idx] = dict_array(mrt)
        elif parsing_type == 'dictionary':
            mrts[idx] = mrt
        elif parsing_type == 'collection':
            mrts[idx] = get_collection(mrt)
        elif parsing_type == 'class':
            mrts[idx] = MRT(mrt)
        elif parsing_type == 'pd_series':  # don't use
            mrts[idx] = pd.Series(mrt)
        else:
            print(f'{parsing_type} is not valid')
            exit
    # load MRT temperature
    del in_df
    print(time.time() - start)
    return mrts