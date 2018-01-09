
#
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.metrics import classification_report
from sklearn.metrics import accuracy_score
import numpy as np


#prepare corpus and divide into train set and test set
def load_corpus(corpus_paths,tags):
    #paths is a list of path saving different tags
    import os
    articles,targets=[],[]
    for i, path in enumerate(corpus_paths):
        for txtfile in os.listdir(path):
            if txtfile.endswith(".txt"):
            #artciles is a list of article string
            #tags is a list of targets
                with open(path+'/'+txtfile, 'r') as article_file:
                    temp_read = article_file.read()
                    temp_read = unicode(temp_read, errors='replace')
                    try:
                        articles.append(temp_read)
                        targets.append(tags[i])
                    except:
                        print(temp_read)
    #return a list of article string, and a list of tags
    return articles, targets

#prepare the vocabulary
def generate_vocabulary_vectorizer(vocabulary_file):
    with open(vocabulary_file, 'r') as d:
        vocabulary=[phrase for phrase in d]
    #print vocabulary[:100]
    vocabulary_vectorizer = CountVectorizer(analyzer ='word',ngram_range=(1, 3),token_pattern=r'(?!\b\d+\b)\b\w{2,}\b', min_df=1, stop_words='english')
    _ =vocabulary_vectorizer.fit_transform(vocabulary)
    '''
    voc = vocabulary_vectorizer.get_feature_names()
    print voc[:500]
    print voc[-500:]
    print 's in voc: ',('s' in voc)
    print 'bacterium in voc: ',('bacterium' in voc)
    '''
    voc = vocabulary_vectorizer.get_feature_names()
    print 'bacterium in voc: ',('bacterium' in voc)
    return vocabulary_vectorizer

def generate_corpus_vector(vocabulary_vectorizer,X):
    #initilize a tf-id vectorizer to the corpus
    corpus_vectorizer = CountVectorizer(analyzer ='word', ngram_range=(1, 3),token_pattern=r'(?!\b\d+\b)\b\w{2,}\b', min_df=1,stop_words='english',vocabulary=vocabulary_vectorizer.vocabulary_)
    X_counts = corpus_vectorizer.fit_transform(X)
    X_tf_transformer = TfidfTransformer(use_idf=False).fit(X_counts)
    X_tf = X_tf_transformer.transform(X_counts)
    return X_tf


def article_classifier(corpus_paths,tags,vocabulary_file):
    from sklearn.model_selection import train_test_split
    articles, targets=load_corpus(corpus_paths,tags)
    X_train, X_test, y_train, y_test = train_test_split(articles, targets, test_size=0.33, random_state=42)
    vocabulary_vectorizer = generate_vocabulary_vectorizer(vocabulary_file)
    #print X_train[:2], y_train[:2]
    X_train_tf = generate_corpus_vector(vocabulary_vectorizer, X_train)
    X_test_tf = generate_corpus_vector(vocabulary_vectorizer,X_test)
    tag(X_train_tf,X_test_tf,y_train,y_test,vocabulary_vectorizer)


def tag(X_train_tf,X_test_tf,y_train,y_test,vocabulary_vectorizer):
    #############################################
    from sklearn.naive_bayes import MultinomialNB
    clf = MultinomialNB().fit(X_train_tf, y_train)
    predicted = clf.predict(X_test_tf)
    #classification_report(y_test, predicted)
    print("MultinomialNB \n", accuracy_score(y_test, predicted))
    print("MultinomialNB \n", classification_report(y_test, predicted))

    #print "MultinomialNB", clf.coef_[0]
    #print clf.coef_
    #np.mean(predicted == y_test)
    #print("MultinomialNB accuracy percent:", np.mean(predicted == y_test) )
    #############################################
    from sklearn.naive_bayes import BernoulliNB
    clf = BernoulliNB().fit(X_train_tf, y_train)
    predicted = clf.predict(X_test_tf)
    #classification_report(y_test, predicted)
    print("BernoulliNB \n", accuracy_score(y_test, predicted))
    print("BernoulliNB \n", classification_report(y_test, predicted))
    #show_most_informative_features(vocabulary_vectorizer, clf, 1000)

    #show_top20(clf, vocabulary_vectorizer, [True,False])
    #############################################
    from sklearn.linear_model import SGDClassifier
    clf = SGDClassifier().fit(X_train_tf, y_train)
    predicted = clf.predict(X_test_tf)
    print("SGDClassifier \n", accuracy_score(y_test, predicted))
    print("SGDClassifier\n", classification_report(y_test, predicted))

    #print "SGDClassifier", clf.coef_[0]
    #print clf.coef_
    ###############################################
    from sklearn.linear_model import LogisticRegression
    clf = LogisticRegression().fit(X_train_tf, y_train)
    predicted = clf.predict(X_test_tf)
    print("LogisticRegression \n", accuracy_score(y_test, predicted))
    print("LogisticRegression", classification_report(y_test, predicted))
    ###############################################
    from sklearn.svm import LinearSVC
    clf = LinearSVC().fit(X_train_tf, y_train)
    predicted = clf.predict(X_test_tf)
    print("LinearSVC \n", accuracy_score(y_test, predicted))
    print("LinearSVC", classification_report(y_test, predicted))
    ###############################################
    from sklearn.svm import SVC
    clf = SVC().fit(X_train_tf, y_train)
    predicted = clf.predict(X_test_tf)
    print("SVC \n", accuracy_score(y_test, predicted))
    print("SVC", classification_report(y_test, predicted))









'''

def tag(training_set,testing_set):
    import nltk
    from nltk.classify.scikitlearn import SklearnClassifier

    classifier = nltk.NaiveBayesClassifier.train(training_set)
    print("Classifier accuracy percent:",(nltk.classify.accuracy(classifier, testing_set))*100)
    classifier.show_most_informative_features(500)
    #############################################
    from sklearn.naive_bayes import MultinomialNB,BernoulliNB

    MNB_classifier = SklearnClassifier(MultinomialNB())
    MNB_classifier.train(training_set)
    #MNB_classifier.show_most_informative_features(15)
    print("MultinomialNB accuracy percent:",nltk.classify.accuracy(MNB_classifier, testing_set))

    BNB_classifier = SklearnClassifier(BernoulliNB())
    BNB_classifier.train(training_set)
    print("BernoulliNB accuracy percent:",nltk.classify.accuracy(BNB_classifier, testing_set))

    ###############################################
    from sklearn.linear_model import LogisticRegression,SGDClassifier

    LogisticRegression_classifier = SklearnClassifier(LogisticRegression())
    LogisticRegression_classifier.train(training_set)
    print("LogisticRegression_classifier accuracy percent:", (nltk.classify.accuracy(LogisticRegression_classifier, testing_set))*100)

    SGDClassifier_classifier = SklearnClassifier(SGDClassifier())
    SGDClassifier_classifier.train(training_set)
    print("SGDClassifier_classifier accuracy percent:", (nltk.classify.accuracy(SGDClassifier_classifier, testing_set))*100)

    ##################################################
    from sklearn.svm import SVC, LinearSVC, NuSVC

    SVC_classifier = SklearnClassifier(SVC())
    SVC_classifier.train(training_set)
    print("SVC_classifier accuracy percent:", (nltk.classify.accuracy(SVC_classifier, testing_set))*100)

    LinearSVC_classifier = SklearnClassifier(LinearSVC())
    LinearSVC_classifier.train(training_set)
    print("LinearSVC_classifier accuracy percent:", (nltk.classify.accuracy(LinearSVC_classifier, testing_set))*100)

################################################################################

def show_most_informative_features(vectorizer, clf, n=20):
    feature_names = vectorizer.get_feature_names()
    coefs_with_fns = sorted(zip(clf.coef_[0], feature_names))
    top = zip(coefs_with_fns[:n], coefs_with_fns[:-(n + 1):-1])
    for (coef_1, fn_1), (coef_2, fn_2) in top:
        print "\t%.4f\t%s\t\t%.4f\t%s" % (coef_1, fn_1, coef_2, fn_2)

def show_top20(classifier, vectorizer, categories):
    feature_names = np.asarray(vectorizer.get_feature_names())
    for i, category in enumerate(categories):
        top20 = np.argsort(classifier.coef_[i])[-20:]
        print("%s: %s" % (category, " ".join(feature_names[top20])))


def show_most_informative_features(vectorizer, clf, n=20):
    feature_names = vectorizer.get_feature_names()
    coefs_with_fns = sorted(zip(clf.coef_[0], feature_names))
    top =  coefs_with_fns[:-(n + 1):-1]
    for (coef, fn) in top:
        print "%s\t:\t%.4f" % (fn, coef)
'''
true_path='/Users/macbook/Documents/RA/classicifation/Syndrom_Prescursor_Control_Agent_01:10:2017/Combined Training set 01:10:2017/True'
false_path='/Users/macbook/Documents/RA/classicifation/Syndrom_Prescursor_Control_Agent_01:10:2017/Combined Training set 01:10:2017/False'
corpus_paths=[true_path,false_path]
tags=["pos","neg"]
vocabulary_file="/Users/macbook/Documents/RA/classicifation/Syndrom_Prescursor_Control_Agent_01:10:2017/variation_Syndrom_Prescursor_Control_Agent.txt"
article_classifier(corpus_paths,tags,vocabulary_file)
