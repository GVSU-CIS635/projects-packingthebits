import argparse
import os

import pandas as pd

import project_logger
import A_read_config as read_config
import B_preprocess_data as preprocess_data

logger = project_logger.create_logger('main')

def parse_args():
    """Parse command line options"""
    parser = argparse.ArgumentParser(
        prog='analyze_meth_data',
        description='Analyze DNA methylation data',
    )

    parser.add_argument('-c', '--config', default='config.toml', help='name of TOML config file')

    return parser.parse_args()

def main():
    """Main entry point for program"""
    # Parse command line arguments
    args = parse_args()

    # Run time configuration
    conf = read_config.read_config(args.config)

    # Read and preprocess data
    df = None
    if len(conf['preprocessed_file']) > 0 and os.path.exists(conf['preprocessed_file']):
        logger.info(f'Using existing preprocessed file: {conf["preprocessed_file"]}')
        df = pd.read_csv(conf['preprocessed_file'], sep='\t', index_col=['chr', 'start'])
    else:
        logger.info('Cannot determine if data has been preprocessed - preprocessing now')
        df = preprocess_data.main(conf['data_dir'], conf['n_processes'], conf['meta_file'], conf['preprocessed_file'])

    print(df)

    return None

if __name__ == '__main__':
    main()
