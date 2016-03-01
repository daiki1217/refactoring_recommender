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


def generate_feature_vector(historage, dataset_csv, metrics, args_jedit_tag_info):
    result = []

    for d in dataset:
        min = 10000000000
        jedit_tag_info_csv = open(args_jedit_tag_info, 'r')
        jedit_tag_info = csv.DictReader(jedit_tag_info_csv)
        for tag in jedit_tag_info:
            tagTime = datetime.datetime.strptime(tag['commit_date'], '%Y/%m/%d')
            tagTime_unix = int(time.mktime(tagTime.timetuple()))
            if fabs(historage.commit(d['commit']).committed_date - tagTime_unix) < min:
                min = fabs(historage.commit(d['commit']).committed_date - tagTime_unix)
                tag_candidate = tag['tag']
        jedit_tag_info_csv.close()

        for f in os.listdir(metrics):
            if tag_candidate in f:
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
                    if class_name == v.get('source').split('.')[0] and method_name == v.get('name'):
                        method_metrics[method_metric_name] = v.get('value')
                        break

        for class_metric_name in class_metric_names:
            if class_metric_name == metric.get('id'):
                for v in metric.findAll('value'):
                    if class_name == v.get('source').split('.')[0]:
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
    parser.add_argument('historage_dir', help='path of historage repository dir')
    parser.add_argument('dataset', help='path of dataset which include refactored_methods and non_refactored_methods')
    parser.add_argument('metrics', help='path of metrics files')
    parser.add_argument('jedit_tag_info', help='path of jedit_tag_info.csv')
    parser.add_argument('output_file', help='path of output file')
    args = parser.parse_args()

    historage = Repo(args.historage_dir)
    dataset_csv = open(args.dataset, 'r')
    dataset = csv.DictReader(dataset_csv)
    print_csv(generate_feature_vector(historage, dataset, args.metrics, args.jedit_tag_info), args.output_file)

    dataset_csv.close()
