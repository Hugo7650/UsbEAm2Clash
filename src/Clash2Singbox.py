#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import argparse
import json
from pathlib import Path

import yaml


def convert_rules(source_root: Path, output_root: Path):
    output_root.mkdir(exist_ok=True, parents=True)
    source_files = sorted(source_root.rglob('*.yaml'))

    if not source_files:
        raise FileNotFoundError(f'No YAML rule files found under {source_root}')

    for source_file in source_files:
        try:
            content = yaml.safe_load(source_file.read_text(encoding='utf-8'))
        except yaml.YAMLError as error:
            raise ValueError(f'Invalid YAML in {source_file}: {error}') from error

        if not isinstance(content, dict) or 'payload' not in content:
            raise ValueError(f'Missing payload in {source_file}')

        domains = content['payload']
        if not isinstance(domains, list) or not all(isinstance(domain, str) for domain in domains):
            raise ValueError(f'Payload must be a list of strings in {source_file}')

        relative_path = source_file.relative_to(source_root).with_suffix('.json')
        output_file = output_root / relative_path
        output_file.parent.mkdir(exist_ok=True, parents=True)

        rules = [{'domain': domains}] if domains else []
        output_file.write_text(
            json.dumps({'version': 3, 'rules': rules}, ensure_ascii=False, indent=2) + '\n',
            encoding='utf-8',
        )


def main():
    parser = argparse.ArgumentParser(description='Convert Clash domain YAML rules to sing-box JSON rules')
    parser.add_argument('--source', type=Path, default=Path('Clash'), help='Clash YAML source directory')
    parser.add_argument('--output', type=Path, default=Path('Sing-box'), help='sing-box JSON output directory')
    args = parser.parse_args()

    convert_rules(args.source, args.output)


if __name__ == '__main__':
    main()
