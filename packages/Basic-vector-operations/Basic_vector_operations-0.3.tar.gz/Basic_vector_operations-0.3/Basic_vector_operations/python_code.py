import numpy as np

class Vector():
    
    def __init__(self, content):
        self.content = np.array(content)
        self.n = len(content)
        
    
    def calculate_norm(self):
        self.norm = np.sqrt(np.sum(self.content**2))
        return self.norm
        
    
    def add(self, other):
        if self.n == other.n:
            return self.content + other.content     
        else:
            raise Exception('Vectors need to have same length!')
    
    
   
    