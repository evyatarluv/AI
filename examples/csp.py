import os
from pathlib import Path
import yaml

# Project root directory
root_directory = Path(__file__).parent.parent


def main():

    # Load configuration file
    config_path = os.path.join(root_directory, 'CSP/config.yaml')
    config = yaml.full_load(open(config_path))





if __name__ == '__main__':

    main()