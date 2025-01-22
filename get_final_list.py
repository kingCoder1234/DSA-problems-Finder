import re
import os


def make_file(arr) :
    file_path = "clean_problems.txt"
    with open(file_path, 'a' if os.path.exists(file_path) else 'w') as file:
        for link in arr:
            file.write(link + "\n")
        file.close()




def removeele(a,p) :
    ans = []
    for ele in a :
        if p not in ele :
            ans.append(ele)
        else :
            print("Removed this : " + ele)
    return ans



file_path = "problems.txt"

with open(file_path, 'r') as file:
    content = file.readlines()
my_ans = [line.strip() for line in content]


my_ans = removeele(my_ans,"/solution")
my_ans = list(set(my_ans))


make_file(my_ans)
