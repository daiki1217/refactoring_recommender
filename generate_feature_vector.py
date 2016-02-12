import csv
import uuid
from BeautifulSoup import BeautifulStoneSoup
from kenja.historage import *
from kenja.detection.extract_method import *

metric_names = ['PAR']


def get_metrics_from_xml(metrics, method_information):
    method_metrics = {}

    package_name = method_information['b_package']
    class_name = method_information['target_class']
    method_name = method_information['extracted_method']

    for metric in metrics.findAll('metric'):
        for metric_name in metric_names:
            if metric_name == metric.get('id'):
                for v in metric.findAll('value'):
                    if package_name == v.get('package') or class_name == v.get('source').split('.')[0] or method_name == v.get('name'):
                        method_metrics[metric_name] = v.get('value')
                        break

    return method_metrics


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Feature Vector Generater')
    parser.add_argument('refactored_methods', help='path of csv file which kenja output')
    parser.add_argument('metrics', help='path of metrics file')
    args = parser.parse_args()

    csv_file = open(args.refactored_methods, 'r')
    refactored_methods = csv.DictReader(csv_file)
    xml_file = open(args.metrics, 'r')
    metrics = BeautifulStoneSoup(xml_file.read())

    for m in refactored_methods:
        print get_metrics_from_xml(metrics, m)

    csv_file.close()
    xml_file.close()
