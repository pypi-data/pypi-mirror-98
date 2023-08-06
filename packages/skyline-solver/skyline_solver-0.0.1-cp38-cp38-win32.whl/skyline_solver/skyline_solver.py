from skyline import skyline
import numpy as np

class skyline_solver:
    def __init__(self,m):
        skyline.init(np.array(m,dtype=int,order='F'))
        self.rank=skyline.dof_total
        self.nnz=skyline.nnz
    
    def add_value(self,i,j,v):
        skyline.add_value(i,j,v)
    
    def decompose(self):
        skyline.decompose()
    
    def solve(self,f):
        x = np.array(f,dtype=float,order='F')
        skyline.solve(x)
        return x

    
    def to_dense(self):
        dof = skyline.dof_total
        d = np.zeros((dof,dof),dtype=float,order='F')
        skyline.to_dense(d)
        return d
    
    def get_skylineVector(self):
        return skyline.m
    
    def get_valuesVector(self):
        return skyline.a
    
    def get_rank(self):
        return skyline.dof_total
    
    def get_value(self,i,j):
        v = skyline.get_value(i,j)
        return v
    
    def set_value(self,i,j,v):
        skyline.set_value(i,j,v)
    
    def set(self,v):
        skyline.set(v)
    
