# -*- coding: iso-8859-1 -*-
##############################
# Author: Te-Yuan Liu
##############################

##############################
# Import library
##############################
import numpy as np
import re
import time
##############################
# Define function
##############################
def mergetxt(fnames):
    with open("merged.txt", "w", encoding="ISO-8859-1") as outfile:
        for fname in fnames:
            with open(fname, encoding="ISO-8859-1") as infile:
                for line in infile:
                    outfile.write(line)
def readtxt_write_edgelist(fname):
    start = time.time()
    cast_movie_dict = {}
    movie_cast_dict = {}
    line_count = 0
    cast_count = 0
    with open(fname, encoding="ISO-8859-1") as fin:
        for line in fin:
            line_count += 1
            obj_list = re.split(r"\t+", line) ############# change to \t
            if len(obj_list) < 11: ############### change to 11 later
                continue
            cast_count += 1
            strip_list = []
            for obj in obj_list:
                strip_list.append(obj.strip("\n").strip())
            strip_list = list(filter(None, strip_list))
            obj_count = 0
            cast_name = strip_list[0]
            new_movie_list = []
            cast_movie_dict[cast_name] = new_movie_list
            for obj in strip_list:
                obj_count += 1
                if obj_count >= 2:
                    p1 = re.search(r"\((\d{4}|\?{4})[^()]*\)(.+)", obj)
                    if p1:
                        obj = obj.replace(p1.group(2),'')
                        ## movie 2 cast dict update
                        if movie_cast_dict.get(obj) == None:
                            new_cast_list = []
                            new_cast_list.append(cast_name)
                            movie_cast_dict[obj] = new_cast_list
                        else:
                            movie_cast_dict[obj].append(cast_name)
                        ## cast 2 movie dict update
                        cast_movie_dict[cast_name].append(obj)
                    else:
                        p2 = re.search(r"\((\d{4}|\?{4})[^()]*\)", obj)
                        if not p2:
                            obj = obj + " (????)"
                        # movie 2 cast dict update
                        if movie_cast_dict.get(obj) == None:
                            new_cast_list = []
                            new_cast_list.append(cast_name)
                            movie_cast_dict[obj] = new_cast_list
                        else:
                            movie_cast_dict[obj].append(cast_name)
                        ## cast 2 movie dict update
                        cast_movie_dict[cast_name].append(obj)
    print("There are ",cast_count," actors/actresses and ",len(movie_cast_dict)," unique movies...")
    #print(dict(list(movie_cast_dict.items())[:]))
    #print("/////////////////////////////")
    #print(dict(list(cast_movie_dict.items())[:]))
    #print("/////////////////////////////")
    
    ## create edge list for actor/actress network
    edgelist_dict = {}
    for c1, ml in cast_movie_dict.items():
        for m in ml:
            for c2 in movie_cast_dict[m]:
                if c1 != c2:
                    key = c1 + "\n" + c2
                    if edgelist_dict.get(key) == None:
                        edgelist_dict[key] = 1.0/len(ml)
                    else:
                        edgelist_dict[key] += 1.0/len(ml)
    #print(dict(list(edgelist_dict.items())[:]))
    with open("cast_network_edgelist.csv", "w", encoding="utf-8") as outfile:
        for k, v in edgelist_dict.items():
            c1, c2 = k.split("\n")
            line = ",".join(["\""+c1+"\"", "\""+c2+"\"", str(v)]) + "\n"
            outfile.write(line)
    
    ## create edge list for movie network
    trim_movie_cast_dict = {}
    trim_cast_movie_dict = {}
    edgelist_dict = {}
    for m, cl in movie_cast_dict.items():
        if len(cl) < 5: ############## change to 5
            continue
        trim_movie_cast_dict[m] = cl
    for m, cl in trim_movie_cast_dict.items():
        for c in cl:
            if trim_cast_movie_dict.get(c) == None:
                new_movie_list = []
                new_movie_list.append(m)
                trim_cast_movie_dict[c] = new_movie_list
            else:
                trim_cast_movie_dict[c].append(m)
                
    for m1, cl1 in trim_movie_cast_dict.items():
        for c in cl1:
            for m2 in trim_cast_movie_dict[c]:
                if m1 != m2:
                    cl2 = movie_cast_dict[m2]
                    cast_union_count = len(list(set(cl1) | set(cl2)))
                    key1 = m1 + "\n" + m2
                    key2 = m2 + "\n" + m1
                    if edgelist_dict.get(key1) == None and edgelist_dict.get(key2) == None:
                        edgelist_dict[key1] = 1.0/cast_union_count
                    elif edgelist_dict.get(key1) != None and edgelist_dict.get(key2) == None:
                        edgelist_dict[key1] += 1.0/cast_union_count
                    elif edgelist_dict.get(key1) == None and edgelist_dict.get(key2) != None:
                        edgelist_dict[key2] += 1.0/cast_union_count
                    else:
                        print("*******error: ",edgelist_dict)
                        return
    with open("movie_network_edgelist.csv", "w", encoding="utf-8") as outfile:
        for k, v in edgelist_dict.items():
            m1, m2 = k.split("\n")
            line = ",".join(["\""+m1+"\"", "\""+m2+"\"", str(v/2)]) + "\n"
            outfile.write(line)
    
    end = time.time()
    print("runtime: " + str(end - start))

##############################
# Main function
##############################
def main():
    # run the two below lines of code for creation of merged.txt
    file_names = ["actor_movies.txt", "actress_movies.txt"]
    mergetxt(file_names)
    print("hello" + " world...")
    readtxt_write_edgelist("merged.txt")
if __name__ == "__main__":
    main()
