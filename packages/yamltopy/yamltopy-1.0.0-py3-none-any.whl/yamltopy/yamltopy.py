#!/usr/bin/env python3

"""
yaml-to-py 0.0.1

A CLI tool to convert YAML file to Python module for better load performance

More info: http://github.com/szikszail/yamltopy
"""

import argparse
import errno
import logging
import os
import yaml

logger = logging.getLogger('yamltopy')


def load_yaml(file):
    logger.info('Loading YAML file: %s', file)
    with open(file, 'r', encoding='utf-8') as f:
        return yaml.load(f, yaml.FullLoader)


def generate_py_content(name, data):
    logger.info('Exported variable will be: %s', name)
    content = []
    if "datetime" in str(data):
        content.append('import datetime')
    content.append(f'{name} = {data}')
    content.append('')
    return '\n'.join(content)


def save_py(file, content):
    logger.info('Saving PY file: %s', file)
    folder = os.path.dirname(file)
    if folder and not os.path.exists(folder):
        try:
            os.makedirs(folder)
        except OSError as exc:
            if exc.errno != errno.EEXIST:
                raise
    with open(file, 'w', encoding='utf-8', ) as f:
        f.write(content)


def main():
    parser = argparse.ArgumentParser(
        description='Convert YAML configuration file to a Python module'
        'for better performance'
    )

    parser.add_argument('-i', '--input', default='input.yml',
                        help='The input Yaml file (YML or YAML)')

    parser.add_argument('-o', '--output', default='output.py',
                        help='The output Py file')

    parser.add_argument('-n', '--name', default='DATA',
                        help='The name of the exported variable containg the Yaml data')

    parser.add_argument('-v', '--verbose', default=False, action='store_true')

    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.INFO)
    data = load_yaml(args.input)
    content = generate_py_content(args.name, data)
    save_py(args.output, content)


if __name__ == "__main__":
    main()
