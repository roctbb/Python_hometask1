import sys
import csv
import xml.dom.minidom
import time
start = time.time()
dom = xml.dom.minidom.parse(sys.argv[1])
alist = dom.getElementsByTagName('net')
nodesnum = len(alist)
matrix = [[float('inf') for j in range(nodesnum)] for i in range(nodesnum)]
for i in range(nodesnum):
    matrix[i][i] = 0
rlist = dom.getElementsByTagName('resistor')
for node in rlist:
    fr = int(node.getAttribute("net_from"))-1
    to = int(node.getAttribute("net_to"))-1
    resis = float(node.getAttribute("resistance"))
    matrix[fr][to] = 1/(1/matrix[fr][to]+1/resis)
    matrix[to][fr] = 1/(1/matrix[to][fr]+1/resis)
rlist = dom.getElementsByTagName('capactor')
for node in rlist:
    fr = int(node.getAttribute("net_from"))-1
    to = int(node.getAttribute("net_to"))-1
    resis = float(node.getAttribute("resistance"))
    matrix[fr][to] = 1/(1/matrix[fr][to]+1/resis)
    matrix[to][fr] = 1/(1/matrix[to][fr]+1/resis)
rlist = dom.getElementsByTagName('diode')
for node in rlist:
    fr = int(node.getAttribute("net_from"))-1
    to = int(node.getAttribute("net_to"))-1
    resis = float(node.getAttribute("resistance"))
    revres = float(node.getAttribute("reverse_resistance"))
    matrix[fr][to] = 1/(1/matrix[fr][to]+1/resis)
    matrix[to][fr] = 1/(1/matrix[to][fr]+1/revres)
for k in range(nodesnum):
    for i in range(nodesnum):
        for j in range(nodesnum):
            if i != j:
                if matrix[i][j] == 0:
                    a = float('inf')
                else:
                    a = 1/matrix[i][j]
                if matrix[i][k]+matrix[k][j] == 0:
                    b = float('inf')
                else:
                    b = 1/(matrix[i][k]+matrix[k][j])
                if a+b == 0:
                    matrix[i][j] = float('inf')
                else:
                    matrix[i][j] = 1/(a+b)
wr = csv.writer(open(sys.argv[2], "w"), delimiter=',')
for row in matrix:
    wr.writerow(row)
finish = time.time()
print (finish - start)
