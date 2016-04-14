import csv
import sys
from kenja.historage import get_method, is_method_body, get_constructor, get_class
from kenja.detection.extract_method import get_method_information
from collect_non_refactoring_method import *
from git.repo import Repo


dataSet = []
Id = 1


def get_package(path, commit):
    split_path = path.split('/')
    path = '/'.join((split_path[0], 'package'))
    try:
        package_blob = commit.tree / path
    except KeyError:
        return None
    return package_blob.data_stream.read()


def shape_refactored_methods(data):
    result = []
    global Id

    csv_file = open(data, 'r')
    refactored_methods = csv.DictReader(csv_file)

    for r in refactored_methods:
        refactored_method_data = {
            'Id': Id,
            'method': get_method_information(r['target_method'])[0],
            'class': r['target_class'],
            'package': r['a_package'].rstrip(),
            'commit': r['a_commit'],
            'category': 1
        }
        Id += 1
        result.append(refactored_method_data)

    csv_file.close()
    return result


def shape_non_refactored_methods(historage, data):
    result = []
    global Id

    for n in data:
        non_refactored_method_data = {
            'Id': Id,
            'method': get_method_information(get_method(n[1]))[0] if is_method_body(n[1]) else get_method_information(get_constructor(n[1]))[0],
            'class': get_class(n[1]),
            'package': get_package(n[1], historage.commit(n[0])).rstrip() if get_package(n[1], historage.commit(n[0])) != None else get_package(n[1], historage.commit(n[0])),
            'commit': n[0].hexsha,
            'category': 0
        }
        Id += 1
        result.append(non_refactored_method_data)

    return result


def shape_inline_refactored_methods(data):
    result = []
    global Id

    csv_file = open(data, 'r')
    inline_refactored_methods = csv.DictReader(csv_file)

    for i in inline_refactored_methods:
        inline_refactored_method_data = {
            'Id': Id,
            'method': get_method_information(i['target_method'])[0],
            'class': i['target_class'],
            'package': i['b_package'].rstrip(),
            'commit': i['b_commit'],
            'category': 2
        }
        Id += 1
        result.append(inline_refactored_method_data)

    csv_file.close()
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
    parser.add_argument('-i', '--inline', help='path of inline methods csv file')
    parser.add_argument('refactored_methods', help='path of csv file which kenja output')
    parser.add_argument('output_file', help='path of output file')
    args = parser.parse_args()

    historage = Repo(args.historage_dir)

    if args.inline:
        dataSet.extend(shape_inline_refactored_methods(args.inline))
    else:
        dataSet.extend(shape_refactored_methods(args.refactored_methods))
        dataSet.extend(shape_non_refactored_methods(historage, collect_non_refactoring_method(historage, len(dataSet))))

    print_csv(args.output_file)
