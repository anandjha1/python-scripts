import csv

with open('extracted.txt', 'r') as txt_file:
    res = txt_file.read()


resList = res.split('#--#')

with open('result', 'w') as file:
    write = csv.writer(file)

    write.writerow(resList)