import pandas as pd
import sys

# enter csv file directory as first arg then enter directory where you want reynold number stored then enter pressure drop
file_name = sys.argv[1]
RE_dir = sys.argv[2]
df = pd.read_csv(file_name)

channel_height = 0.02

u_sum = 0

start_index = 1
#end_index = 
slice_df = df.iloc[start_index:]

#right riemann sum
prev_x = 0
for i, j in slice_df.iterrows():
    u_sum += j.iloc[10] * (j.iloc[1] - prev_x)
    prev_x = j.iloc[1]

avg_u = u_sum/channel_height

characteristic_length = 0.01

viscosity = 8.9e-7

reynolds = avg_u * characteristic_length / viscosity

with open(RE_dir, "w+") as file1:
    file1.write(str(reynolds) + "\n" + sys.argv[3])





