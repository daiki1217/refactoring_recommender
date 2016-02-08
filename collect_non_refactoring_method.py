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
        random_commit = random.choice(commits)
        if len(random_commit.parents) >= 2 or not random_commit.parents:
            continue
        p = random_commit.parents[0]
        method_candidates = []
        for f in p.tree.traverse():
            if f.type == 'blob':
                if is_method_body(f.path) or is_constructor_body(f.path):
                    assert f.path.split('/')[0].endswith('.java')
                    method_candidates.append(f.path)

        non_refactoring_methods.append(random.choice(method_candidates))
        extract_method_information = detect_extract_method_from_commit(p, random_commit, historage)
        if any((e['extracted_method_path'] == non_refactoring_methods[-1] for e in extract_method_information)):
            non_refactoring_methods.pop(-1)
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
