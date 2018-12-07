import _pickle as pickle


wrangled_data = r'C:\Users\mches\Dropbox\Georgetown Data Science -- Team Amazon\wrangled_knn_data.db'

def unpickle():
    file = "finalized_model.sav"
    clf = pickle.load(open(file, "rb"))
    return clf

def get_index_from_name(name, review_data):
    return review_data[review_data["product_title"]==name].index.tolist()[0]

def print_similar_books(review_data, query=None,id=None, model=None):
    distances2, indices2 = model.kneighbors()
    if id:
        for id in indices2[id][1:]:
            print(review_data.iloc[id]["product_title"])
    if query:
        found_id = get_index_from_name(query, review_data)
        for id in indices2[found_id][1:]:
            print(review_data.iloc[id]["product_title"])
