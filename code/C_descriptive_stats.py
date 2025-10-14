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

    # TODO: Add xtick labels with sample names turned 90 degrees
    # TODO: Fix y-axis ticks and range

    plt.savefig('stats_by_sample.pdf', bbox_inches='tight')
    plt.close('all')

    return None

def by_cpg(df):
    """Create lineplot of statistics by CpG"""
    # TODO: Rethink how I might want to show this. WAY too many points to plot
    x = range(len(df))
    mean = df.mean(axis=1)
    std = df.std(axis=1)

    fig, ax = plt.subplots(figsize=(10, 5))
    plt.tight_layout()

    ax.plot(x, mean, '-')
    ax.fill_between(x, mean - std, mean + std, alpha=0.2)

    plt.title('Mean Methylation Level Across All CpGs')
    plt.xlabel('CpG')
    plt.ylabel('Methylation Level')

    plt.savefig('stats_by_cpg.pdf', bbox_inches='tight')
    plt.close('all')

    return None

def main(fname):
    """Calculate and plot descriptive statistics from preprocessed data"""
    logger.info(f'Reading preprocessed data file: {fname}')
    df = pd.read_csv(fname, sep='\t', index_col=['chr', 'start'])

    by_sample(df)

    by_cpg(df)

    return None

if __name__ == '__main__':
    fname = 'example_data.tsv'
    if os.path.exists(fname):
        main(fname)
    else:
        logger.error('B_preprocess_data.py has not been run. Run and try again!')
