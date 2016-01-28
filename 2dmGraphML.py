import numpy as np
#set workspace
myworkspace = "D:/temp"

#set the name of the .2dm file (mesh-file for BASEMENT-ETH flood simulation model)
meshfilename = "testgraphml.2dm"

#set the name of the output file
outputfilename = "out.graphml"
outputfilefullname = myworkspace+"/"+outputfilename

#parse the mesh and fill the nodes-array with x,y,z of nodes and triangles-list
mesh = open(myworkspace+"/"+meshfilename, "r")
countnodes = 0
counttriangles = 0
countedges = 0
nodeslist = []
triangleslist = []
edgeslist = []
templist = []
temptrianglelist = []
print "importing the mesh "+str(meshfilename)+" ..."

#loop through all nodes and triangles in the .2dm mesh file
for line in mesh:
    tokens = line.strip().split()
    if tokens[0] == 'ND':
        nodeslist.append(tokens[1:5])
        countnodes += 1
    if tokens[0] == 'E3T':
        triangleslist.append(tokens[1:5])
        counttriangles += 1
print "mesh file "+str(meshfilename)+" imported ..."
print "number of imported nodes in mesh: "+str(countnodes)
print "number of imported triangles in mesh: "+str(counttriangles)
mesh.close()

#create an array for the nodes and their attributes (id, x, y, z)
nodesarray = np.zeros((countnodes, 4), dtype=np.float32)
linenumber=0
for node in nodeslist:
    nodesarray[linenumber,0]=float(node[0])
    nodesarray[linenumber,1]=float(node[1])
    nodesarray[linenumber,2]=float(node[2])
    nodesarray[linenumber,3]=float(node[3])
    linenumber += 1
nodeslist = []

#create an array for the triangles
trianglesarray = np.zeros((counttriangles, 4), dtype=np.int)
linenumber=0
for triangle in triangleslist:
    trianglesarray[linenumber,0]=int(triangle[0])
    trianglesarray[linenumber,1]=int(triangle[1])
    trianglesarray[linenumber,2]=int(triangle[2])
    trianglesarray[linenumber,3]=int(triangle[3])
    linenumber += 1

#create and open the output file
outputfile = open(outputfilefullname, "w")
#write the BMG header file
outputfile.write('<?xml version="1.0" encoding="UTF-8"?>' + '\n')
outputfile.write('<graphml xmlns="http://graphml.graphdrawing.org/xmlns"'+ '\n')
outputfile.write('    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'+ '\n')
outputfile.write('    xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns'+ '\n')
outputfile.write('     http://graphml.graphdrawing.org/xmlns/1.0/graphml.xsd">'+ '\n')
outputfile.write('<key id="x" attr.name="x" attr.type="double" for="node" />'+ '\n')
outputfile.write('<key id="y" attr.name="y" attr.type="double" for="node" />'+ '\n')
#outputfile.write('<key id="z" for="node" attr.name="z" attr.type="double" /key>'+ '\n')
outputfile.write('<graph edgedefault="undirected">'+ '\n')

#loop through the nodes-array and write the attributes to the graphml file
i = 0
while i < countnodes:
    outputfile.write('<node id="' + str(int(nodesarray[i,0])) + '">' + '\n')
    outputfile.write('    <data key="x">' + str(nodesarray[i,1]) + '</data>' + '\n')
    outputfile.write('    <data key="y">' + str(nodesarray[i,2]) + '</data>' + '\n')
    outputfile.write('</node>'+ '\n')
    i += 1

#loop through the triangles-array and write the edges
j = 0
while j < counttriangles:
    outputfile.write('<edge source="' + str(int(trianglesarray[j,1])) + '" target="'+str(int(trianglesarray[j,2])) +'">' + '\n')
    outputfile.write('</edge>'+ '\n')
    outputfile.write('<edge source="' + str(int(trianglesarray[j,1])) + '" target="'+str(int(trianglesarray[j,3])) +'">' + '\n')
    outputfile.write('</edge>'+ '\n')
    outputfile.write('<edge source="' + str(int(trianglesarray[j,2])) + '" target="'+str(int(trianglesarray[j,3])) +'">' + '\n')
    outputfile.write('</edge>'+ '\n')
    j += 1

outputfile.write('</graph>' + '\n')
outputfile.write('</graphml>' + '\n')
outputfile.close()
print "output written .."


