import requests
import json
import urllib.parse
import urllib.request
import array
import collections 
import copy
import pandas as pd
import numpy as np
#from multipledispatch import dispatch 
#from multimethod import multimethod



url = "https://rapidapi.p.rapidapi.com/words/funny/synonyms"

headers = {
    'x-rapidapi-key': "38a7bfcc1dmsh9dbba8c93ef165ep187a93jsnf1655cfe5b7a",
    'x-rapidapi-host': "wordsapiv1.p.rapidapi.com"
    }

r = requests.request("GET", url, headers=headers)






#for key in data['associations_scored']:

def hash_function(key_str, size):
    return sum([ord(c) for c in key_str]) % size

class HashTable:
        """ Hash table which uses strings for keys. Value can be any object.
        Example usage:
            ht = HashTable(10)
            ht.set('a', 1).set('b', 2).set('c', 3)
            ht['c'] = 30
        """

        def __init__(self, capacity=1000):
            """ Capacity defaults to 1000. """

            self.capacity = capacity
            self.size = 0
            self._keys = []
            # Storage format: [ [ [key1, value], [key2, value] ], [ [key3, value] ] ]
            # The outmost list is the one which the hash function maps the index to. The next inner
            # Array is the list of objects in that storage cell. The 3rd level is the individual
            # item array, where the 1st item is the key, and the 2nd item is the value.
            self.data = [[] for _ in range(capacity)]

        def _find_by_key(self, key, find_result_func):
            index = hash_function(key, self.capacity)
            hash_table_cell = self.data[index]
            found_item = None
            for item in hash_table_cell:
                if item[0] == key:
                    found_item = item
                    break

            return find_result_func(found_item, hash_table_cell)

        def set(self, key, obj):
            """ Insert object with key into hash table. If key already exists, then the object will be
            updated. Key must be a string. Returns self. """

            def find_result_func(found_item, hash_table_cell):
                if found_item:
                    found_item[1] = obj
                else:
                    hash_table_cell.append([key, obj])
                    self.size += 1
                    self._keys.append(key)

            self._find_by_key(key, find_result_func)
            return self

        def get(self, key):
            """ Get object with key (key must be a string). If not found, it will raise a KeyError. """

            def find_result_func(found_item, _):
                if found_item:
                    return found_item[1]
                else:
                    return False

            return self._find_by_key(key, find_result_func)

        def remove(self, key):
            """ Remove the object associated with key from the hashtable. If found, the object will
            be returned. If not found, KeyError will be raised. """

            def find_result_func(found_item, hash_table_cell):
                if found_item:
                    hash_table_cell.remove(found_item)
                    self._keys.remove(key)
                    self.size -= 1
                    return found_item[1]
                else:
                    raise KeyError(key)

            return self._find_by_key(key, find_result_func)


        ####### Python's dict interface

        def keys(self):
            return self._keys

        def __setitem__(self, key, value):
            self.set(key, value)

        def __getitem__(self, key):
            return self.get(key)

        def __delitem__(self, key):
            return self.remove(key)

        def __repr__(self):
            return '{ ' + ', '.join([key + ':' + str(self.get(key)) for key in self._keys]) + ' }'

       


######Dijkstras######

class SynonymGraph:
    

    def __init__(self):
        emotions = ['depressed', 'angry', 'frustrated', 'appreciative', 'amused', 'anxious', 'awkward', 'bored', 'disgusted', 'calm', 'confused', 'empathetic', 'entranced', 'envious', 'excited', 'fearful', 'joyful', 'horrendous', 'stressed', 'prideful']
        self.vertices = HashTable(20000)
        #words
        self.df = pd.DataFrame()
        
        #dijkstras
        self.dj = pd.DataFrame()
        self.dj = self.dj.reindex(columns=emotions)



    class Vertex:
        edgesLeaving = None
        size = 0
        data = 0

        def __init__(self, data):
            self.data = data
            self.edgesLeaving = collections.deque()
        
        
    class Edge:
        
       def __init__(self, target, weight):
           self.target = target
           self.weight = weight
    


    def insertVertex(self, data):
        if (data is None):
            raise TypeError
        if (self.vertices.get(data)):
            return False
        
        vertex = self.Vertex(data)
        self.vertices.set(data, vertex)
        return True

    def removeVertex(self, data):
        if(data is None):
            raise TypeError

        removeVertex = self.vertices.get(data)
        if(removeVertex is None):
            return False
        
        for vertex in self.vertices._keys:
            removeEdge = None

            for edge in vertex.edgesLeaving:
                if(edge.target == removeVertex):
                      removeEdge = edge

            if(removeEdge != None):
                vertex.edgesLeaving.remove(removeEdge)

        return self.vertices.remove(data) != None

    def insertEdge(self, source, target, weight):
        if(source == None or target == None):
            raise TypeError
        if(source == False or target == False):
            return
        
        sourceVertex = self.vertices.get(source.data)
        targetVertex = self.vertices.get(target.data) #flagged

        if(sourceVertex == None or targetVertex == None):
            raise TypeError

        if(weight < 0):
            raise TypeError

        for edge in sourceVertex.edgesLeaving:
            if(edge.target == targetVertex):
                if(edge.weight == weight):
                    return False
                else:
                    edge.weight = weight
                return True
        edge = self.Edge(targetVertex, weight)
        sourceVertex.edgesLeaving.append(edge)
        sourceVertex.size += 1
        return True

    
    def removeEdge(self, source, target):
        if(source == None or target == None):
            raise TypeError
        sourceVertex = self.vertices.get(source.data)
        targetVertex = self.vertices.get(target.data)

        if(sourceVertex == None or target == None):
            raise TypeError

        removeEdge = None

        for edge in sourceVertex.edgesLeaving:
            if(edge.target == targetVertex):
                removeEdge = edge

        if(removeEdge != None):
            sourceVertex.edgesLeaving.remove(removeEdge)
            return True
        
        return False
    
    def containsVertex(self, data):
        if(data == None):
            raise TypeError

        return self.vertices.get(data)

    def containsEdge(self, source, target):
        if(source == None or target == None):
            raise TypeError

        sourceVertex = self.vertices.get(source.data)
        targetVertex = self.vertices.get(target.data)

        if(sourceVertex == None):
            return False

        for edge in sourceVertex.edgesLeaving:
            if(edge.target == targetVertex):
                return False
        return False

    def getWeight(self, source, target):
        if(source == None or target == None):
            raise TypeError

        sourceVertex = self.vertices.get(source)
        targetVertex = self.vertices.get(target)

        if(sourceVertex == None or targetVertex == None):
            raise TypeError

        for edge in sourceVertex.edgesLeaving:
            if(edge.target == targetVertex):
                return edge.weight
            
        raise Exception


    def getEdgeCount(self):
        edgeCount = 0

        for vertex in self.vertices._keys:
            edgeCount += vertex.edgesLeaving.size
        
        return edgeCount

    def getVertexCount(self):
        return self.vertices.size

    def isEmpty(self):
        return self.vertices.size == 0

    def insertEdgestoDataFrame(self):
        for word in list(self.df.index):
            vertex = self.vertices.get(word)
            for edge in list(vertex.edgesLeaving):
                self.df.at[word, edge.target.data] = edge.weight
        


    def insertDataFrame(self, fileName):
        self.df = pd.read_csv(fileName)

    


    class Path:

        def __init__(self, start):
            if isinstance(start, SynonymGraph.Vertex):
                self.start = start
                self.distance = 0
                self.dataSequence = collections.deque()
                self.dataSequence.append(start.data)
                self.end = start

            elif isinstance(start, SynonymGraph.Path):
                #for num in range(0, start.dataSequence.__len__()):
                self.start = start.start
                self.distance = start.distance
                self.dataSequence = collections.deque()
                for word in start.dataSequence:
                    self.dataSequence.append(start.dataSequence.index(word))
                self.end = start.end
            else:
                raise TypeError


        def extend(self, edge):
            self.dataSequence.append(edge.target.data)
            self.distance += edge.weight
            self.end = edge.target


        def compareTo(self, other):
            cmp = self.distance - other.distance
            if(cmp != 0):
                return cmp
            
            return self.end.data - other.end.data


    #you shouldn't need this

    def getIndex(self, edges, num):
        deepEdges = copy.deepcopy(edges)

        
        for x in list(deepEdges):
            #flag
            if(x.weight == num.weight):
                return deepEdges.popleft() 

            
            deepEdges.popleft()

    #all calculations done inside method
    def dijkstrasShortestPath(self, start, end):
        
       
        queue = collections.deque()  #change collections to priority queue
        
        if(not self.containsVertex(start)):
            raise Exception
        
        startNode = self.vertices.get(start)
        endNode = self.vertices.get(end)

        visited = collections.deque()
        paths = collections.deque()

        startPath = SynonymGraph.Path(startNode)
        
        queue.append(startPath)

        
        
        if(len(startNode.edgesLeaving) == 0):
                raise Exception
        


        while(len(queue) != 0):
            print(len(queue))
            c = queue.popleft()
           
            if(visited.count(c.end) > 0):
                queue.popleft()
                continue

            currNode = c.end

            if(currNode != None and currNode.edgesLeaving != None):
                

                for x in list(currNode.edgesLeaving):
                    

                    nodePath = SynonymGraph.Path(c)
                    nodePath.extend(self.getIndex(currNode.edgesLeaving, x)) #fix
                    queue.append(nodePath)

                       
            
            visited.append(currNode.data)
            temp = queue.popleft
            paths.append(temp)

        '''   
        finalPath = None

        for path in paths:
            if(path.start == startNode.data and path.end == endNode.data):
                finalPath = path
                break
        
        if (finalPath == None):
            raise Exception
    
        return finalPath
        '''
        #i = 0
        for path in paths:
            self.dj.at[self.dj.loc[path.end.data], start] = path.weight
            #i += 1

        print(self.dj)
        
    '''
    def insertFromDataFrame(self):
        for word in df.index:
            self.insertVertex(word)
        
        for word in df.columns:
            self.insertVertex
        
    '''

    def insertAllVertices(self, start_query):
        url = "https://api.datamuse.com/words?ml={}&sp&max=8000".format(start_query)
        r = requests.get(url)
        data = r.json()
           
        queue = collections.deque()
        '''
        if(not self.vertices.get(start_query)):
            self.insertVertex(start_query)
        else:
            return
        '''
        if(self.vertices.get(start_query)):
            return
        
        self.insertVertex(start_query)
        
        
        queue.append(start_query)
        self.df[start_query] = 0
        self.df = self.df.append(pd.Series(name=start_query))
        if(len(data) <= 0):
            raise Exception


        while(len(queue) != 0):
            
            print(len(queue))
            #print(self.df)
            nextWord = queue.popleft()
            
            queue.appendleft(nextWord)
           
            url = f"https://api.datamuse.com/words?ml={nextWord}&sp&md=f&max=8000"
            r = requests.get(url)
            data = r.json()
           
            

            if(nextWord != None):
                nextNode = self.vertices.get(nextWord)
                self.insertEdge(nextNode, nextNode, 0)
                size = 0
                for word in data:
                    if(size == 5):
                        break
                    #add in score
                    try:
                        freq = None
                        
                        for tag in word['tags']:
                            if(tag[:1] == 'f'):
                                freq = tag[2:3]
                                break

                        for tag in word['tags']:   
                            if(int(freq) > 3 and tag == 'adj' and not self.vertices.get(word['word'])):
                                self.insertVertex(word['word'])
                                targetVert = self.vertices.get(word['word'])
                                self.insertEdge(nextNode, targetVert, word['score'])
                                queue.append(word['word'])
                                
                                self.df = self.df.append(pd.Series(name=word['word']))
                                self.df[word['word']] = None
                                size += 1
                                break
                        
                    except KeyError:
                        print("Not adj or no score")
                        continue

                   

            '''
            for edge in self.vertices.get(nextWord).edgesLeaving:
                print(edge.target.data)
                print(edge.weight)
            '''

            queue.popleft()
            #graph.insertEdgestoDataFrame()
            #graph.dataFrameToCSV()
            '''
            for vertex in list(self.vertices._keys):
                print(vertex)
            '''
        
    #gapminder.loc[:,'pop_in_millions'] = -1 add column
    #gapminder.

    def shortestPath(self, start, end):
        return self.dijkstrasShortestPath(start, end).dataSequence

    def getPathCost(self, start, end):
        return self.dijkstrasShortestPath(start, end).distance
    
    def insertPaths(self):
        for word in self.df.index:
            for emotion in list(self.df.columns):
                distance = self.getPathCost(word, emotion)
                self.df.at[word, emotion]= distance

    def dataFrameToCSV(self):
        self.df.to_csv('wordgraph.csv', index=True)

    def shortestDataFrameToCSV(self):
        self.df.to_csv('shortestpath.csv', index=True)
    
    def insertVerticesAndEdgesFromCSV(self):
        self.insertDataFrame('wordgraph.csv')
        print(self.df)
        for word in self.df['words']:
            self.insertVertex(word)


        '''
        for row in self.df['words']:
            for column in self.df.columns[1:]:
                if(self.df.loc[row, column] != 0):
                    self.insertEdge(row, column, self.df.at[row, column])
        
        
        for column in self.df.columns[1:]:

            self.df[column] = self.df[column].fillna('')

        print(self.df)
        '''
        size = 1
        for row in range(4373):
            self.dj = self.dj.append(pd.Series(name=self.df.loc[row,'words']))
            print(size)
            size += 1
            for column in self.df.columns[1:]:
                if(not pd.isnull(self.df.loc[row, column])):
                    self.insertEdge(self.vertices.get(self.df.loc[row,'words']), self.vertices.get(column), self.df.at[row, column])
        


    
    def dijkstrasShortestPathtoCSV(self):
        print(self.dj)
        for emotion in self.dj.columns[1:]:
            #self.dj.at[word, emotion] = self.getPathCost(word, emotion)
            self.getPathCost(self.df.loc[0, 'words'], emotion)
            self.dj.to_csv('dijkstras.csv', index=True)

            #self.dj.at[self.dj.iloc[word], emotion] 
        
        
    


            
            

    

    
    
    



#print(data[])  
'''     
for key, value in data['associations_scored'].items():
    print(key, value)
    #print(data['associations_scored'][key])
'''


graph = SynonymGraph()
'''
graph.insertAllVertices('depressed')
graph.insertAllVertices('angry')
graph.insertAllVertices('frustrated')
graph.insertAllVertices('appreciative')
graph.insertAllVertices('amused')
graph.insertAllVertices('anxious')
graph.insertAllVertices('awkward')
graph.insertAllVertices('bored')
graph.insertAllVertices('calm')
graph.insertAllVertices('confused')
graph.insertAllVertices('disgusted')
graph.insertAllVertices('empathetic')
graph.insertAllVertices('entranced')
graph.insertAllVertices('envious')
graph.insertAllVertices('excited')
graph.insertAllVertices('fearful')
graph.insertAllVertices('joyful')
graph.insertAllVertices('horrendous')
graph.insertAllVertices('stressed')
graph.insertAllVertices('prideful')

graph.insertEdgestoDataFrame()
graph.dataFrameToCSV()
'''


graph.insertVerticesAndEdgesFromCSV()

graph.dijkstrasShortestPathtoCSV()



#graph.dijkstrasShortestPathtoCSV()
#graph.insertPaths()
#graph.dataFrameToCSV()

#path = graph.getPathCost('funny', 'hilarious')

#data = [{'a': 1, 'b': 2}, {'a': 5, 'b': 10, 'c': 20}] 

#df.to_csv(index=False)
#df.at['funny','admirable']= 20


    
    
#df = pd.DataFrame(columns =['admirable', 'adoring', 'appreciative', 'amused', 'anxious', 'awesome', 'awkward', 'bored', 'calm', 'confused', 'craved', 'disgusted', 'empathetic', 'entranced', 'envious', 'excited', 'fearful', 'horrendous', 'interesting', 'joyful', 'nostalgic', 'romantic', 'sad', 'satisfied', 'lustful', 'sympathetic', 'triumphant'])



#print(index)
'''
for row in df.iterrows():
    print(row)
'''



#print(data)

'''
size = 0
for word in data:
    string = word['tags'][len(word['tags'])-1]
    c
    if((word['tags'][0] == "adj" or (len(word['tags']) > 1 and word['tags'][1] == "adj")) and size < 20):
        size += 1
        print(word['word'])
'''


'''
Admiration - *
Adulatory - * 
Aesthetic appreciation - Appreciative - *
Amused - *
Anxious - *
Awesome - *
Awkward - *
Bored - *
Calm - *
Confused - *
Craved - *
Disgusted - *
Empathetic pain - Empathetic - *
Entranced - *
Envious - *
Excited - *
Fearful - *
Horrendous - * 
Interesting - *
Joyful - *
Nostalgic - *
Romantic - *
Sad - *
Satisfied - *
Lustful - *
Sympathetic - *
Triumphant - *
'''

   
# With two column indices, values same  
# as dictionary keys 

