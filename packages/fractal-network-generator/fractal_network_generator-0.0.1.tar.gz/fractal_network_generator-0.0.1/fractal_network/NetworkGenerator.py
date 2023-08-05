#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 10 20:05:18 2021

@author: royc1
"""

coordMap={}
nodesList={}
nodesList1={}
neighsList={}
edgesList={}

def makeGraph(levels,nu):
    
    nodes=nu**levels
    for i in range(nodes):
        coord=()
        Ind=i
        coordcnt=10**(levels)
        for l in range(levels):
            indx=Ind%nu
            Ind=Ind/nu
            coord=coord+(int(indx),)
            neighsList[i]=set()
            coordcnt=coordcnt+(indx)*10**(levels-l-1)
#			coordcnt=coordcnt+(10+indx)*100**(levels-l-1)
            nodesList1[i]=coordcnt
            nodesList[i]=coord
            coordMap[coord]=i
#		print i,coord,coordcnt
    for i in nodesList.keys():
        coord = nodesList[i]
        for j in range(1,nu):
            coordJ=(int((coord[0]+j)%nu),)
            for k in range(1,len(coord)):
                coordJ=coordJ+(int(coord[k]),)
                J=coordMap[coordJ]
#			edgesList[(i,J)]=a
#			edgesList[(J,i)]=a
            edgesList[(i,J)]=1
            edgesList[(J,i)]=1
            neighsList[i].add(J)        
            neighsList[J].add(i)        
        if (coord[0]!=coord[1]):
            coordJ=(coord[1],coord[0])
            for k in range(2,len(coord)):
                coordJ=coordJ+(coord[k],)
            J=coordMap[coordJ]
#		    edgesList[(i,J)]=a*r
#			edgesList[(J,i)]=a*r
            edgesList[(i,J)]=2
            edgesList[(J,i)]=2
            neighsList[i].add(J)        
        else:
            J=coord[0]
            cnt=1
            for j in range(len(coord)-1):
                if(coord[j+1]!=J):
                    break
                cnt=cnt+1
            coordJ=()
            if (cnt!=len(coord)):
                for j in range(cnt):
                    coordJ=coordJ+(coord[cnt],)            
                coordJ=coordJ+(coord[0],)
                for j in range(cnt+1,len(coord)):
                    coordJ=coordJ+(coord[j],)            
                J=coordMap[coordJ]
                edgesList[(i,J)]=cnt+1
                edgesList[(J,i)]=cnt+1
#				edgesList[(i,J)]=a*(r**cnt)
#				edgesList[(J,i)]=a*(r**cnt)
                neighsList[i].add(J)        
                neighsList[J].add(i)        
                
                
def graph(lvls,n):
    #coordMap={}
    #nodesList={}
    #neighsList={}
    #edgesList={}
    makeGraph(lvls,n)
    with open(str(n)+"-"+str(lvls)+".dat","w") as f:
        for i in nodesList1:
            f.write(str(i)+" "+str(int(nodesList1[i]))+" "+str(len(neighsList[i])))
            for j in neighsList[i]:
                f.write(" "+str(j)+" "+str(edgesList[(i,j)]))
            f.write("\n")

