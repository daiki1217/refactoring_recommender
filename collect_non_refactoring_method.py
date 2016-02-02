from git.repo import Repo
from kenja.historage import *
import random
from kenja.detection.extract_method import *

def collect_non_refactoring_method(historage, num_of_methods):
    non_refactoring_methods = []

    commits = []
    for ref in get_refs(historage):
        commits.extend(list(historage.iter_commits(ref)))

    while len(non_refactoring_methods) < num_of_methods:
        random_commit = commits[random.randint(0, len(commits) - 1)]
        if not random_commit.parents:
            continue
        p = random_commit.parents[0]
        extract_method_information = detect_extract_method_from_commit(p, random_commit, historage)
        for f in p.tree.trees[random.randint(0, len(p.tree.trees) - 1)].traverse():
            if f.type == 'blob':
                if is_method_body(f.path) or is_constructor_body(f.path):
                    if is_method_body(f.path):
                        method = get_method(f.path)
                    else:
                        method = get_constructor(f.path)
                    method_information = get_method_information(method)

                    if extract_method_information:
                        for e in extract_method_information:
                            if e['extracted_method_path'] == f.path:
                                del method
                        if method:
                            non_refactoring_methods.append(method_information)
                            break
                    else:
                        non_refactoring_methods.append(method_information)
                        break

    return non_refactoring_methods


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Non Refactoring Method Collecter')
    parser.add_argument('historage_dir', help='path of historage repository dir')
    parser.add_argument('num_of_methods', help='the number of methods that you want to collect')
    args = parser.parse_args()

    historage = Repo(args.historage_dir)
    num_of_methods = int(args.num_of_methods)
    print collect_non_refactoring_method(historage, num_of_methods)

