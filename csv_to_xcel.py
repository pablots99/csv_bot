import pandas as pd
import os, fnmatch
import sys


def find(pattern, path):
    result = []
    if(os.path.exists("combined_csv.csv")):
        result.append("combined_csv.csv")
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

def joincsv(downloads_path,output_path):
    output_path = output_path + "/combined_csv.csv"
    paths = find('results*.csv', downloads_path)
    out = 0
    if(paths):
        #combine all files in the list
        combined_csv = pd.concat([pd.read_csv(f) for f in paths]).drop_duplicates(keep='first')
        #export to csv
        combined_csv.to_csv( output_path, index=False, encoding='utf-8-sig')
        for f in paths:
            if(f != output_path):
                os.remove(f)
            else:
                out = 1
    if(out == 1):  
        print("Nothing to import")


