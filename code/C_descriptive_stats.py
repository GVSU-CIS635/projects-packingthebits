import os

import matplotlib.pyplot as plt
import pandas as pd

import project_logger

logger = project_logger.create_logger('descriptive_stats')

def by_sample(df):
    """Create a by-sample boxplot"""
    fig = plt.figure(figsize=(10, 5))
    plt.tight_layout()

    bp = plt.boxplot(df, sym='k.')

    plt.setp(bp['fliers'], markersize=1)

    plt.title('Methylation Levels By Sample')
    plt.xlabel('')
    plt.ylabel('Methylation Level')

    plt.ylim(0, 1.05)

    fontsize = 10 if len(df.columns) <= 10 else 6

    plt.xticks(ticks=range(1,len(df.columns)+1), labels=df.columns, rotation=90, fontsize=fontsize)

    plt.savefig('stats_by_sample.pdf', bbox_inches='tight')
    plt.close('all')

    return None

def by_cpg_cell_type(df):
    """Create lineplot of statistics by CpG"""
    e_samples = [x for x in df.columns if x.endswith('E_raw')]
    s_samples = [x for x in df.columns if x.endswith('S_raw')]
    e_mean = df[e_samples].mean(axis=1)
    s_mean = df[s_samples].mean(axis=1)

    fig, ax = plt.subplots(figsize=(5, 5))
    plt.tight_layout()

    parts = ax.violinplot(
        [e_mean, s_mean],
        positions=[1.0, 1.3],
        widths=0.2,
        showmeans=True,
        showmedians=True
    )

    colors = ['#377eb8', '#e41a1c']
    for i, part in enumerate(parts['bodies']):
        part.set_facecolor(colors[i])
        part.set_edgecolor('black')
        part.set_alpha(1)

    parts['cmeans'].set_color('black')
    for key in ['cmins', 'cmaxes', 'cbars', 'cmedians']:
        parts[key].set_color('#bdbdbd')

    plt.title('Mean Methylation Levels Across All CpGs')
    plt.xlabel('')
    plt.ylabel('Methylation Level')

    plt.xlim(0.8,1.5)
    plt.ylim(0, 1.05)
    plt.xticks(ticks=[1,1.3], labels=['Epithelial', 'Stromal'])

    plt.savefig('stats_by_cpg.pdf', bbox_inches='tight')
    plt.close('all')

    return None

def main(df):
    """Calculate and plot descriptive statistics from preprocessed data"""
    logger.info('Restricting to only raw data for plotting')
    df_raw = df[[col for col in df.columns if '_raw' in col]]

    logger.info('Generating by-sample descriptive statistics plot')
    by_sample(df_raw)

    logger.info('Generating by-CpG descriptive statistics plot')
    by_cpg_cell_type(df_raw)

    return None

if __name__ == '__main__':
    fname = 'example_data.tsv'

    if os.path.exists(fname):
        logger.info(f'Reading preprocessed data file: {fname}')
        df = pd.read_csv(fname, sep='\t', index_col=['chr', 'start'])
        main(df)
    else:
        logger.error('B_preprocess_data.py has not been run. Run and try again!')
