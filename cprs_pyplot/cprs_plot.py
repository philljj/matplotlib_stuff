import numpy as np
import matplotlib.pyplot as plt
import itertools

# global vars

# compression test filesize in MB
input_file_size=19.0
title="my 19 MB binary test file, release build"

# plot colors to cycle through
c_colors = itertools.cycle(["r", "b", "g", "y"])
d_colors = itertools.cycle(["r", "b", "g", "y"])

cprs_list = ['brotli', 'zlib', 'bzip', 'lzma']
#blk_list = ['12', '16']
blk_list = ['16']
#blk_list = []

# Whether to connect scatter points with line
plot_line = False

# functions

def str_to_ratio(str):
  c_percent = float(str)
  ratio = 100.0 / (100.0 - c_percent)
  return ratio

def str_to_mbs(str):
  time = float(str)
  speed = input_file_size / time
  return speed

def load_data(file, c_speed, c_ratio, d_speed):
 # After parsing, file is organized in columns:
 #   <method> <compression time> <compression %> <decompression time>
 #
 # Convert this to speed in MB/s and compression ratio.

 with open(file) as f:
  lines = f.readlines()

  for line in lines:
    line = line.split(' ')

    c_speed.append(str_to_mbs(line[1]))
    c_ratio.append(str_to_ratio(line[2]))
    d_speed.append(str_to_mbs(line[3]))

  return

def load_subplot(axarr, label):
  file = "data/" + label + ".txt"

  c_speed = []
  c_ratio = []
  d_speed = []
  
  load_data(file, c_speed, c_ratio, d_speed)
  
  x = c_ratio
  y = c_speed
  z = d_speed

  label = label + "MB"
  
  axarr[0].scatter(x, y, label=label, color=next(c_colors))
  axarr[0].set_ylabel('compression speed (MB/s)')
  axarr[0].margins(0.07)

  axarr[1].scatter(x, z, label=label, color=next(d_colors))
  axarr[1].set_xlabel('compression ratio')
  axarr[1].set_ylabel('decompression speed (MB/s)')
  axarr[1].legend()
  axarr[1].margins(0.07)

  if plot_line:
    axarr[0].plot(x, y, color="black")
    axarr[1].plot(x, z, color="black")

  return

# Now do work finally.

fig, axarr = plt.subplots(2, sharex=True)

for cprs in cprs_list:
  if not blk_list:
    label = cprs
    load_subplot(axarr, label)

  else:
    for blk in blk_list:
      plot_line = True
      label = cprs + "_" + blk
      load_subplot(axarr, label)
    
plt.suptitle(title, fontsize=14)
plt.show()
