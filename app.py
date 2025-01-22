import math
import itertools


from flask import Flask, render_template, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField

def load_vocab():
    vocab = {}
    with open('tf-idf/vocab.txt', 'r') as f:
        vocab_terms = f.readlines()
    with open('tf-idf/idf-values.txt', 'r') as f:
        idf_values = f.readlines()
    
    for (term,idf_value) in zip(vocab_terms, idf_values):
        vocab[term.strip()] = int(idf_value.strip())
    
    return vocab

def load_documents():
    documents = []
    with open('tf-idf/documents.txt', 'r') as f:
        documents = f.readlines()
    documents = [document.strip().split() for document in documents]

    print('Number of documents: ', len(documents))
    return documents

def load_inverted_index():
    inverted_index = {}
    with open('tf-idf/inverted-index.txt', 'r') as f:
        inverted_index_terms = f.readlines()

    for row_num in range(0,len(inverted_index_terms),2):
        term = inverted_index_terms[row_num].strip()
        documents = inverted_index_terms[row_num+1].strip().split()
        inverted_index[term] = documents
    
    print('Size of inverted index: ', len(inverted_index))
    return inverted_index


def load_links():
    with open("questions/qindex.txt", "r") as f:
        links = f.readlines()

    return links


vocab_idf_values = load_vocab()
documents = load_documents()
inverted_index = load_inverted_index()
qlink = load_links()



def get_tf_dictionary(term):
    tf_values = {}
    if term in inverted_index:
        for document in inverted_index[term]:
            if document not in tf_values:
                tf_values[document] = 1
            else:
                tf_values[document] += 1
                
    for document in tf_values:
        tf_values[document] /= len(documents[int(document)])
    
    return tf_values





def get_idf_value(term):
    return math.log((1+len(documents))/(1+vocab_idf_values[term]))




def order_of_documents(query_terms):
    potential_docs = {}
    ans = []
    for term in query_terms:
        if (term not in vocab_idf_values):
            continue

        tf_vals_by_docs = get_tf_dictionary(term)
        idf_value = get_idf_value(term)

        for doc in tf_vals_by_docs:
            if doc not in potential_docs:
                potential_docs[doc] = tf_vals_by_docs[doc]*idf_value
            else:
                potential_docs[doc] += tf_vals_by_docs[doc]*idf_value

        # divide the scores of each doc with no of query terms
        for doc in potential_docs:
            potential_docs[doc] /= len(query_terms)

        # sort in dec order acc to values calculated
        potential_docs = dict(sorted(potential_docs.items(), key=lambda item: item[1], reverse=True))

        # if no doc found
        if (len(potential_docs) == 0):
            print("No matching question found. Please search with more relevant terms.")

        for doc_index in potential_docs:
            ans.append({"Question Link": qlink[int(doc_index) - 1][:-2], "Score": potential_docs[doc_index]})
    return ans








#query_string = input('Enter your query: ')
#query_terms = [term.lower() for term in query_string.strip().split()]


#print(order_of_documents(query_terms)[0])


app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'your-secret-key'
app.static_folder = 'static'

class SearchForm(FlaskForm):
    search = StringField('Enter your search term')
    submit = SubmitField('Search')


@app.route("/<query>")
def return_links(query):
    q_terms = [term.lower() for term in query.strip().split()]
    return jsonify(order_of_documents(q_terms)[:10:])


@app.route("/", methods=['GET', 'POST'])
def home() :
    form = SearchForm()
    results = []
    if form.validate_on_submit():
        query = form.search.data
        q_terms = [term.lower() for term in query.strip().split()]
        results = order_of_documents(q_terms)[:20:]
    return render_template('index.html', form=form, results=results)

if __name__ == '__main__':
    app.run(debug=True)