import pickle
import argparse
import numpy  as np
import pandas as pd
#from processing import kmer_counting


def main():

    argument = argparse.ArgumentParser()
    argument.add_argument('-f', '--file_path', required=True, help='path to the file.txt')
    argument.add_argument('-m', '--model_path', required=True, help='Path to the trained model')
    argument.add_argument('-l', '--model_list', required=True, help='Path to the train features')
    
    arguments = argument.parse_args()

    predictions(file=arguments.file_path, 
                model_path=arguments.model_path,
                model_features=arguments.model_list)

def predictions(file:str, model_path, model_features): 
    with open(model_path, 'rb') as handle:
        model = pickle.load(handle)
    data = transform_data_prediction(file, list_path=model_features)

    label = {0:'Sem Alzheimer', 1:'Alzheimer detectado'}

    prediction = model.predict(data)
    print('------------------------------------------')
    print(f'Predição concluída: {label[prediction[0]]}')
    print('------------------------------------------')


def transform_data_prediction(path, list_path):
    data = kmer_counting(path)
    data = data.T
    data.rename(columns=data.loc['kmer'], inplace=True)
    data.drop('kmer', inplace=True)

    if 'Age' not in data.columns:
        data['Age'] = 0

    with open(list_path, 'rb') as file:
        features_name = pickle.load(file)
    
    for column in features_name:
        if column not in data.columns:
            data[column] = 0.0
    
    data = data[features_name]
    return data

def kmer_counting(path:str) -> pd.DataFrame:
    data_raw = pd.read_csv(path, sep=" ", names=['kmer', 'counting'])
    data_raw["counting"] = data_raw.counting/data_raw.counting.sum()
    data_raw["counting"] = data_raw["counting"].astype("float64")
    return data_raw


if __name__ == "__main__":
    main()