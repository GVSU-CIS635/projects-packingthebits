import tomllib

def read_config(cname):
    """Read config TOML file"""
    with open(cname, 'rb') as fh:
        conf = tomllib.load(fh)

    return conf

if __name__ == '__main__':
    conf = read_config('config.toml')
    print(conf)
