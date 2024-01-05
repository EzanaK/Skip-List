from __future__ import annotations
import json
from typing import List

verbose = False

# DO NOT MODIFY!
class Node():
    def  __init__(self,
                  key      : int,
                  value    : str,
                  toplevel : int,
                  pointers : List[Node] = None):
        self.key      = key
        self.value    = value
        self.toplevel = toplevel
        self.pointers = pointers

# DO NOT MODIFY!
class SkipList():
    def  __init__(self,
                  maxlevel : int,
                  headnode : Node = None,
                  tailnode : Node = None):
        self.headnode  = headnode
        self.tailnode  = tailnode
        self.maxlevel = maxlevel

    # DO NOT MODIFY!
    # Return a reasonable-looking json.dumps of the object with indent=2.
    # We create an list of nodes,
    # For each node we show the key, the value, and the list of pointers and the key each points to.
    def dump(self) -> str:
        currentNode = self.headnode
        nodeList = []
        while currentNode is not self.tailnode:
            pointerList = str([n.key for n in currentNode.pointers])
            nodeList.append({'key':currentNode.key,'value':currentNode.value,'pointers':pointerList})
            currentNode = currentNode.pointers[0]
        pointerList = str([None for n in currentNode.pointers])
        nodeList.append({'key':currentNode.key,'value':currentNode.value,'pointers':pointerList})
        return json.dumps(nodeList,indent = 2)

    # DO NOT MODIFY!
    # Creates a pretty rendition of a skip list.
    # It's vertical rather than horizontal in order to manage different lengths more gracefully.
    # This will never be part of a test but you can put "pretty" as a single line in your tracefile
    # to see what the result looks like.
    def pretty(self) -> str:
        currentNode = self.headnode
        longest = 0
        while currentNode != None:
            if len(str(currentNode.key)) > longest:
                longest = len(str(currentNode.key))
            currentNode = currentNode.pointers[0]
        longest = longest + 2
        pretty = ''
        currentNode = self.headnode
        while currentNode != None:
            lineT = 'Key = ' + str(currentNode.key) + ', Value = ' + str(currentNode.value)
            lineB = ''
            for p in currentNode.pointers:
                if p is not None:
                    lineB = lineB + ('('+str(p.key)+')').ljust(longest)
                else:
                    lineB = lineB + ''.ljust(longest)
            pretty = pretty + lineT
            if currentNode != self.tailnode:
                pretty = pretty + "\n"
                pretty = pretty + lineB + "\n"
                pretty = pretty + "\n"
            currentNode = currentNode.pointers[0]
        return(pretty)

    # DO NOT MODIFY!
    # Initialize a skip list.
    # This constructs the headnode and tailnode each with maximum level maxlevel.
    # Headnode has key -inf, and pointers point to tailnode.
    # Tailnode has key inf, and pointers point to None.
    # Both have value None.
    def initialize(self,maxlevel):
        pointers = [None] * (1+maxlevel)
        tailnode = Node(key = float('inf'),value = None,toplevel = maxlevel,pointers = pointers)
        pointers = [tailnode] * (maxlevel+1)
        headnode = Node(key = float('-inf'),value = None, toplevel = maxlevel,pointers = pointers)
        self.headnode = headnode
        self.tailnode = tailnode
        self.maxlevel = maxlevel

    # Create and insert a node with the given key, value, and toplevel.
    # The key is guaranteed to not be in the skiplist.
    def insert(self,key,value,toplevel):
        node = Node(key=key,value=value,toplevel=toplevel,pointers=[None]*(1 + toplevel))
        cur = self.headnode
        while cur:
            if key < cur.key:
                # set node's pointer
                for i in range(toplevel+1):
                    while i > cur.toplevel:
                        cur = cur.pointers[0]
                    node.pointers[i] = cur   
                break                     
            cur = cur.pointers[0]
        # set pointers of previous nodes
        cur = self.headnode
        while cur != node:
            for i in reversed(range(min(cur.toplevel+1,node.toplevel+1))):
                if cur.pointers[i].key > node.key:
                    if cur == self.headnode:
                        self.headnode.pointers[i] = node
                    else:
                        cur.pointers[i] = node
                else:
                    cur = cur.pointers[i]
                    break

    # Delete node with the given key.
    # The key is guaranteed to be in the skiplist.
    def delete(self,key):
        cur = self.headnode
        while cur.key != key:
            for i in reversed(range(cur.toplevel+1)):
                if cur.pointers[i].key == key:
                    if cur == self.headnode:
                        self.headnode.pointers[i] = self.headnode.pointers[i].pointers[i]
                    else:
                        cur.pointers[i] = cur.pointers[i].pointers[i]
                elif cur.pointers[i].key < key:
                    cur = cur.pointers[i]
                    break
                if i == 0:
                    return

    # Search for the given key.
    # Construct a list of all the keys in all the nodes visited during the search.
    # Append the value associated to the given key to this list.
    def search(self,key) -> str:
        lst = []
        cur = self.headnode
        while cur.key != key:
            lst.append(cur.key)
            for i in reversed(range(cur.toplevel+1)):
                if cur.pointers[i].key <= key:
                    cur = cur.pointers[i]
                    break
        lst.append(cur.key)
        lst.append(cur.value)
        return json.dumps(lst,indent = 2)