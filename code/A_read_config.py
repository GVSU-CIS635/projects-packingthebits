import tomllib

import project_logger

logger = project_logger.create_logger('read_config')

def read_config(cname):
    """Read config TOML file"""
    logger.info(f'Loading config file: {cname}')

    with open(cname, 'rb') as fh:
        conf = tomllib.load(fh)

    return conf

if __name__ == '__main__':
    conf = read_config('config.toml')
    logger.info(f'Configuration: {conf}')
