def readfiles(paths,tags):
    #paths is a list of path saving different tags
    import random, os
    article_tag=[]
    for i, path in enumerate(paths):
        for txtfile in os.listdir(path):
            if txtfile.endswith(".txt"):
            #artcile is a list of words in article after preprocessing
                article=preprocess(txtfile)
                article_tag.append((article,tags[i]))
    random.shuffle(article_tag)
    #article_tag is a list of (article, tag)
    return article_tag

#preprocessing txtfile to return a list of strings
def preprocess(article):
    article=article.strip().lower()
    return article.split()

def generate_word_features_set(word_features_file):
    with open(word_features_file, 'r') as d:
        word_features_list=[word.strip().lower() for word in d]
    d.close()
    word_features_set=set(word_features_list)
    single_word_features_set=[]
    for i in word_features_set:
        single_word_features_set+=i.split()
    print "length of word feature=",len(set(single_word_features_set))
    return set(single_word_features_set)

#for each article_tag, record feature existence booleans, return dictionay{word:occur or not}
def find_features_in_article(article,word_features_set):
    words_in_article = set(article)
    features_in_article = {}
    for w in word_features_set:
        features_in_article[w] = (w in words_in_article)
    return features_in_article

def generate_features_occurence_inarticle_tag(article_tag,word_features_file):
    features_occurence_inarticle_tag=[]
    word_features_set=generate_word_features_set(word_features_file)
    for (article,tag) in article_tag:
        features_occurence_inarticle_tag.append((find_features_in_article(article,word_features_set),tag))
    return features_occurence_inarticle_tag


def tag(training_set,testing_set):
    import nltk
    from nltk.classify.scikitlearn import SklearnClassifier

    classifier = nltk.NaiveBayesClassifier.train(training_set)
    print("Classifier accuracy percent:",(nltk.classify.accuracy(classifier, testing_set))*100)
    classifier.show_most_informative_features(50)
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
    '''
    NuSVC_classifier = SklearnClassifier(NuSVC())
    NuSVC_classifier.train(training_set)
    print("NuSVC_classifier accuracy percent:", (nltk.classify.accuracy(NuSVC_classifier, testing_set))*100)
    '''
################################################################################
def show_most_informative_features(vectorizer, clf, n=20):
    feature_names = vectorizer.get_feature_names()
    coefs_with_fns = sorted(zip(clf.coef_[0], feature_names))
    top = zip(coefs_with_fns[:n], coefs_with_fns[:-(n + 1):-1])
    for (coef_1, fn_1), (coef_2, fn_2) in top:
        print "\t%.4f\t%-15s\t\t%.4f\t%-15s" % (coef_1, fn_1, coef_2, fn_2)

def article_classifier(paths,tags,word_features_file ):
    from sklearn.cross_validation import train_test_split
    article_tag=readfiles(paths,tags)
    #assign word_features_file
    #word_features_file=
    dataset=generate_features_occurence_inarticle_tag(article_tag,word_features_file)
    training_set,testing_set = train_test_split(dataset, random_state=4)
    tag(training_set,testing_set)

paths=["/Users/macbook/Documents/RA/case_study_txt","/Users/macbook/Documents/RA/training_set_false_txt123"]
tags=["pos","neg"]
word_features_file="/Users/macbook/Documents/RA/variation_all.txt"
article_classifier(paths, tags,word_features_file )
