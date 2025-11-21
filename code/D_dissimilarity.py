import os

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

import project_logger

logger = project_logger.create_logger('dissimilarity')

def euclidean_norm(v):
    """Calculate Euclidean norm of a vector"""
    total = sum(x_i*x_i for x_i in v)

    return np.sqrt(total)

def dot_product(x, y):
    """Calculate dot product between two vectors"""
    return sum(x_i*y_i for x_i, y_i in zip(x, y))

def cosine_similarity(x, y):
    """Calculate cosine similarity between two vectors"""
    x_norm = euclidean_norm(x)
    y_norm = euclidean_norm(y)

    dot = dot_product(x, y)

    return dot / (x_norm*y_norm)

def calculate_dissimilarity_matrix(df):
    """Calculate dissimilarity matrix"""
    t_df = df.T

    data = []
    for i in range(len(t_df)):
        row = []
        for j in range(len(t_df)):
            if j > i:
                # Only calculate one triangular portion of matrix
                row.append(np.nan)
            elif j == i:
                # Shortcut value for on-diagonal of matrix
                row.append(0.0)
            else:
                dis = 1 - cosine_similarity(t_df.iloc[i], t_df.iloc[j])
                row.append(round(dis, 3))
        data.append(row)

    return data

def plot_dissimilarity(mat, labels):
    """Draw heatmap of dissimilarity values"""
    fig, ax = plt.subplots(figsize=(8,8))
    plt.tight_layout()

    hm = ax.pcolor(mat, vmin=np.nanmin(mat), vmax=np.nanmax(mat))
    hm.cmap.set_under('white')

    cbar = fig.colorbar(hm)

    ax.set_xticks(np.arange(len(labels)) + 0.5, labels, minor=False, rotation=45)
    ax.set_yticks(np.arange(len(labels)) + 0.5, labels, minor=False)

    ax.invert_yaxis()
    ax.xaxis.tick_top()

    # Only add text if the dimension isn't too high
    if len(mat) < 10:
        for i in range(len(mat)):
            for j in range(len(mat)):
                text = ax.text(j+0.5, i+0.5, mat[i][j], ha='center', va='center', color='w')

    ax.set_title('Dissimilarity Matrix')

    plt.savefig('dissimilarity_matrix.pdf', bbox_inches='tight')
    plt.close('all')

    return None

def main(df):
    """Calculate and plot a dissimilarity matrix from preprocessed data"""
    # Only use raw data for calculating dissimilarity
    logger.info('Restricting to only raw data for plotting')
    df_raw = df[[col for col in df.columns if '_raw' in col]].copy()

    # Find 10,000 most variable CpGs, then use these to calculate dissimilarity
    df_raw['variance'] = df_raw.var(axis=1)

    df_sorted = df_raw.sort_values(by='variance', ascending=False)
    df_sorted.drop(columns='variance', inplace=True)
    df_sorted.reset_index(drop=True, inplace=True)
    df_sorted = df_sorted.head(10000)

    logger.info('Calculating dissimilarity matrix')
    mat = calculate_dissimilarity_matrix(df_sorted)

    logger.info('Plotting dissimilarity matrix')
    plot_dissimilarity(mat, df_sorted.columns)

    return None

if __name__ == '__main__':
    fname = 'example_data.tsv'

    if os.path.exists(fname):
        logger.info(f'Reading preprocessed data file: {fname}')
        df = pd.read_csv(fname, sep='\t', index_col=['chr', 'start'])
        main(df)
    else:
        logger.error('B_preprocess_data.py has not been run. Run and try again!')
