import sys
import csv
import xml.dom.minidom
from xml.dom.minidom import Node
print(sys.argv[1])
dom = xml.dom.minidom.parse(sys.argv[1])
alist=dom.getElementsByTagName('net')
nodesnum = len(alist);

matrix = [[float ('inf') for j in range(nodesnum)] for i in range(nodesnum)]

for i in range(nodesnum):
    matrix[i][i] = 0

rlist=dom.getElementsByTagName('resistor')

for node in rlist:
    matrix[int(node.attributes["net_from"].nodeValue)-1][int(node.attributes["net_to"].nodeValue)-1]= 1/(1/matrix[int(node.attributes["net_from"].nodeValue)-1][int(node.attributes["net_to"].nodeValue)-1]+1/float(node.attributes["resistance"].nodeValue) )
    matrix[int(node.attributes["net_to"].nodeValue)-1][int(node.attributes["net_from"].nodeValue)-1]= 1/(1/matrix[int(node.attributes["net_to"].nodeValue)-1][int(node.attributes["net_from"].nodeValue)-1]+1/float(node.attributes["resistance"].nodeValue) )

rlist=dom.getElementsByTagName('capator')

for node in rlist:
    matrix[int(node.attributes["net_from"].nodeValue)-1][int(node.attributes["net_to"].nodeValue)-1]= 1/(1/matrix[int(node.attributes["net_from"].nodeValue)-1][int(node.attributes["net_to"].nodeValue)-1]+1/float(node.attributes["resistance"].nodeValue) )
    matrix[int(node.attributes["net_to"].nodeValue)-1][int(node.attributes["net_from"].nodeValue)-1]= 1/(1/matrix[int(node.attributes["net_to"].nodeValue)-1][int(node.attributes["net_from"].nodeValue)-1]+1/float(node.attributes["resistance"].nodeValue) )

rlist=dom.getElementsByTagName('diode')

for node in rlist:
    matrix[int(node.attributes["net_from"].nodeValue)-1][int(node.attributes["net_to"].nodeValue)-1]= 1/(1/matrix[int(node.attributes["net_from"].nodeValue)-1][int(node.attributes["net_to"].nodeValue)-1]+1/float(node.attributes["resistance"].nodeValue) )
    matrix[int(node.attributes["net_to"].nodeValue)-1][int(node.attributes["net_from"].nodeValue)-1]= 1/(1/matrix[int(node.attributes["net_to"].nodeValue)-1][int(node.attributes["net_from"].nodeValue)-1]+1/float(node.attributes["reverse_resistance"].nodeValue) )
for k in range(nodesnum):
    for i in range(nodesnum):
        for j in range(nodesnum):
            if matrix[i][j] == 0:
                a=float('inf')
            else:
                a=1/matrix[i][j]
            if matrix[i][k]+matrix[k][j] == 0:
                b=float('inf')
            else:
                b=1/(matrix[i][k]+matrix[k][j])
            if a+b == 0:
                matrix[i][j] = float('inf')
            else:
                matrix[i][j] = 1/(a+b)

print(matrix)
wr = csv.writer(open("test1.csv", "w"), delimiter=';')
for row in matrix:
    wr.writerow(row)