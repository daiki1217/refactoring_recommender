import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.cross_validation import train_test_split, cross_val_score, KFold
from sklearn.metrics import accuracy_score
from pandas import DataFrame


def cross_val(clf, X, y, K, random_state=0):
    cv = KFold(len(y), K, shuffle=True, random_state=random_state)
    scores = cross_val_score(clf, X, y, cv=cv)
    return scores


def predict_refactoring_with_own_for_train_and_test(data, explained_variable):
    clf = LogisticRegression()
    scores = cross_val(clf, X, y, 10)
    print scores, scores.mean()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Refactoring Recommender')
    parser.add_argument('feature_vectors', help='path of feature vectors csv file')
    parser.add_argument('-i', '--inline', help='path of inline methods csv file')
    args = parser.parse_args()

    df = pd.read_csv(args.feature_vectors)

    if args.inline:
        df_inline = pd.read_csv(args.inline)
        X_inline = df_inline[['PAR', 'VG', 'NBD', 'MLOC', 'WMC', 'DIT', 'LCOM', 'NSC']]
        y_inline = df_inline['category']

        df_refactored_method_all = df.ix[df['category'] == 1, :]
        df_refactored_method = df_refactored_method_all.take(np.random.permutation(len(df_refactored_method_all))[:len(df_inline)])
        df_refactored_method_and_inline = pd.concat([df_refactored_method, df_inline])
        X_refactored_method_and_inline = df_refactored_method_and_inline[['PAR', 'VG', 'NBD', 'MLOC', 'WMC', 'DIT', 'LCOM', 'NSC']]
        y_refactored_method_and_inline = df_refactored_method_and_inline['category']
        X_refactored_method_and_inline_train, X_refactored_method_and_inline_val, y_refactored_method_and_inline_train, y_refactored_method_and_inline_val = train_test_split(X_refactored_method_and_inline, y_refactored_method_and_inline, train_size=0.8, random_state=1)
        clf_inline = LogisticRegression()
        clf_inline.fit(X_refactored_method_and_inline, y_refactored_method_and_inline)

        df_random_method_all = df.ix[df['category'] == 0, :]
        df_random_method = df_random_method_all.take(np.random.permutation(len(df_random_method_all))[:len(df_inline)])
        df_equal = pd.concat([df_refactored_method, df_random_method])
        X_equal = df_equal[['PAR', 'VG', 'NBD', 'MLOC', 'WMC', 'DIT', 'LCOM', 'NSC']]
        y_equal = df_equal['category']
        clf_equal = LogisticRegression()
        clf_equal.fit(X_equal, y_equal)

        df_inline_reverse = df_inline
        df_inline_reverse['category'] = 1
        df_inline_reverse_random = pd.concat([df_inline_reverse, df_random_method])
        X_inline_reverse_random = df_inline_reverse_random[['PAR', 'VG', 'NBD', 'MLOC', 'WMC', 'DIT', 'LCOM', 'NSC']]
        y_inline_reverse_random = df_inline_reverse_random['category']
        clf_inline_reverse_random = LogisticRegression()
        clf_inline_reverse_random.fit(X_inline_reverse_random, y_inline_reverse_random)
        df_inline_reverse['category'] = 0

        df_non_refactored_method_all = df.ix[df['category'] == 0, :]
        df_non_refactored_method = df_non_refactored_method_all.take(np.random.permutation(len(df_non_refactored_method_all))[:len(df_refactored_method_all) - len(df_inline)])
        df_refactored_method_and_non_and_inline = pd.concat([df_refactored_method_all, df_non_refactored_method, df_inline])
        X_refactored_method_and_non_and_inline = df_refactored_method_and_non_and_inline[['PAR', 'VG', 'NBD', 'MLOC', 'WMC', 'DIT', 'LCOM', 'NSC']]
        y_refactored_method_and_non_and_inline = df_refactored_method_and_non_and_inline['category']
        clf_random_and_inline = LogisticRegression()
        clf_random_and_inline.fit(X_refactored_method_and_non_and_inline, y_refactored_method_and_non_and_inline)

        df_inline_reverse = df_inline
        df_inline_reverse['category'] = 1
        df_refactored_method = df_refactored_method_all.take(np.random.permutation(len(df_refactored_method_all))[:len(df_random_method_all) - len(df_inline)])
        df_extractInline_and_random = pd.concat([df_refactored_method, df_inline_reverse, df_random_method_all])
        X_extractInline_and_random = df_extractInline_and_random[['PAR', 'VG', 'NBD', 'MLOC', 'WMC', 'DIT', 'LCOM', 'NSC']]
        y_extractInline_and_random = df_extractInline_and_random['category']
        clf_extractInline_and_random = LogisticRegression()
        clf_extractInline_and_random.fit(X_extractInline_and_random, y_extractInline_and_random)
        df_inline_reverse['category'] = 0

        df = pd.concat([df_refactored_method_all.take(np.random.permutation(len(df_refactored_method_all))[:len(df_non_refactored_method_all)]), df_non_refactored_method_all])
        X = df[['PAR', 'VG', 'NBD', 'MLOC', 'WMC', 'DIT', 'LCOM', 'NSC']]
        y = df['category']
        clf_random = LogisticRegression()
        clf_random.fit(X, y)

        print("---model info---")
        print "[model]: constracted extract and random \t [extract method]: " + str(len(df.ix[df['category'] == 1, :])) + "\t [random method]: " + str(len(df.ix[df['category'] == 0, :]))
        print "[model]: constracted extract and random equal \t [extract method]: " + str(len(df_equal.ix[df_equal['category'] == 1, :])) + "\t [random method]: " + str(len(df_equal.ix[df_equal['category'] == 0, :]))
        print "[model]: constructed extract and inline \t [extract method]: " + str(len(df_refactored_method_and_inline.ix[df_refactored_method_and_inline['category'] == 1, :])) + "\t [inline method]: " + str(len(df_refactored_method_and_inline.ix[df_refactored_method_and_inline['category'] == 0, :]))
        print "[model]: constructed extract and (inline and random) \t [extract method]: " + str(len(df_refactored_method_and_non_and_inline.ix[df_refactored_method_and_non_and_inline['category'] == 1, :])) + "\t [inline and random method]: " + str(len(df_refactored_method_and_non_and_inline.ix[df_refactored_method_and_non_and_inline['category'] == 0, :]))
        print "[model]: constructed inline and random \t [inline method]: " + str(len(df_inline_reverse_random.ix[df_inline_reverse_random['category'] == 1, :])) + "\t [random method]: " + str(len(df_inline_reverse_random.ix[df_inline_reverse_random['category'] == 0, :]))
        print "[model]: constructed (extract and inline) and random \t [extract and inline method]: " + str(len(df_extractInline_and_random.ix[df_extractInline_and_random['category'] == 1, :])) + "\t [random method]: " + str(len(df_extractInline_and_random.ix[df_extractInline_and_random['category'] == 0, :]))

        print ("---validation---")
        y_inline_pred = clf_random.predict(X_inline)
        print "[model]: constructed extract and random \t [test data]: only inline \t [accuracy score]:", accuracy_score(y_inline, y_inline_pred)

        #y_refactored_method_and_inline_train_pred = clf_inline.predict(X_refactored_method_and_inline_train)
        #print "[model]: constructed extract and inline \t [test data]: train include extract and inline \t [accuracy_score]:", accuracy_score(y_refactored_method_and_inline_train, y_refactored_method_and_inline_train_pred)

        #y_refactored_method_and_inline_val_pred = clf_inline.predict(X_refactored_method_and_inline_val)
        #print "[model]: constructed extract and inline \t [test data]: val include extract and inline \t [accuracy_score]:", accuracy_score(y_refactored_method_and_inline_val, y_refactored_method_and_inline_val_pred)

        y_inline_pred = clf_equal.predict(X_inline)
        print "[model]: constructed extract and random equal \t [test data]: only inline \t [accuracy score]:", accuracy_score(y_inline, y_inline_pred)

        y_inline_pred = clf_inline.predict(X_inline)
        print "[model]: constructed extract and inline \t [test data]: only inline \t [accuracy score]:", accuracy_score(y_inline, y_inline_pred)

        y_inline_pred = clf_random_and_inline.predict(X_inline)
        print "[model]: constructed extract and (inline and random) \t [test data]: only inline \t [accuracy score]:", accuracy_score(y_inline, y_inline_pred)

        y_inline_reverse_random_pred = clf_inline_reverse_random.predict(X_inline_reverse_random)
        print "[model]: constructed inline and random \t [test data]: only inline \t [accuracy score]:", accuracy_score(y_inline_reverse_random, y_inline_reverse_random_pred)

        y_inline_reverse_random_pred = clf_extractInline_and_random.predict(X_inline_reverse_random)
        print "[model]: constructed (extract and inline) and random \t [test data]: only inline \t [accuracy score]:", accuracy_score(y_inline_reverse_random, y_inline_reverse_random_pred)

        print ("---10 fold cross validation---")
        print "[model]: constructed extract and random \t [mean accuracy score]:", cross_val(clf_random, X, y, 10).mean()
        print "[model]: constructed extract and random equal \t [mean accuracy score]:", cross_val(clf_equal, X_equal, y_equal, 10).mean()
        print "[model]: constructed extract and inline \t [mean accuracy score]:", cross_val(clf_inline, X_refactored_method_and_inline, y_refactored_method_and_inline, 10).mean()
        print "[model]: constructed extract and (inline and random) \t [mean accuracy score]:", cross_val(clf_random_and_inline, X_refactored_method_and_non_and_inline, y_refactored_method_and_non_and_inline, 10).mean()
        print "[model]: constructed inline and random \t [mean accuracy score]:", cross_val(clf_inline_reverse_random, X_inline_reverse_random, y_inline_reverse_random, 10).mean()
        print "[model]: constructed (extract and inline) and random \t [mean accuracy score]:", cross_val(clf_extractInline_and_random, X_extractInline_and_random, y_extractInline_and_random, 10).mean()

    #predict_refactoring_with_own_for_train_and_test(X, y)

    #X_train, X_val, y_train, y_val = train_test_split(X, y, train_size=0.8, random_state=1)

    #clf.fit(X_train, y_train)
    #y_train_pred = clf.predict(X_train)
    #y_val_pred = clf.predict(X_val)

    #print accuracy_score(y_train, y_train_pred), accuracy_score(y_val, y_val_pred)
