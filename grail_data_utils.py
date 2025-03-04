import matplotlib.pyplot as plt
import numpy as npy
import re


# normalizes word according to the conventions of fastText; only transforms the word to lower case

def normalize_word(orig_word):
    word = orig_word.lower()
    if (word == "["):
        word = "("
    if (word == "]"):
        word = ")"
    
    return word


def read_maxentdata(file):
    with open(file, 'r') as f:
        vocabulary = set()
        vnorm = set()
        partsofspeech1 = set()
        partsofspeech2 = set()
        superset = set()
        sentno = 0
        maxlen = 0
        words = []
        postags1 = []
        postags2 = []
        supertags = []
        allwords = []
        allpos1 = []
        allpos2 = []
        allsuper = []
        for line in f:
            line = line.strip().split()
            length = len(line)
            if (length > maxlen):
                maxlen = length
            for l in range(length):
                item = line[l].split('|')
                orig_word = item[0]
                word = normalize_word(orig_word)
                postag = item[1]
                supertag = item[2]
                poslist = postag.split('-')
                pos1 = poslist[0]
                pos2 = poslist[1]
                vocabulary.add(orig_word)
                vnorm.add(word)
                partsofspeech1.add(pos1)
                partsofspeech2.add(pos2)
                superset.add(supertag)
                words.append(orig_word)
                postags1.append(pos1)
                postags2.append(pos2)
                supertags.append(supertag)
            allwords.append(words)
            allpos1.append(postags1)
            allpos2.append(postags2)
            allsuper.append(supertags)
            words = []
            postags1 = []
            postags2 = []
            supertags = []
            
        X = npy.asarray(allwords)
        Y1 = npy.asarray(allpos1)
        Y2 = npy.asarray(allpos2)
        Z = npy.asarray(allsuper)
        return X, Y1, Y2, Z, vocabulary, vnorm, partsofspeech1, partsofspeech2, superset, maxlen


# create a bi-directional mapping (using two dictionaries) translating elements of a set to and from integers

def indexify (set):
    i = 1
    item_to_index = {}
    index_to_item = {}

    for item in set:
        item_to_index[item] = i
        index_to_item[i] = item
        i = i + 1

    return item_to_index, index_to_item



# convert array of lists X into an (m,max_len) array

def lists_to_indices(X, item_to_index, max_len, normalize=False):

    m = X.shape[0]                                   # number of training examples
    
    # Initialize X_indices as a numpy matrix of zeros and the correct shape (≈ 1 line)
    X_indices = npy.zeros((m,max_len))

    for i in range(m):                               # loop over training examples
        
        # Convert the ith training sentence in lower case and split it into words. You should get a list of words.
        list = X[i]

        j = 0
        
        # Loop over the words of sentence_words
        for w in list:
            if normalize == True:
                w = normalize_word(w)
            # Set the (i,j)th entry of X_indices to the index of the correct word.
            try:
                X_indices[i, j] = item_to_index[w]
            except:
                print("Unknown: ", w)
                X_indices[i, j] = 1  # unknown
            # Increment j to j + 1
            j = j + 1
            
    return X_indices


def sentences_to_indices(X, word_to_index, max_len):
    """
    Converts an array of sentences (strings) into an array of indices corresponding to words in the sentences.
    The output shape should be such that it can be given to `Embedding()` (described in Figure 4). 
    
    Arguments:
    X -- array of sentences (strings), of shape (m, 1)
    word_to_index -- a dictionary containing the each word mapped to its index
    max_len -- maximum number of words in a sentence. You can assume every sentence in X is no longer than this. 
    
    Returns:
    X_indices -- array of indices corresponding to words in the sentences from X, of shape (m, max_len)
    """
    
    m = X.shape[0]                                   # number of training examples
    
    ### START CODE HERE ###
    # Initialize X_indices as a numpy matrix of zeros and the correct shape (≈ 1 line)
    X_indices = npy.zeros((m,max_len))
    
    for i in range(m):                               # loop over training examples
        
        # Convert the ith training sentence in lower case and split it into words. You should get a list of words.
        sentence_words = X[i]
        
        # Initialize j to 0
        j = 0
        
        # Loop over the words of sentence_words
        for w in sentence_words:
            # w = normalize_word(w)
            # Set the (i,j)th entry of X_indices to the index of the correct word.
            try:
                X_indices[i, j] = word_to_index[w]
            except:
                print("Unknown: ", w)
                X_indices[i, j] = 1   # index for unknown words
            # Increment j to j + 1
            j = j + 1
            
    ### END CODE HERE ###
    
    return X_indices


def plot_confusion_matrix(y_actu, y_pred, title='Confusion matrix', cmap=plt.cm.gray_r):
    
    df_confusion = pd.crosstab(y_actu, y_pred.reshape(y_pred.shape[0],), rownames=['Actual'], colnames=['Predicted'], margins=True)
    
    df_conf_norm = df_confusion / df_confusion.sum(axis=1)
    
    plt.matshow(df_confusion, cmap=cmap) # imshow
    #plt.title(title)
    plt.colorbar()
    tick_marks = npy.arange(len(df_confusion.columns))
    plt.xticks(tick_marks, df_confusion.columns, rotation=45)
    plt.yticks(tick_marks, df_confusion.index)
    #plt.tight_layout()
    plt.ylabel(df_confusion.index.name)
    plt.xlabel(df_confusion.columns.name)

def tag_sequence(sentence, model, wmap, imap, maxLen):
    list = sentence.strip().split()
    arr = npy.array([list])
    indices = lists_to_indices(arr, wmap, max_len = maxLen, normalize=True)
    pred = model.predict(indices)
    for j in range(len(list)):
        num = npy.argmax(pred[0][j])        
        print(list[j] + '|' + imap[num], end=' ')


def print_tagged(X, model, wmap, imap, maxLen):

    Xi = lists_to_indices(X, wmap, maxLen)
    pred = model.predict(Xi) 
    
    for i in range(len(X)-1):
        for j in range(len(X[i])):
            num = npy.argmax(pred[i][j])
            print(X[i][j] + '|' + imap[num], end = ' ')
        print()

def print_tagged_beta(X, model, beta, wmap, imap, maxLen):

    Xi = lists_to_indices(X, wmap, maxLen)
    pred = model.predict(Xi) 
    
    for i in range(len(X)-1):
        for j in range(len(X[i])):
            tags = predict_beta(pred[i][j],beta)
            print(X[i][j], end = '')
            print('|', end='')
            print(len(tags), end='')
            for key,value in tags.items():
                print('|', end='')
                print(imap[key], end='')
                print('|', end='')
                print(value, end='')
            print(' ', end='')    
        print()

# returns set with integer indices of all solutions with probability
# greater than or equal to beta time the probability assigned to the
# best solution
        
def predict_beta_set(vec,beta):
    tags = set()
    maxp = npy.max(vec)
    bm = maxp * beta
    for k in range(len(vec)):
        kprob = vec[k]
        if (kprob >= bm):
            tags.add(k)
    return tags

def predict_beta(vec,beta):
    tags = {}
    maxp = npy.max(vec)
    bm = maxp * beta
    for k in range(len(vec)):
        kprob = vec[k]
        if (kprob >= bm):
            tags[k] = kprob
    return tags

# This code allows you to see the mislabelled examples

def eval_beta(X_dev, Y_dev, model, wmap, imap, iimap, beta, maxLen):
    correct = 0
    wrong = 0
    totalpreds = 0

    Xi = lists_to_indices(X_dev, wmap, maxLen)
    Y_dev_indices = lists_to_indices(Y_dev, imap, max_len = maxLen)
    pred = model.predict(Xi)
    
    for i in range(len(X_dev)-1):
        for j in range(len(X_dev[i])):
            numset = predict_beta_set(pred[i][j], beta)
            totalpreds = totalpreds + len(numset)
            if not (Y_dev_indices[i][j] in numset):
                wrong = wrong + 1
                print('Expected tag: '+ X_dev[i][j] + '|' + Y_dev[i][j] + ' prediction: '+ X_dev[i][j],end='')
#                print(numset)
                for pi in numset:
                    print('|' + iimap[pi], end='')
                print()
            else:
                correct = correct + 1
    total = wrong + correct
    print("Total  : ", total)
    print("Correct: ", correct)
    print("Wrong  : ", wrong)

    cpct = (100*correct)/total
    wpct = (100*wrong)/total
    print("Correct %: ", cpct)
    print("Wrong   %: ", wpct)
    
    avpreds = totalpreds/total
    print("Average predictions : ", avpreds)

