from typing import Callable

class PQ:
    def __init__(self, heuristic: Callable):  
        self.arr = []
        self.paths = {}
        self.heuristic = heuristic

    def _heapify_up(self, el: int): 
        f = self.heuristic

        if el != 0:
            parent = (el - 1) // 2
            if f(self.arr[parent]) > f(self.arr[el]):     
                self.arr[parent], self.arr[el] = self.arr[el], self.arr[parent]
                self._heapify_up(parent)
    
    def append(self, el: int):
        self.arr.append(el)
        last = len(self.arr) - 1
        self._heapify_up(last)
    
    def _heapify_down(self, el: int):  
        f = self.heuristic
        l = 2 * el + 1
        r = 2 * el + 2
        n = len(self.arr) - 1
        minimum = el
    
        if l <= n and f(self.arr[minimum]) > f(self.arr[l]):
            minimum = l 

        if r <= n and f(self.arr[minimum]) > f(self.arr[r]):
            minimum = r
        
        if minimum != el:  
            self.arr[el], self.arr[minimum] = self.arr[minimum], self.arr[el]
            self._heapify_down(minimum)

    def pop(self):
        root = self.arr[0]
        self.arr[-1], self.arr[0] = self.arr[0], self.arr[-1]
        self.arr.pop()
        self._heapify_down(0)
        return root
    
    def add_path(self, node: int, path: list):  
        self.paths[node] = path
    
    def get_path(self, node: int):  
        return self.paths[node] 