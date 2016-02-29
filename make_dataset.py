import csv
import sys
from kenja.historage import *
from collect_non_refactoring_method import *
from git.repo import Repo


dataSet = []
Id = 1


def shape_refactored_methods(data):
    result = []
    global Id

    csv_file = open(data, 'r')
    refactored_methods = csv.DictReader(csv_file)

    for r in refactored_methods:
        refactored_method_data = {
            'Id': Id,
            'method': r['extracted_method'],
            'class': r['target_class'],
            'package': r['b_package'].rstrip(),
            'commit': r['b_commit'],
            'category': 1
        }
        Id += 1
        result.append(refactored_method_data)

    csv_file.close()
    return result


def shape_non_refactored_methods(data):
    result = []
    global Id

    for n in data:
        non_refactored_method_data = {
            'Id': Id,
            'method': get_method_information(get_method(n[1]) if is_method_body(n[1]) else get_constructor(n[1]))[0],
            'class': get_class(n[1]),
            'package': get_package(n[1], n[0]),
            'commit': n[0].hexsha,
            'category': 0
        }
        Id += 1
        result.append(non_refactored_method_data)

    return result


def print_csv(output_file):
    fieldnames = (
        'Id',
        'method',
        'class',
        'package',
        'commit',
        'category'
    )

    f = open(output_file, 'w')
    writer = csv.DictWriter(f, fieldnames, lineterminator="\n")
    writer.writeheader()
    writer.writerows(dataSet)
    f.close()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='DataSet Maker')
    parser.add_argument('historage_dir', help='path of historage repository dir')
    parser.add_argument('refactored_methods', help='path of csv file which kenja output')
    parser.add_argument('output_file', help='path of output file')
    args = parser.parse_args()

    historage = Repo(args.historage_dir)
    dataSet.extend(shape_refactored_methods(args.refactored_methods))
    dataSet.extend(shape_non_refactored_methods(collect_non_refactoring_method(historage, len(dataSet))))
    print_csv(args.output_file)
