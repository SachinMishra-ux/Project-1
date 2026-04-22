from src.processor_regex import classifiy_with_regex
from src.processor_embedding import classify_with_embedding
from src.processor_llm import classify_with_llm
import pandas as pd



def classify(logs):
    labels= []
    for source, log_message in logs:
        label= classify_log(source, log_message)
        labels.append(label)
    return labels

def classify_log(source, log_message):
    if source== "LegacyCRM":
        label= classify_with_llm(log_message)
    
    else:
        label= classifiy_with_regex(log_message)
        if label is None:
            label= classify_with_embedding(log_message)
    return label

def classify_csv_logs(csv_file_or_df):
    if isinstance(csv_file_or_df, pd.DataFrame):
        df = csv_file_or_df.copy()
    else:
        df = pd.read_csv(csv_file_or_df)
    df['label']= df.apply(lambda x: classify_log(x['source'], x['log_message']), axis=1)
    #df.to_csv("classified_logs.csv", index=False)
    return df

if __name__ == "__main__":
    # logs= [
    #     ("LegacyCRM", "Lead conversion failed for prospect ID 7842 due to missing contact information."),
    #     ("LegacyCRM", "API endpoint 'getCustomerDetails' is deprecated and will be removed in version 3.2. Use 'fetchCustomerInfo' instead."),
    #     ("LegacyCRM", "User User1 logged in at 2024-01-15 10:00:00"),
    #     ("AnalyticsEngine", "Unauthorized access to data was attempted"),
    #     ("BillingSystem", "Hi bro how are you"),
    #     ("ThirdPartyAPI", "nova.compute.claims [req-a07ac654-8e81-416d-bfbb-189116b07969 113d3a99c3da401fbd62cc2caa5b96d2 54fadb412c4e40cdbaed9335e4c35a9e - - -] [instance: bf8c824d-f099-4433-a41e-e3da7578262e] Total memory: 64172 MB, used: 512.00 MB")
    # ]
    # print(classify(logs))
    classify_csv_logs("/Users/sachinmishra/Desktop/Project-1/training/dataset/synthetic_logs.csv")
        
    
        