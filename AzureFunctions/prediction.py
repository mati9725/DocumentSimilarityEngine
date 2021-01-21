import pickle
from preprocessing import preprocess_data

def predict(text, topn=20):
    with open("d2v.model", 'rb') as f:
        model = pickle.load(f)
    # logging.info("model loaded")

    data = preprocess_data(text)
    # logging.info(f"text preprocessed: {data}")
    
    inferred_vector = model.infer_vector(data)
    # logging.info(f"vector inferred")

    response = model.docvecs.most_similar([inferred_vector], topn = topn)
    # logging.info(n)
    return response
