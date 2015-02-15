import sys
import xml.dom.minidom
from xml.dom.minidom import Node
dom = xml.dom.minidom.parse(sys.argv[0])
Topic=dom.getElementsByTagName('Topic')
i = 0
for node in Topic:
    alist=node.getElementsByTagName('Title')
    for a in alist:
        Title= a.firstChild.data
        print Title