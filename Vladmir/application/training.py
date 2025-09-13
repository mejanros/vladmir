
import pandas as pd 
import os
import argparse
import pickle
import pathlib
import logging
from sklearn.metrics  import classification_report
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB

from sklearn.model_selection import train_test_split

def main():
    base_dir = pathlib.Path(__file__).resolve().parent.parent
    model_dir_path = os.path.join(base_dir, "data/models")

    models = {'ExtraTree':ExtraTreesClassifier(), 'RandomForest':RandomForestClassifier(), 'KNeighbor':KNeighborsClassifier(), 'GaussianNB':GaussianNB()}

    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument('-i', '--input', required=True, help='path to dataframe')
    argument_parser.add_argument('-r', '--report', required=False, action='store_true')
    argument_parser.add_argument('-save', '--model_save', required=True, action='store_true', help='if true, it saves model')
    argument_parser.add_argument('-o', '--model_path_save', required=False, type=pathlib.Path, default=model_dir_path ,help='destinary path in order to save model')
    argument_parser.add_argument('-k', '--kmer', required=True, help="size of kmer to save model's name")

    argument_parser.add_argument('-m', '--model', choices=['ExtraTree', 'RandomForest', 'KNeighbor', 'GaussianNB'])
    
    
    arguments = argument_parser.parse_args()

    train_test (path=arguments.input,
               report=arguments.report,
               save_model=arguments.model_save,
               output_model=arguments.model_path_save,
               kmer=arguments.kmer,
               
               model=models[arguments.model]
    )


def train_test(path, report, save_model, output_model, kmer, model):
    
    
    data = pd.read_csv(path)
    data = data.fillna(0)

    X=data.drop(['feature', 'SRA'], axis=1)
    y=data['feature']

    model = model
    model_name = model.__class__.__name__

    X_train, X_test, y_train, y_test = train_test_split(X, y)
    X_train_columns = X_train.columns.to_list()

    file_name = f'list_features_{model_name}.pkl'
    base_dir = pathlib.Path(__file__).resolve().parent.parent.parent   
    model_dir_path = os.path.join(base_dir, "data/models")

    with open(os.path.join(model_dir_path, file_name), 'wb') as handle:
        pickle.dump(X_train_columns, handle)

    import logging
    logging.info("Training model")
    
    model.fit(X_train, y_train)
    
    print('Making prediction on data training')
    y_prediction = model.predict(X_test)
    #classificatian report
    print('generating classification report')
    print()
    report = classification_report(y_test, y_prediction)
    print(report)
    
    if not output_model:
        output_model = model_dir_path
    
    if save_model:
        output_model = model_dir_path
        print(f'salvando o model em {output_model}')
        model_seriatilization(model_path=output_model, model=model, model_name=model_name, kmer_size=kmer)
    
    return report

def model_seriatilization(model_path:str, model, model_name, kmer_size):
    model_name = f"{model_name}_kmer_{kmer_size}"
    with open(os.path.join(model_path, model_name), 'wb') as file:
        pickle.dump(model, file)

if __name__ == '__main__':
    main()




