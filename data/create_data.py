import argparse
import random

import pandas as pd

# Set seed for reproducibility
random.seed(2025)

# How to download file:
#
# wget https://github.com/huishenlab/biscuit/releases/download/v1.7.1.20250908/hg38_biscuit_qc_assets.zip
# unzip hg38_biscuit_qc_assets.zip
# cd hg38
# rsync cpg.bed.gz /path/to/your/working/directory
def read_cpg_bed(bed_name):
    """Read CpG BED file and pull out chromosome 21 as our test chromosome"""
    df = pd.read_csv(bed_name, sep='\t', names=['chr', 'start', 'end'])

    # Restrict to smallest autosomal chromosome
    df.drop(df[~df['chr'].str.startswith('chr21')].index, inplace=True)
    df.reset_index(inplace=True, drop=True)

    return df

def random_covg():
    """Produce a random coverage value"""
    x = int(random.gauss(mu=20, sigma=5))
    if x < 1:
        x = 1

    return x

def run_simulation(cpgs):
    """Select random set of CpGs, simulate coverage methylation levels"""
    covg = [] # Number of reads spanning the CpG
    beta = [] # Fraction of cytosines that are methylated
    ctxt = [] # Distribution of covg/beta that comes from forward and reverse strands
    for _ in range(len(cpgs)):
        cv = random_covg()
        bt = round(random.binomialvariate(cv, p=0.7) / cv, 3)
        ct = f'C:{bt:.3f}:{cv},G:.:0'

        covg.append(cv)
        beta.append(bt)
        ctxt.append(ct)

    df = cpgs.copy(deep=True)
    df['beta'] = beta
    df['covg'] = covg
    df['ctxt'] = ctxt

    return df

def create_metadata(n, cell_types):
    """Create a mock metadata sheet for the example data"""
    # Columns that are needed for metadata
    data = {
        'WGBS_ID': [],
        'tumor_id': [],
        'cluster': [],
        'matched_epi_str': [],
        'sample': [],
        'age': [],
        'os_years': [],
        'xtic': [],
        'cellType': [],
        'histotype': [],
        'anatomic_site': [],
        'site': [],
        'Stage': [],
        'Stage_full': [],
        'Grade': [],
        'MillionReadsMapped_Methylation': [],
        'CpA.Retention': [],
        'CpC.Retention': [],
        'CpG.Retention': [],
        'CpT.Retention': [],
        'cpgi.beta': [],
        'solo.wcgw.beta': [],
        'gene.counts': [],
        'MIR200cAvgBeta': [],
        'MIR200CHG': [],
    }

    # Simulate that most, but not all, samples are used in analysis
    samples = random.sample(range(n), n-2)

    # Set some choices to select from
    xtic_choices = ['Normal', 'HGSC-like', 'CCOC-like', 'ENOC-like']
    histo_choices = ['ENOC', 'HGSC', 'CCOC']
    site_choices = [('Ovary', 'Ovary'), ('Omentum', 'Non-ovary'), ('Endometrium', 'Non-ovary')]
    stage_choices = ['I', 'II', 'III']

    for samp in samples:
        cell_type = cell_types[samp]
        data['WGBS_ID'].append(f'{samp:>02}a{cell_type}')
        data['tumor_id'].append(f'{samp}')
        data['cluster'].append('S{}'.format(random.randint(1, 4)))
        data['matched_epi_str'].append('none')
        data['sample'].append(f'{samp:>02}a{cell_type}')
        data['age'].append(random.randrange(40000, 75000) / 10000)
        data['os_years'].append(random.randrange(500, 25000) / 10000)
        data['xtic'].append(random.choice(xtic_choices))
        data['cellType'].append('stromal' if cell_type == 'S' else 'epithelial')
        data['histotype'].append(random.choice(histo_choices))

        site = random.choice(site_choices)
        data['anatomic_site'].append(site[0])
        data['site'].append(site[1])

        stage = random.choice(stage_choices)
        data['Stage'].append(stage)
        data['Stage_full'].append('{}{}'.format(stage, random.choice(['A', 'B', 'C'])))

        data['Grade'].append(random.randint(1,3))
        data['MillionReadsMapped_Methylation'].append(random.randrange(2000, 12000) / 10)
        data['CpA.Retention'].append(random.random())
        data['CpC.Retention'].append(random.random())
        data['CpG.Retention'].append(random.randrange(60000, 80000) / 1000)
        data['CpT.Retention'].append(random.random())
        data['cpgi.beta'].append(random.randrange(20000, 30000) / 1000)
        data['solo.wcgw.beta'].append(random.randrange(55000, 60000) / 1000)
        data['gene.counts'].append(1000000 * random.random())
        data['MIR200cAvgBeta'].append(random.random())
        data['MIR200CHG'].append(random.randrange(0, 100) / 10)

    return pd.DataFrame(data)

def parse_args():
    """Command line arguments"""
    parser = argparse.ArgumentParser(
        prog='create_data.py',
        description='Create example data for CIS 635 project'
    )

    parser.add_argument('cpg_bed', help='CpG location BED file')

    return parser.parse_args()

def main():
    # Command line arguments
    args = parse_args()

    # Select CpGs to simulate
    cpgs = read_cpg_bed(args.cpg_bed)

    # Number of samples
    N = 12

    # Simulate samples
    cell_types = []
    for n in range(N):
        df = run_simulation(cpgs)
        cell_type = random.choice(['S', 'E'])
        cell_types.append(cell_type)

        df.to_csv(f'{n:>02}a{cell_type}_mergecg.bed.gz', sep='\t', index=False, header=False)

    # Create metadata
    meta = create_metadata(N, cell_types)
    meta.to_csv('metadata.tsv', sep='\t', index=False)

if __name__ == '__main__':
    main()
