import os

import matplotlib.pyplot as plt
import pandas as pd

import project_logger

logger = project_logger.create_logger('descriptive_stats')

def by_sample(df):
    """Create a by-sample boxplot"""
    fig = plt.figure(figsize=(10, 5))
    plt.tight_layout()

    plt.boxplot(df)

    plt.title('Methylation Levels By Sample')
    plt.xlabel('')
    plt.ylabel('Methylation Level')

    plt.ylim(0, 1.05)

    plt.xticks(ticks=range(1,len(df.columns)+1), labels=df.columns, rotation=90)

    plt.savefig('stats_by_sample.pdf', bbox_inches='tight')
    plt.close('all')

    return None

def by_cpg(df):
    """Create lineplot of statistics by CpG"""
    mean = df.mean(axis=1)

    fig, ax = plt.subplots(figsize=(5, 5))
    plt.tight_layout()

    ax.violinplot(mean, widths=0.1, showmeans=True, showmedians=True)

    plt.title('Mean Methylation Levels Across All CpGs')
    plt.xlabel('CpG')
    plt.ylabel('Methylation Level')

    plt.xlim(0.8,1.2)
    plt.ylim(0, 1.05)
    plt.xticks([])

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
    by_cpg(df_raw)

    return None

if __name__ == '__main__':
    fname = 'example_data.tsv'

    if os.path.exists(fname):
        logger.info(f'Reading preprocessed data file: {fname}')
        df = pd.read_csv(fname, sep='\t', index_col=['chr', 'start'])
        main(df)
    else:
        logger.error('B_preprocess_data.py has not been run. Run and try again!')
