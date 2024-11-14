# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 21:06:42 2023

@author: Mohammad
"""
def modify(filename1,filename2):
    with open(filename1) as f:
        a = f.readlines()
        dele = []
        for i in range(len(a)):
            if 'bonds' in a[i]:
                beg = i+1
            if 'angles' in a[i]:
                end = i
                
        for i in range(beg,end):
            if a[i].split()[3] == '0.064' and a[i].split()[4] == '90000':
                dele.append([int(a[i].split()[0]),int(a[i].split()[1])])
                
    with open(filename2) as f:
        b = f.readlines()
    
    for i in range(len(dele)):
        a[dele[i][0]+2] = a[dele[i][0]+2][:32] + 'PARM ' + a[dele[i][0]+2][37:]
        b[dele[i][0]+1] = b[dele[i][0]+1][:10] + ' PARM' + b[dele[i][0]+1][15:]
    for i in range(len(dele)):
        a[dele[i][1]+2] = a[dele[i][1]+2][:32] + 'DEL  ' + a[dele[i][1]+2][37:]
        b[dele[i][1]+1] = b[dele[i][1]+1][:10] + '  DEL' + b[dele[i][1]+1][15:]
    
    with open(filename1, 'w') as f:
        for i in a:
            f.write(i)
    with open(filename2, 'w') as f:
        for i in b:
            f.write(i)

if __name__ == '__main__':
    import sys
    filename1 = sys.argv[1]
    filename2 = sys.argv[2]
    modify(filename1,filename2)