import argparse
import os

import pandas as pd

import project_logger
import A_read_config as read_config
import B_preprocess_data as preprocess_data
import C_descriptive_stats as descriptive_stats
import D_dissimilarity as dissimilarity
import E_pca as pca

logger = project_logger.create_logger('main')

def parse_args():
    """Parse command line options"""
    parser = argparse.ArgumentParser(
        prog='analyze_meth_data',
        description='Analyze DNA methylation data',
    )

    parser.add_argument('-c', '--config', default='config.toml', help='name of TOML config file')

    return parser.parse_args()

def get_data(conf):
    """Read preprocessed TSV if available, otherwise create"""
    if os.path.exists(conf['preprocessed_file']):
        logger.info(f'Using existing preprocessed file: {conf["preprocessed_file"]}')
        return pd.read_csv(
            conf['preprocessed_file'],
            sep='\t',
            index_col=['chr', 'start']
        )

    logger.info('Cannot determine if data has been preprocessed - preprocessing now')
    return preprocess_data.main(
        conf['data_dir'],
        conf['n_processes'],
        conf['meta_file'],
        conf['preprocessed_file']
    )

def main():
    """Main entry point for program"""
    # Parse command line arguments
    args = parse_args()

    # Run time configuration
    conf = read_config.read_config(args.config)

    # Read and preprocess data
    df = get_data(conf)

    # Setup metadata DataFrame
    meta = pd.read_csv(conf['meta_file'], sep='\t')

    # Do analysis and visualization portions of pipeline
    descriptive_stats.main(df)
    dissimilarity.main(df)
    pca.main(df, meta)

    return None

if __name__ == '__main__':
    main()
