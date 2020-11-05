import requests
import json
import urllib.parse
import urllib.request
import array
import collections 



url = "https://rapidapi.p.rapidapi.com/words/funny/synonyms"

headers = {
    'x-rapidapi-key': "38a7bfcc1dmsh9dbba8c93ef165ep187a93jsnf1655cfe5b7a",
    'x-rapidapi-host': "wordsapiv1.p.rapidapi.com"
    }

r = requests.request("GET", url, headers=headers)


url = "https://rapidapi.p.rapidapi.com/associations/"

querystring = {"entry":"hyper"}

headers = {
    'x-rapidapi-key': "38a7bfcc1dmsh9dbba8c93ef165ep187a93jsnf1655cfe5b7a",
    'x-rapidapi-host': "twinword-word-associations-v1.p.rapidapi.com"
    }

response = requests.request("GET", url, headers=headers, params=querystring)

data = response.json()


print(data['associations_scored'])

for key in data['associations_scored']:
    print(key)
    print(data['associations_scored'][key])

#for key in data['associations_scored']:



######Dijkstras######

class SynonymGraph:

    class Vertex:
        edgesLeaving = collections.deque()
        data = 0

        def __init__(self, data):
            this.data = data
        
    class Edge:
        
       def __init__(self, target, weight):
           this.target = target
           this.weight = weight
    

    
    global vertices = HashTable(1000000)

    def insertVertex(data):
        if (data is None):
            raise TypeError
        if (vertices._find_by_key(data)):
            return False
        vertices.set(data, Vertex(data))
        return True

    def removeVertex(data):
        if(data is None):
            raise TypeError

        removeVertex = vertices._find_by_key(data)
        if(removeVertex is None):
            return False
        
        for vertex in vertices.keys:
            removeEdge = None

            for edge in vertex.edgesLeaving:
                if(edge.target == removeVertex):
                      removeEdge = edge

            if(removeEdge != None):
                vertex.edgesLeaving.remove(removeEdge)

        return vertices.remove(data) != null

    def insertEdge(source, target, weight):
        if(source == None or target == None):
            raise TypeError
        sourceVertex = this.vertices.get(source)
        targetVertex = this.vertex.get(target)

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
        
        sourceVertex.edgesLeaving.add(Edge(targetVertex))
        return True

    
    def removeEdge(source, target):
        if(source == None or target == None):
            raise TypeError
        sourceVertex = this.vertices.get(source)
        targetVertex = this.vertices.get(target)

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
    

    def containsVertex(data):
        if(data == None):
            raise TypeError

        return vertices._find_by_key(data)

    def containsEdge(source, target):
        if(source == None or target == None):
            raise TypeError

        sourceVertex = vertices.get(source)
        targetVertex = vertices.get(target)

        if(sourceVertex == None):
            return False

        for edge in sourceVertex.edgesLeaving:
            if(edge.target == targetVertex):
                return False
        return False

    def getWeight(source, target):
        if(source == None or target == None):
            raise TypeError

        sourceVertex = vertices.get(source)
        targetVertex = vertices.get(target)

        if(sourceVertex == None or targetVertex == None):
            raise TypeError

        for edge in sourceVertex.edgesLeaving:
            if(edge.target == targetVertex):
                return edge.weight
            
        raise Exception


        




            
            
                
            



    
        
    




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
                    raise KeyError(key)

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

       
      

#Vertex Graph



    


