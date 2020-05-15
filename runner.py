import argparse

from app import main, utils

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--rows_number', type=int, default=4)
    parser.add_argument('--cols_number', type=int, default=4)
    parser.add_argument('--debug', type=utils.str2bool, default=True)
    args = parser.parse_args()
    main.run(args)
