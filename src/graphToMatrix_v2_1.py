# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 10:08:27 2019

@author: Hushub zhou
"""

# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 13:09:52 2019

@author: Hushub zhou
"""


import heapq #最小堆
import math

def main(car_path,road_path,cross_path,answer_path):
#    car_path = "car.txt"
#    road_path = "road.txt"
#    cross_path = "cross.txt"
#    answer_path = "answer.txt"
    
                
    Road = {} #保存路的信息
    with open(road_path) as road: #读取路
        for ind  in road:
            if ind[0] != "#":
                re = ind.split(",")
                roddID = int(re[0].split("(")[1]) #道路ID
                length = int(re[1]) #道路长度
                speed = int(re[2]) #道路限速
                channel =int(re[3]) #车道数目
                start = int(re[4]) #起点
                to = int(re[5]) #终点
                isDuplex = int(re[6].split(")")[0]) #是否双向
                Road[roddID] = [length,speed,channel,start,to,isDuplex]
    
    
    #将路口信息保存为字典
    crossDict = {}
    with open(cross_path) as cross: #读取路口
        for ind in cross:
            if ind[0] != "#":
                re = ind.split(",")
                crossID = int(re[0].split("(")[1]) #道路ID
                up = int(re[1]) 
                right = int(re[2]) 
                down =int(re[3]) 
                left = int(re[4].split(")")[0]) 
                crossDict[crossID] = [up,right,down,left]
    
    
    #给定一个路口，查找连接道路的车道数乘以速度
    def findchannelMultspeed(roadstartid,roadtoid):
        weight = 0
        x = set(crossDict[roadstartid])
        y = set(crossDict[roadtoid])
        re = max(x.intersection(y))#需排除包含-1的情况
        
        weight_to = 0
        DirectionWeight_to = [1.5,2,1.3,1]
        count = -1 #表示上 右  下 左
        
        for ind  in crossDict[roadtoid]: #循环遍历四个方向
            count += 1
            if ind > 0 and ind != re:
                weight_to += Road[ind][0]*(Road[ind][2])*Road[ind][1]*DirectionWeight_to[count]
                if Road[ind][5] > 0:
                    weight_to += Road[ind][0]*(Road[ind][2])*Road[ind][1]*DirectionWeight_to[count]
        
        weight_start = 0
        DirectionWeight_start = [1.3,1,1.5,2]
        count = -1 #表示上 右  下 左
        
        for ind  in crossDict[roadstartid]: #循环遍历四个方向
            count += 1
            if ind > 0 and ind != re:
                weight_start += Road[ind][0]*(Road[ind][2])*Road[ind][1]*DirectionWeight_start[count]
                if Road[ind][5] > 0:
                    weight_start += Road[ind][0]*(Road[ind][2])*Road[ind][1]*DirectionWeight_start[count]
        
        
        weightother = weight_start + weight_to  #越大越好
        
        weightself = (Road[re][1]*(Road[re][2]))/Road[re][0] #越大越好
        if Road[re][5]:
            weightself += weightself
        
        weight = (weightother-weightself)/weightother + 1/weightself
        
        return weight
    
    def findchannelMultspeed1(roadstartid,roadtoid):
        weight = 0
        x = set(crossDict[roadstartid])
        y = set(crossDict[roadtoid])
        re = max(x.intersection(y))#需排除包含-1的情况
        
        weight_to = 0
        count = -1 #表示上 右  下 左
        
        for ind  in crossDict[roadtoid]: #循环遍历四个方向
            count += 1
            if ind > 0 and ind != re:
                weight_to += Road[ind][0]*(Road[ind][2])*Road[ind][1]
                if Road[ind][5] > 0:
                    weight_to += Road[ind][0]*(Road[ind][2])*Road[ind][1]
        
        weight_start = 0
        count = -1 #表示上 右  下 左
        
        for ind  in crossDict[roadstartid]: #循环遍历四个方向
            count += 1
            if ind > 0 and ind != re:
                weight_start += Road[ind][0]*(Road[ind][2])*Road[ind][1]
                if Road[ind][5] > 0:
                    weight_start += Road[ind][0]*(Road[ind][2])*Road[ind][1]
        
        
        weightother = weight_start + weight_to  #越大越好
        
        weightself = (Road[re][2])*Road[re][1]/Road[re][0] #越大越好
        if Road[re][5]:
            weightself += weightself
        
        weight = 1432/weightother + 1/weightself
        
        return weight
                    
    
    Graph = {}
#    Graph_unidirectional = {} #保存单向的路径
    with open(road_path) as road: #读取路
        for ind  in road:
            if ind[0] != "#":
                re = ind.split(",")
                roddID = int(re[0].split("(")[1]) #道路ID
                length = int(re[1]) #道路长度
                speed = int(re[2]) #道路限速
                channel =int(re[3]) #车道数目
                start = int(re[4]) #起点
                to = int(re[5]) #终点
                isDuplex = int(re[6].split(")")[0]) #是否双向
    
                weight = findchannelMultspeed(start,to)
                
                length = weight
                
                if (start not in Graph):
                    Graph[start] = {}
                    Graph[start][to] = length 
                    if isDuplex:
                        if to not in Graph:
                            Graph[to] = {}
                            Graph[to][start]  = length 
                        else:
                            Graph[to][start]  = length 
                            
                elif (isinstance(Graph[start],dict)):
                    Graph[start][to] = length 
                    if isDuplex:
                        if to not in Graph:
                            Graph[to] = {}
                            Graph[to][start]  = length 
                        else:
                            Graph[to][start]  = length 



    Graph1 = {}
#    Graph1_unidirectional = {} #保存单向的路径
    with open(road_path) as road: #读取路
        for ind  in road:
            if ind[0] != "#":
                re = ind.split(",")
                roddID = int(re[0].split("(")[1]) #道路ID
                length = int(re[1]) #道路长度
                speed = int(re[2]) #道路限速
                channel =int(re[3]) #车道数目
                start = int(re[4]) #起点
                to = int(re[5]) #终点
                isDuplex = int(re[6].split(")")[0]) #是否双向
                
                weight = findchannelMultspeed1(start,to)
                
                length = weight
                
                if (start not in Graph1):
                    Graph1[start] = {}
                    Graph1[start][to] = length 
                    if isDuplex:
                        if to not in Graph1:
                            Graph1[to] = {}
                            Graph1[to][start]  = length 
                        else:
                            Graph1[to][start]  = length 
                            
                elif (isinstance(Graph1[start],dict)):
                    Graph1[start][to] = length 
                    if isDuplex:
                        if to not in Graph1:
                            Graph1[to] = {}
                            Graph1[to][start]  = length 
                        else:
                            Graph1[to][start]  = length 


    ######################################
             
    #根据路径查找道路号
    def findRoad(path):
        results = []                 
        for ind in range(1,len(path)):
            start = path[ind-1]
            end = path[ind]
            x = set(crossDict[start])
            y = set(crossDict[end])
            re = max(x.intersection(y))#需排除包含-1的情况
            results.append(re)
        return results
    
    
    
                           
    def init_distance(graph,s):
        distance={s:0}
        for vertex in graph:
            if vertex!=s:
                distance[vertex]=math.inf
        return distance
    
    def dijkstra(graph,s):
        pqueue=[]
        heapq.heappush(pqueue,(0,s))    
        seen=set()#哈希set
        #
        parent={s:None}
        
        distance=init_distance(graph,s)#距离起点的距离
        #parent[w]=v 表示w的前一个点是v
        while(len(pqueue)>0):
            
            pair=heapq.heappop(pqueue)
            dist=pair[0]
            vertex=pair[1]
            seen.add(vertex)
            nodes=graph[vertex].keys()
                   
            for w in nodes:
                if  w not in seen :
                    if dist+graph[vertex][w]<distance[w]:
                        heapq.heappush(pqueue,(dist+graph[vertex][w],w))
                        parent[w]=vertex
                        distance[w]=dist+graph[vertex][w]
        return parent,distance
     
    
    def findLength(Graph,carstart,carto):    
        parent = dijkstra(Graph, carstart)[0]
        out = []
        
        while carto !=None:
            out.insert(0,carto)
            carto=parent[carto]
            
        RoadList = findRoad(out)  
        
        return RoadList       
         
    count = 1
    num = 0
    count1 = 1
    num1 = 0
    count2 = 1
    num2 = 0
    count3 = 1
    num3 = 0
    answer = open(answer_path,"w") 
    with open(car_path) as car: #读取路   
        for carindex in car:
            if carindex[0] != "#":
                carre = carindex.split(",")
                carid=int(carre[0].split("(")[1])
                carfrom=int(carre[1])
                carto=int(carre[2])
                carspeed = int(carre[3])
                carplanTime=int(carre[4].split(")")[0])
                
                if carspeed > 6:
                    out = findLength(Graph,carfrom,carto) 
                    if count % 37 == 0:
                        num += 1
                    count += 1
                    out.insert(0,carplanTime+num)
                    out.insert(0,carid)
                    answer.writelines(str(tuple(out))+"\n")
                    
#                elif carspeed == 6:
#                    out = findLength(Graph,carfrom,carto) 
#                    if count % 40 == 0:
#                        num += 1
#                    count += 1
#                    out.insert(0,carplanTime+num)
#                    out.insert(0,carid)
#                    answer.writelines(str(tuple(out))+"\n")
#                    
#                elif carspeed == 4:
#                    out = findLength(Graph,carfrom,carto) 
#                    if count % 40 == 0:
#                        num += 1
#                    count += 1
#                    out.insert(0,carplanTime+num)
#                    out.insert(0,carid)
#                    answer.writelines(str(tuple(out))+"\n")
                       
                else:
                    if count3 % 24 == 0:
                        num3 += 1
                    count3 += 1
                    out = findLength(Graph,carfrom,carto) 
                    out.insert(0,carplanTime+1250+num3)
                    out.insert(0,carid)
                    answer.writelines(str(tuple(out))+"\n")
    answer.close() #关闭文件



if __name__ == '__main__':
    car_path = "car.txt"
    road_path = "road.txt"
    cross_path = "cross.txt"
    answer_path = "answer.txt"
    main(car_path,road_path,cross_path,answer_path)











  
    

                    
                        
