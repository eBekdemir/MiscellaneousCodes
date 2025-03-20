import numpy as np
import pandas as pd
import scipy.sparse as sp
from scipy.sparse.linalg import eigs
import json
import time

with open('data/ranking_settings.json') as f:
    S = json.load(f)

movies = pd.read_parquet('data/movies.parquet')
adjacency_matrix = pd.read_parquet('data/adjacency_matrix.parquet')
scores = pd.read_parquet('data/initial_scores.parquet').sort_values(by='id')


def pagerank(adjacency_df, alpha=0.85, tol=1e-6, max_iter=100, initial_scores=None):
    """
    adjacency_matrix : scipy.sparse matrix (N x N)
        Transition probability matrix where each row sums to 1.
    alpha : float, optional
        Damping factor, usually set to 0.85.
    tol : float, optional
        Convergence tolerance.
    max_iter : int, optional
        Maximum number of iterations.
    initial_scores : np.array, optional
        Custom initial PageRank scores.
    """
    adjacency_matrix = sp.csr_matrix(adjacency_df.values)
    n = adjacency_matrix.shape[0]
    
    # Handle dangling nodes (nodes with no outlinks)
    dangling_nodes = np.where(adjacency_matrix.sum(axis=1) == 0)[0]
    if len(dangling_nodes) > 0:
        adjacency_matrix[dangling_nodes, :] = 1.0 / n
    
    # Normalize the adjacency matrix row-wise to make it a stochastic matrix
    row_sums = np.array(adjacency_matrix.sum(axis=1)).flatten()
    stochastic_matrix = adjacency_matrix.multiply(1.0 / row_sums[:, None])
    
    # Teleportation matrix (uniform distribution for teleportation)
    teleportation = np.ones((n, 1)) / n
    
    # Initialize the scores
    if initial_scores is None:
        scores = np.ones(n) / n  # Equal probability distribution
    else:
        scores = np.array(initial_scores, dtype=np.float64)
        scores /= scores.sum()  # Normalize to sum to 1
        
    
    teleportation_part = (1 - alpha) * teleportation.flatten()

    # Power iteration method
    for _ in range(max_iter):
        new_scores = alpha * (stochastic_matrix.T @ scores) + teleportation_part
        
        # Check for convergence
        if np.linalg.norm(new_scores - scores, ord=1) < tol:
            break
        scores = new_scores
    return scores

def main():
    pRank = pagerank(adjacency_matrix, initial_scores=scores['totalScore'])
    df = pd.DataFrame({'id': scores['id'], 'pagerank': pRank})
    df.to_parquet('data/pagerank_scores2.parquet')



if __name__=='__main__':
    start = time.time()
    main()
    print(f'Pagerank scores computed in {time.time() - start:.2f} seconds.')