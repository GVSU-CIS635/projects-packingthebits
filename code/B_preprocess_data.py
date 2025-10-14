from multiprocessing import Pool
import gzip
import glob
import os

import pandas as pd

def get_sample_name(fname):
    """Extract sample name from file name"""
    base = os.path.basename(fname)
    return base.replace('_mergecg.bed.gz', '')


def read_file(fname):
    """Read and preprocess BED file"""
    samp = get_sample_name(fname)

    df = pd.read_csv(
        fname,
        sep='\t',
        names=['chr', 'start', 'end', f'{samp}', 'covg', 'context'],
        usecols=['chr', 'start', f'{samp}', 'covg']
    )

    # Require minimum coverage of 10 and restrict to canonical chromosomes
    df.drop(df[(df['covg'] < 10) | (~df['chr'].str.startswith('chr'))].index, inplace=True)

    # Only need coverage column to do filter, drop so we don't carry it around during analysis
    df.drop(columns='covg', inplace=True)

    # Set index levels
    df.set_index(['chr', 'start'], inplace=True)

    return df

def read_metadata(fname):
    """Read metadata TSV file"""
    df = pd.read_csv(
        fname,
        sep='\t',
        usecols=[
            'WGBS_ID',
            'tumor_id',
            'cluster',
            'matched_epi_str',
            'sample',
            'age',
            'os_years',
            'xtic',
            'cellType',
            'histotype',
            'anatomic_site',
            'site',
            'Stage',
            'Stage_full',
            'Grade',
            'MillionReadsMapped_Methylation',
            'CpA.Retention',
            'CpC.Retention',
            'CpG.Retention',
            'CpT.Retention',
            'cpgi.beta',
            'solo.wcgw.beta',
            'gene.counts',
            'MIR200cAvgBeta',
            'MIR200CHG',
        ]
    )

    return df

def process_files(dir, n_processes, meta_name):
    """Pull out files in directory and process them in parallel"""
    # Metadata (defines which samples we want to keep)
    meta = read_metadata(meta_name)

    # Not the most efficient way to do this, but it gets the job done
    files = []
    for f in glob.glob(f'{dir}/*.gz'):
        if get_sample_name(f) in list(meta['WGBS_ID']):
            files.append(f)

    with Pool(processes=n_processes) as pool:
        dfs = pool.map(read_file, files)

    # To address missing data, use only data that is included in all samples
    df = dfs[0].join(dfs[1:], how='inner')

    return df

def main(dir, n_processes, meta_name, oname):
    """Main preprocessing function"""
    df = process_files(dir, n_processes, meta_name)

    if len(oname) > 0:
        df.to_csv(oname, sep='\t')

    return df

if __name__ == '__main__':
    main('../data', 1, '../data/metadata.tsv', '')
