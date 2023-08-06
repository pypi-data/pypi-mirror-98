from skyline_solver import skyline_solver

# Skyline vector of a symmetric matrix
# 1-based indexing must be used
m=[1,1,2,3,1]

# The matrix initialization
sk=skyline_solver(m)

# The matrix is initialized with zero values by default. 
# However, the initial values can be set using the set method:
sk.set(0.0)


print("The rank is:", sk.rank)
print("The number of non-zero values is:", sk.nnz)

# Adding values according to 1-based indexing scheme.
sk.add_value(1,1,2.0)
sk.add_value(1,2,-2.0)
sk.add_value(1,5,-1.0)

sk.add_value(2,2,3.0)
sk.add_value(2,3,-2.0)

sk.add_value(3,3,5.0)
sk.add_value(3,4,-3.0)

sk.add_value(4,4,10.0)
sk.add_value(4,5,4.0)

sk.add_value(5,5,10.0)

print("The matrix in the dense format is:")
print(sk.to_dense())

# The factorization is done inplace.
sk.decompose()

print("The factorized matrix in the dense format is:")
print(sk.to_dense())

# Constants or load vectors 
f=[0,1,0,0,0]

# Providing in place solution
f = sk.solve(f)

print("The solution is:")
print(f) 
print("The solution from Finite Element Procedures By K. J. Bathe (Example 8.5) is:")
print([636, 619, 292, 74, 34])
