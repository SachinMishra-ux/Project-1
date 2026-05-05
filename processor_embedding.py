import joblib
from sentence_transformers import SentenceTransformer

model_embedding= SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')
model_classification= joblib.load('model/log_classifier.joblib')

def classify_with_embedding(log_message):
    embedding= model_embedding.encode([log_message])
    #prediction= model_classification.predict(embedding) # X, y
    probabilities = model_classification.predict_proba(embedding)
    if probabilities.max() < 0.5:
        return "Unclassified"
    else:
        return model_classification.predict(embedding)[0]

if __name__ == "__main__":
    #log_message= "User User1 logged in at 2024-01-15 10:00:00"
    log_message= "Hello How are you?"
    print(classify_with_embedding(log_message))
    

