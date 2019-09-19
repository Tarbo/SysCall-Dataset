"""
@author: Okwudili Ezeme
@date: 2019-09-19
A function to generate the processed data from the raw dataset
"""
import os 
import pandas as pd


base_path = "..data/raw-dataset/" # use your full system path to avoid errors
file_name_normal = "001_NORMAL_Flight.txt"
file_name_delay = "002_BUSYDELAY_Flight.txt"
file_name_socket = "003_SOCKETS_Flight.txt"



# only the timestamp, "syscal" and RAX attributes are loaded
normal_df = pd.read_csv(os.path.join(base_path,file_name_normal),header=None,
                        names=['timestamp','SYSCALL','RAX'],usecols=[0,1,2])
delay_df = pd.read_csv(os.path.join(base_path,file_name_delay),header=None,
                        names=['timestamp','SYSCALL','RAX'],usecols=[0,1,2])
random_df = pd.read_csv(os.path.join(base_path,file_name_socket),header=None,
                        names=['timestamp','SYSCALL','RAX'],usecols=[0,1,2])

# drop the ROWS with NaN values because they contain just process page pointer which we dont need
normal_df = normal_df.dropna(axis=0,inplace=False)
delay_df = delay_df.dropna(axis=0,inplace=False)
random_df = random_df.dropna(axis=0,inplace=False)

# drop the SYSCALL column as it is not needed in our experiment
normal_df = normal_df.drop('SYSCALL',axis=1,inplace=False)
delay_df = delay_df.drop('SYSCALL',axis=1,inplace=False)
random_df = random_df.drop('SYSCALL',axis=1,inplace=False)

# convert the system call hex values to integers using linux system call table as a guide
normal_df['RAX'] = normal_df.RAX.apply(lambda x: int(x,16))
delay_df['RAX'] = delay_df.RAX.apply(lambda x: int(x,16))
random_df['RAX'] = random_df.RAX.apply(lambda x: int(x,16))

# find the difference in execution time via the timestamp feature
dfs = [normal_df,delay_df,random_df]
for df in dfs:
    df['timestamp'] = df['timestamp'].diff(periods=1).fillna(0)
    df['RAX'] = df['RAX'].add(1) # add 1 to remove zero ID

# Save the timestamp and RAX to csv
normal_df.to_csv('normal1.csv',columns=['timestamp','RAX'],index=False,header=False)
delay_df.to_csv('delay1.csv',columns=['timestamp','RAX'],index=False,header=False)
random_df.to_csv('random1.csv',columns=['timestamp','RAX'],index=False,header=False)
