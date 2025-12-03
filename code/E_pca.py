import sys
import os

import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
import pandas as pd

import project_logger

logger = project_logger.create_logger('pca')

def run_pca(x):
    """Run PCA on data"""
    # Transpose for finding PCA of samples, not CpGs
    transpose = x.transpose()

    # Run PCA
    pca = PCA(n_components=2)
    principals = pca.fit_transform(transpose)

    # Only use PC1 and PC2 for plotting
    pcs = pd.DataFrame(data=principals, columns=['pc1', 'pc2'])

    # Add sample name for merging with metadata later
    pcs['samp'] = [name.replace('_scaled', '') for name in transpose.index]

    return pca.explained_variance_ratio_, pcs

def make_plot(df, var, keys, cols, title, xlab, ylab, figname):
    """Create plot for PCA.

    Inputs -
        df      - PCA DataFrame with metadata included
        var     - name of column color points by
        keys    - keys from var to match to colors in cols list
        cols    - colors for coloring points
        title   - plot title
        xlab    - x-axis label
        ylab    - y-axis label
        figname - output file name
    Returns -
        None
    """
    fig, ax = plt.subplots(figsize=(5,5))
    plt.tight_layout()

    if len(keys) != len(cols):
        logger.error('Number of keys and colors does not match')
        sys.exit(1)

    # Easiest to add data points with each unique key to plot individually
    for key, col in zip(keys, cols):
        keep = df[var] == key
        if not any(list(keep)):
            continue

        ax.scatter(x=df.loc[keep, 'pc1'], y=df.loc[keep, 'pc2'], c=col, s=25)

    ax.legend(keys, ncol=1, loc='upper left', fontsize=12)

    plt.title(title)
    plt.xlabel(xlab)
    plt.ylabel(ylab)

    plt.savefig(figname, bbox_inches='tight')
    plt.close('all')

    return None

def main(df, meta):
    """Main function to generate principal component analysis"""
    # Only use scaled data for calculating PCA
    logger.info('Restricting to only scaled data for PCA')
    df_scaled = df[[col for col in df.columns if '_scaled' in col]].copy()

    var_ratio, pcs = run_pca(df_scaled)

    # Add metadata
    pcs = pcs.merge(meta, left_on='samp', right_on='WGBS_ID')

    # Create plots
    logger.info('Creating PCA plots')
    make_plot(
        pcs,
        'cluster', # stromal compartment cluster
        ['S1', 'S2', 'S3', 'S4'],
        ['red', 'blue', 'green', 'brown'],
        'PCA: Stromal Cluster',
        f'Prinicipal Component 1 [{var_ratio[0]:.3f}]',
        f'Prinicipal Component 2 [{var_ratio[1]:.3f}]',
        'pca_cluster.pdf',
    )

    make_plot(
        pcs,
        'cellType', # type of cell
        ['stromal', 'epithelial'],
        ['#e41a1c', '#377eb8'],
        'PCA: Cell Type',
        f'Prinicipal Component 1 [{var_ratio[0]:.3f}]',
        f'Prinicipal Component 2 [{var_ratio[1]:.3f}]',
        'pca_cell_type.pdf',
    )

    make_plot(
        pcs,
        'histotype', # type of ovarian cancer
        ['ENOC', 'CCOC', 'HGSC'],
        ['red', 'blue', 'brown'],
        'PCA: Histotype',
        f'Prinicipal Component 1 [{var_ratio[0]:.3f}]',
        f'Prinicipal Component 2 [{var_ratio[1]:.3f}]',
        'pca_histotype.pdf',
    )

    make_plot(
        pcs,
        'Stage_full', # cancer stage
        ['IA', 'IB', 'IC', 'IIA', 'IIB', 'IIC', 'III', 'IIIA', 'IIIB', 'IIIC'],
        ['#014636', '#016c59', '#02818a', '#3690c0', '#67a9cf', '#a6bddb', '#d0d1e6', '#d0d1e6', '#ece2f0', '#fff7fb'],
        'PCA: Stage',
        f'Prinicipal Component 1 [{var_ratio[0]:.3f}]',
        f'Prinicipal Component 2 [{var_ratio[1]:.3f}]',
        'pca_stage.pdf',
    )

    return None

if __name__ == '__main__':
    meta_name = '../data/metadata.tsv'
    logger.info(f'Reading metadata file: {meta_name}')
    meta = pd.read_csv(meta_name, sep='\t')

    df_name = 'example_data.tsv'
    if os.path.exists(df_name):
        logger.info(f'Reading preprocessed data file: {df_name}')
        df = pd.read_csv(df_name, sep='\t', index_col=['chr', 'start'])
        main(df, meta)
    else:
        logger.error('B_preprocess_data.py has not been run. Run and try again!')
