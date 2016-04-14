import csv
from BeautifulSoup import BeautifulStoneSoup
from kenja.historage import *
from kenja.detection.extract_method import *
from git.repo import Repo
import datetime
import time
from math import fabs
import os


method_metric_names = ['PAR', 'VG', 'NBD', 'MLOC']
class_metric_names = ['WMC', 'DIT', 'LCOM', 'NSC']


def generate_feature_vector(dataset_csv, metrics):
    result = []

    for d in dataset:
        for f in os.listdir(metrics):
            if f.startswith(d['commit']):
                xml = open(metrics + f, 'r')
                result.append(get_metrics_from_xml(BeautifulStoneSoup(xml.read()), d))
                xml.close()
                break


    return result


def get_metrics_from_xml(metrics, method_information):
    method_metrics = {}

    package_name = method_information['package']
    class_name = method_information['class']
    method_name = method_information['method']
    method_metrics['Id'] = method_information['Id']
    method_metrics['category'] = method_information['category']

    for metric in metrics.findAll('metric'):
        for method_metric_name in method_metric_names:
            if method_metric_name == metric.get('id'):
                for v in metric.findAll('value'):
                    if package_name == v.get('package') and class_name == v.get('source').split('.')[0] and method_name == v.get('name'):
                        method_metrics[method_metric_name] = v.get('value')
                        break

        for class_metric_name in class_metric_names:
            if class_metric_name == metric.get('id'):
                for v in metric.findAll('value'):
                    if package_name == v.get('package') and class_name == v.get('source').split('.')[0]:
                        method_metrics[class_metric_name] = v.get('value')
                        break


    return method_metrics


def print_csv(data, output_file):
    fieldnames = (
        'Id',
        'category',
        'PAR',
        'VG',
        'NBD',
        'MLOC',
        'WMC',
        'DIT',
        'LCOM',
        'NSC'
    )

    f = open(output_file, 'w')
    writer = csv.DictWriter(f, fieldnames, lineterminator="\n")
    writer.writeheader()
    writer.writerows(data)
    f.close()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Feature Vector Generater')
    parser.add_argument('dataset', help='path of dataset which include refactored_methods and non_refactored_methods')
    parser.add_argument('metrics', help='path of metrics files')
    parser.add_argument('output_file', help='path of output file')
    args = parser.parse_args()

    dataset_csv = open(args.dataset, 'r')
    dataset = csv.DictReader(dataset_csv)
    print_csv(generate_feature_vector(dataset, args.metrics), args.output_file)

    dataset_csv.close()
