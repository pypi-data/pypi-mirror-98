import unittest
import numpy as np

from python_code import Vector

class TestVectorClass(unittest.TestCase):
    def setUp(self):
        self.Vector = Vector([3,4])
        self.Vector2 = Vector([6,8])
        self.Vector3 = Vector([-1,-2,-3])

    def test_initialization(self): 
        self.assertEqual(self.Vector.n, 2, 'incorrect length')
        
    def test_norm(self):
        self.assertEqual(self.Vector2.calculate_norm(), 10.0, 'incorrect norm')

    def test_sum(self):
        self.assertEqual(self.Vector.add(self.Vector2).all(), np.array([9,12]).all(), 'incorrect sum')
    
    def test_sum_different_lengths(self):
        self.assertEqual(self.Vector.add(self.Vector3).all(), np.array([9,12]).all(), 'incorrect sum')
    
if __name__ == '__main__':
    unittest.main()