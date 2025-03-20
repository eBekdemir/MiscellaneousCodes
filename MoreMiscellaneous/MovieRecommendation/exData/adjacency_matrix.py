import pandas as pd
import numpy as np
from scipy.sparse import lil_matrix
import time

movies = pd.read_parquet('movies.parquet')

def main() -> None:
    relation = movies[['id','suggestionsID']]

    relation['suggestionsID'] = relation['suggestionsID'].apply(lambda x: x.split(':,:') if isinstance(x, str) else [])

    unique_ids = sorted(set(relation['id']))
    id_to_index = {id_val: idx for idx, id_val in enumerate(unique_ids)}


    matrix_size = len(unique_ids)
    # adj_matrix = np.zeros((matrix_size, matrix_size), dtype=int)
    adj_matrix = lil_matrix((matrix_size, matrix_size), dtype=int)


    for _, row in relation.iterrows():
        row_idx = id_to_index[row['id']]
        for suggested in row['suggestionsID']:
            if suggested in id_to_index:
                col_idx = id_to_index[suggested]
                adj_matrix[row_idx, col_idx] = 1  


    # adj_df = pd.DataFrame(adj_matrix, index=unique_ids, columns=unique_ids)
    adj_df = pd.DataFrame.sparse.from_spmatrix(adj_matrix, index=unique_ids, columns=unique_ids)

    adj_df = adj_df.astype(bool)
    adj_df.to_parquet('adjacency_matrix.parquet')



if __name__=='__main__':
    start = time.time()
    main()
    print(f'Finished in {time.time() - start:.2f} seconds')