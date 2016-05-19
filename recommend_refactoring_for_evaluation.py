import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import train_test_split, cross_val_score, KFold
from sklearn.metrics import accuracy_score
from pandas import DataFrame
from sklearn.metrics import classification_report, precision_recall_fscore_support
from texttable import Texttable


table = Texttable()


def init_table():
    table.set_deco(Texttable.HEADER)
    table.set_cols_dtype(['t', 'i', 'i', 'f', 'f', 'f', 'f', 'f', 'f', 'f'])
    table.add_row(["model", "c0 example", "c1 example", "c0 precision", "c1 precision", "c0 recall", "c1 recall", "c0 f-score", "c1 f-score", "accuracy"])
    table.set_cols_width([12, 11, 11, 11, 11, 11, 11, 11, 11, 11])
    table.set_cols_align(['l', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r', 'r'])


def cross_val(clf, df, K, model_name, random_state=0):
    X = df[['PAR', 'VG', 'NBD', 'MLOC', 'WMC', 'DIT', 'LCOM', 'NSC']]
    y = df['category']
    target_names = ['class 0', 'class 1']
    precisions0 = []
    precisions1 = []
    recalls0 = []
    recalls1 = []
    fscores0 = []
    fscores1 = []
    cv = KFold(len(y), K, shuffle=True, random_state=random_state)

    for train_index, test_index in cv:
        X_train, X_test = X.ix[train_index, :], X.ix[test_index, :]
        y_train, y_test = y.ix[train_index], y.ix[test_index]
        clf.fit(X_train, y_train)
        y_pred = clf.predict(X_test)
        #print(classification_report(y_test, y_pred, target_names=target_names))
        scores = precision_recall_fscore_support(y_test, y_pred, pos_label=1)
        precisions0.append(scores[0][0])
        precisions1.append(scores[0][1])
        recalls0.append(scores[1][0])
        recalls1.append(scores[1][1])
        fscores0.append(scores[2][0])
        fscores1.append(scores[2][1])

    #print ('[precision for class0]'), np.average(precisions0)
    #print ('[precision for class1]'), np.average(precisions1)
    #print ('[recall for class0]'), np.average(recalls0)
    #print ('[recall for class1]'), np.average(recalls1)
    #print ('[F1-score for class0]'), np.average(fscores0)
    #print ('[F1-score for class1]'), np.average(fscores1)
    scores = cross_val_score(clf, X, y, cv=cv)
    #print ('[accuracy]:'),

    table.add_row([model_name, len(df.ix[df['category'] == 0, :]), len(df.ix[df['category'] == 0, :]), np.average(precisions0), np.average(precisions1), np.average(recalls0), np.average(recalls1), np.average(fscores0), np.average(fscores1), scores.mean()])
    return scores


def construct_dataframe(positive, negative):
    if len(positive) > len(negative):
        positive = positive.take(np.random.permutation(len(positive))[:len(negative)])
    elif len(positive) < len(negative):
        negative = negative.take(np.random.permutation(len(negative))[:len(positive)])
    df = pd.concat([positive, negative]).reset_index(drop=True)

    #print ("[positive example]: " + str(len(df.ix[df['category'] == 1, :])) + "\t [negative example]: " + str(len(df.ix[df['category'] == 0, :])))

    return df


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Refactoring Recommender')
    parser.add_argument('extract_method_feature_vectors', help='path of extract method feature vectors csv file')
    parser.add_argument('inline_method_feature_vectors', help='path of inline method feature vectors csv file')
    args = parser.parse_args()

    init_table()
    df_extract_and_random = pd.read_csv(args.extract_method_feature_vectors)
    df_extract = df_extract_and_random.ix[df_extract_and_random['category'] == 1, :]
    df_random = df_extract_and_random.ix[df_extract_and_random['category'] == 0, :]
    df_inline = pd.read_csv(args.inline_method_feature_vectors)
    df_inline_reverse = df_inline.copy()
    df_inline_reverse['category'] = 1

    #print ('---extract and random---')
    cross_val(LogisticRegression(), construct_dataframe(df_extract, df_random), 10, "[extract and random]").mean()

    #print ('---extract(=inline) and random---')
    df = df_extract.take(np.random.permutation(len(df_extract))[:len(df_inline)])
    cross_val(LogisticRegression(), construct_dataframe(df, df_random), 10, "[extract(=inline) and random]").mean()

    #print ('---extract and inline---')
    cross_val(LogisticRegression(), construct_dataframe(df_extract, df_inline), 10, "[extract and inline]").mean()

    #print ('---inline and random---')
    cross_val(LogisticRegression(), construct_dataframe(df_inline_reverse, df_random), 10, "[inline and random]").mean()

    #print ('---extract and (inline and random)---')
    df = df_random.take(np.random.permutation(len(df_random))[:len(df_extract) - len(df_inline)])
    df = pd.concat([df, df_inline])
    cross_val(LogisticRegression(), construct_dataframe(df_extract, df), 10, "[extract and (inline and random)]").mean()

    #print ('---(extract and inline) and random---')
    df = df_extract.take(np.random.permutation(len(df_extract))[:len(df_random) - len(df_inline_reverse)])
    df = pd.concat([df, df_inline_reverse])
    cross_val(LogisticRegression(), construct_dataframe(df, df_random), 10, "[(extract and inline) and random]").mean()

    print table.draw()
