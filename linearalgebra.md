```mermaid
flowchart TD

subgraph A1[1. Systems of Linear Equations and Matrix Representations]
    A1a[Systems of Linear Equations]
    A1b[Gauss-Jordan Elimination]
    A1c[Row Reduction & Solution Sets]
    A1d[Matrix Equation Ax=b]
    A1e[Homogeneous Systems]
    A1f[Linear Independence]
    A1g[Vector Equations and Linear Combinations]
end

subgraph A2[2. Linear Transformations]
    A2a[Introduction to Linear Transformations]
    A2b[Matrix of a Linear Transformation]
    A2c[Inverses of Linear Transformations]
    A2d[Compositions & Matrix Products]
    A2e[Linear Transformations in Geometry]
    A2f[Applications to Differential Equations]
end

subgraph A3[3. Matrix Algebra]
    A3a[Matrix Operations]
    A3b[Inverse of a Matrix & Invertibility]
    A3c[Partitioned Matrices]
    A3d[Matrix Products and Composition]
end

subgraph A4[4. Subspaces and Dimension]
    A4a[Subspaces of R^n]
    A4b[Null Space, Column Space, Image and Kernel]
    A4c[Basis and Linear Independence]
    A4d[Coordinate Systems & Change of Basis]
    A4e[Dimension and Rank]
    A4f[Applications to Markov Chains]
end

subgraph A5[5. Determinants]
    A5a[Introduction to Determinants]
    A5b[Properties of Determinants]
    A5c[Geometric Interpretation, Cramer's Rule, Volume]
    A5d[Permutation Matrices]
end

subgraph A6[6. Orthogonality and Least Squares]
    A6a[Inner Product, Norm, Orthogonality]
    A6b[Orthogonal Projections]
    A6c[Gram-Schmidt and QR Factorization]
    A6d[Orthonormal Bases & Orthogonal Matrices]
    A6e[Least Squares & Data Fitting]
end

subgraph A7[7. Eigenvalues and Eigenvectors]
    A7a[Introduction via Dynamical Systems]
    A7b[Finding Eigenvalues]
    A7c[Finding Eigenvectors]
    A7d[Diagonalization]
    A7e[Complex Eigenvalues & Rotations]
    A7f[Stability Analysis]
    A7g[Applications in Differential Equations]
end

subgraph A8[8. Symmetric Matrices and Quadratic Forms]
    A8a[Diagonalization of Symmetric Matrices]
    A8b[Quadratic Forms]
    A8c[Singular Value Decomposition SVD]
end

subgraph A9[9. Abstract Linear Spaces]
    A9a[General Vector Spaces & Subspaces]
    A9b[Review of Coordinate Systems and Advanced Spaces]
end

subgraph A10[10. Optional Topics in Differential Equations]
    A10a[ODEs, PDEs, Fourier Series]
end

%% Link big topics only
A1 --> A2
A2 --> A3
A3 --> A4
A4 --> A5
A5 --> A6
A6 --> A7
A7 --> A8
A8 --> A9
A9 --> A10


'''
