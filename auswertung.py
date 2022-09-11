from globale_Variablen import globale_variablen
import torch
import os
import re

progress_training_path = os.listdir(globale_variablen["path_to_progress"])[-1]
progress_name = os.listdir(globale_variablen["path_to_progress"]+progress_training_path)[2]
progress_dict = torch.load(globale_variablen["path_to_progress"]+progress_training_path+"/"+progress_name)

logs = progress_dict["save_logs"]

pattern = re.compile(r"OUT: (\d)     LABEL: (\d)")


table = [[0 for x in range(3)] for y in range(3)]


for log in logs:
    result = re.search(pattern, log)
    out = result.group(1)
    label = result.group(2)
    #print(out)
    #print(label)
    table[int(label)][int(out)] += 1


print(table)