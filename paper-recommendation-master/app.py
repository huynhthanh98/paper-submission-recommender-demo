# -*- coding: utf-8 -*-
"""
Created on Sat Jul 11 17:35:56 2020

@author: huynh
"""

from flask import Flask, render_template, request
import os

template_dir = os.path.abspath("./templates")


app = Flask(__name__, template_folder=template_dir, static_url_path="", static_folder="static")
#app = Flask(__name__)
@app.route('/')
def hello_world():
    return render_template('home.html', title=" AISIA paper submission")

@app.route("/Predict",methods=["POST"])
def Predictt():
    #content = request.form.get('title')
    #return render_template('home.html',content = content)
    title=request.form.get('title')
    keyword=request.form.get('keyword')
    abstract=request.form.get('abstract')
    lists=['IEEE Transactions on Computers',
       'IEEE Trans on Pattern Analysis and Machine Intelligence',
       'International Conference on Software Engineering',
       'ACM International Conference on Multimedia',
       'IEEE Transactions on Image Processing',
       'International Conference on Computer Vision',
       'ACM Symposium on Theory of Computing',
       'ACM Conference on Human Factors in Computing Systems',
       'ACM International Conference on the applications, technologies, architectures, and protocols for computer communication',
       'High-Performance Computer Architecture',
       'Proceedings of the IEEE',
       'International Conference on Research on Development in Information Retrieval',
       'International Joint Conference on Artificial Intelligence',
       'ACM Transactions on Information Systems',
       'IEEE Transactions on Dependable and Secure Computing',
       'International Conference on Machine Learning',
       'IEEE International Conference on Data Engineering',
       'IEEE Transactions on Parallel and Distributed Systems',
       'IEEE Transactions on Information Forensics and Security',
       'Conference on Object-Oriented Programming Systems, Languages, and Applications',
       'AAAI Conference on Artificial Intelligence',
       'IEEE Transactions on Visualization and Computer Graphics',
       'European Cryptology Conference', 'Real-Time Systems Symposium',
       'IEEE Journal of Selected Areas in Communications',
       'IEEE Transactions on Mobile Computing',
       'IEEE International Conference on Computer Communications',
       'IEEE Transactions on Knowledge and Data Engineering',
       'ACM SIGPLAN-SIGACT Symposium on Principles of Programming Languages',
       'Journal of Cryptology',
       'IEEE Transactions on Software Engineering',
       'SIAM Journal on Computing',
       'ACM Transactions on Programming Languages & Systems',
       'ACM SIGGRAPH Annual Conference',
       'ACM Knowledge Discovery and Data Mining',
       'IEEE Symposium on Logic in Computer Science',
       'ACM Transactions on Graphics',
       'IEEE Symposium on Foundations of Computer Science',
       'ACM International Conference on Mobile Computing and Networking',
       'ACM International Conference on Ubiquitous Computing',
       'Journal of Machine Learning Research',
       'IEEE Conference on Computer Vision and Pattern Recognition',
       'ACM Conference on Management of Data',
       'International Cryptology Conference',
       'Security  Usenix Security Symposium', 'Journal of the ACM',
       'Conference on File and Storage Technologies',
       'ACM Transactions on Computer-Human Interaction',
       'ACM Transactions on Computer Systems',
       'ACM SIGPLAN Symposium on Programming Language Design & Implementation',
       'International Conference on Very Large Data Bases',
       'Information and Computation', 'VLDB Journal',
       'International Symposium on Computer Architecture',
       'International Journal of Human Computer Studies',
       'International Journal of Computer Vision',
       'IEEE/ACM Transactions on Networking', 'MICRO',
       'Architectural Support for Programming Languages and Operating Systems',
       'USENIX Symposium on Operating Systems Design and Implementations',
       'ACM Transactions on Database Systems',
       'IEEE Symposium on Security and Privacy',
       'ACM Conference on Computer and Communications Security',
       'Artificial Intelligence',
       'ACM SIGSOFT Symposium on the Foundation of Software Engineering/ European Software Engineering Conference',
       'ACM Symposium on Operating Systems Principles']
    import numpy as np
    import re
    import pickle
    from tensorflow.keras.preprocessing.sequence import pad_sequences
    stop = ["a", "about", "above", "above", "across", "after", "afterwards", "again", "against", "all", "almost", "alone", "along", "already", "also","although","always","am","among", "amongst", "amoungst", "amount",  "an", "and", "another", "any","anyhow","anyone","anything","anyway", "anywhere", "are", "around", "as",  "at", "back","be","became", "because","become","becomes", "becoming", "been", "before", "beforehand", "behind", "being", "below", "beside", "besides", "between", "beyond", "bill", "both", "bottom","but", "by", "call", "can", "cannot", "cant", "co", "con", "could", "couldnt", "cry", "de", "describe", "detail", "do", "done", "down", "due", "during", "each", "eg", "eight", "either", "eleven","else", "elsewhere", "empty", "enough", "etc", "even", "ever", "every", "everyone", "everything", "everywhere", "except", "few", "fifteen", "fify", "fill", "find", "fire", "first", "five", "for", "former", "formerly", "forty", "found", "four", "from", "front", "full", "further", "get", "give", "go", "had", "has", "hasnt", "have", "he", "hence", "her", "here", "hereafter", "hereby", "herein", "hereupon", "hers", "herself", "him", "himself", "his", "how", "however", "hundred", "ie", "if", "in", "inc", "indeed", "interest", "into", "is", "isnt", "it", "its", "itself", "keep", "keeps", "kept", "last", "latter", "latterly", "least", "less", "ltd", "made", "many", "may", "me", "meanwhile", "might", "mill", "mine", "more", "moreover", "most", "mostly", "move", "much", "must", "my", "myself", "name", "names", "named", "namely", "neither", "never", "nevertheless", "next", "nine", "no", "nobody", "none", "noone", "nor", "not", "nothing", "now", "nowhere", "of", "off", "often", "ok", "on", "once", "one", "only", "onto", "or", "other", "others", "otherwise", "our", "ours", "ourselves", "out", "over", "own","part", "per", "perhaps", "please", "put", "puts", "rather", "re", "same", "see", "seem", "seemed", "seeming", "seems", "sees", "serious", "several", "she", "should", "show", "shows", "showed", "side", "since", "sincere", "six", "sixty", "so", "some", "somehow", "someone", "something", "sometime", "sometimes", "somewhere", "still", "such", "system", "take", "ten", "than", "that", "the", "their", "them", "themselves", "then", "thence", "there", "thereafter", "thereby", "therefore", "therein", "thereupon", "these", "they", "thickv", "thin", "third", "this", "those", "though", "three", "through", "throughout", "thru", "thus", "to", "together", "too", "top", "toward", "towards", "twelve", "twenty", "two", "un", "under", "until", "up", "upon", "us", "very", "via", "was", "we", "well", "were", "what", "whatever", "when", "whence", "whenever", "where", "whereafter", "whereas", "whereby", "wherein", "whereupon", "wherever", "whether", "which", "while", "whither", "who", "whoever", "whole", "whom", "whose", "why", "will", "with", "within", "without", "would", "yet", "you", "your", "yours", "yourself", "yourselves", "the", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"]
    #A="rate adaptation   multiuser mimo networks "
    
    #title
    title=title.lower()
    title = re.sub("\d+", "", title)
    title = re.sub("[^\w]", " ", title)
    
    filtered_sentence = [] 
    for w in title.split(" "): 
        if w not in stop: 
            filtered_sentence.append(w)
    Title=" ".join(filtered_sentence)
     
    #keyword
    keyword=keyword.lower()
    keyword = re.sub("\d+", "", keyword)
    # text = re.sub("[-]+", " ", text)
    Keyword = re.sub("[^\w]", " ", keyword)
    
    #abstract
    abstract=abstract.lower()
    abstract = re.sub("\d+", "", abstract)
    abstract = re.sub("[^\w]", " ", abstract)
    
    filtered_sentence = [] 
    for w in abstract.split(" "): 
        if w not in stop: 
            filtered_sentence.append(w)
    Abstract=" ".join(filtered_sentence)

    
    Feature=Title + " " + " " + Keyword + " " +Abstract
    
    with open('tokenizer_Feature.pickle', 'rb') as f:
        token = pickle.load(f)
    X=token.texts_to_sequences([Feature])
    X=pad_sequences(X, maxlen=343)
    import tensorflow as tf 
    new_model = tf.keras.models.load_model('my_model_Feature.h5')
    C=new_model.predict(np.array(np.array([X[0]])))
    predict=np.sort(C, axis=1)[:,::-1]
    y_pred = np.argsort(C, axis=1)[:,::-1]
    #return render_template('home.html',content=Feature)
    return render_template('home.html',content0 = lists[y_pred[0,0]],content1 = lists[y_pred[0,1]],
                           content2 = lists[y_pred[0,2]],content3 = lists[y_pred[0,3]],
                           content4 = lists[y_pred[0,4]],score0=predict[0,0],
                           score1=predict[0,1],score2=predict[0,2],
                           score3=predict[0,3],score4=predict[0,4])



if __name__ == '__main__':
    app.run()
    #app.debug(True)
