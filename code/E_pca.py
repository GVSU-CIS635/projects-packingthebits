import os

import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import pandas as pd
import numpy as np

import project_logger

logger = project_logger.create_logger('pca')

def run_pca(x):
    """Run PCA on data"""
    # TODO: verify PCA okay
    pca = PCA(n_components=2)
    principals = pca.fit_transform(x)
    print(pca.explained_variance_ratio_)
    pcs = pd.DataFrame(data=principals, columns=['pc1', 'pc2'])
    print(pcs)

    # TODO: Add metadata columns for plotting with colors

def main(df):
    """Main function to generate principal component analysis"""
    # Only use scaled data for calculating PCA
    logger.info('Restricting to only scaled data for PCA')
    df_scaled = df[[col for col in df.columns if '_scaled' in col]].copy()

    run_pca(df_scaled)

    return None

if __name__ == '__main__':
    fname = 'example_data.tsv'
    logger.info(f'Reading preprocessed data file: {fname}')
    df = pd.read_csv(fname, sep='\t', index_col=['chr', 'start'])

    if os.path.exists(fname):
        main(df)
    else:
        logger.error('B_preprocess_data.py has not been run. Run and try again!')
