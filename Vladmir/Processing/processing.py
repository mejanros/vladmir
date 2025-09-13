import os
import tqdm
import argparse
import numpy as np
import pandas as pd

def main() -> pd.DataFrame:
    argument = argparse.ArgumentParser(prog        ='Processing script',
                                       description ='Process kmer file devired from jellyfish',
                                       epilog      ="""This script is used to process kmer files"
                                                    from download_file script into a datafreme of k-mer""")

    argument.add_argument('-i', '---input', required=True, help='directory path of kmers files')
    argument.add_argument('-m', '---metadata', required=True, help='metadata file path')
    argument.add_argument('-f', '---file_name', required=True, help='Dataframe name')
    argument.add_argument('-o', '---output', required=True, help='path where dataframe will be saved.')

    argument = argument.parse_args()
    
    transform(files_path=argument.input,
              metapath=argument.metadata,
              file_name=argument.file_name,
              output=argument.output)
    
def transform(files_path:str, metapath:str, file_name:str, output) -> pd.DataFrame:
    
    metadata    = pd.read_csv(metapath, sep=',')
    cols_select = ['Run','Age','Group']
    metadata    = metadata[cols_select]
    data_final  = pd.DataFrame()  
    #SRR = dict()

    print('processando arquivos raw...')
    print()
    for path_dir, _, files in os.walk(files_path):
        for file in files:
            path = os.path.join(path_dir, file)
            #os arquivos derivados do fasterq-dump precisa sair com extensão .txt
            
            if '.txt' in file:
                srr = file.split('.')[0]
                for r, row in metadata.iterrows():
                    if srr in row.Run: 
                        
                        if 'alzheimer' in row.Group.lower() or 'impairment' in row.Group.lower():
            
                            feature    = 1
                            sra        = row.Run
                            age        = row.Age
                            data       = processed_dataframe(path, feature=feature, sra=sra, age=age)
                            data.fillna(0, inplace=True)
                            data_final = pd.concat([data_final, data])
                            
                        else:
                            
                            feature    = 0
                            sra        =row.Run
                            age        =row.Age
                            data       = processed_dataframe(path, feature=feature, sra=sra, age=age)
                            data.fillna(0, inplace=True)
                            data_final = pd.concat([data_final, data])
                            

    data_final.to_csv(os.path.join(output, file_name), index=False)
    print('Dataframe processado')

def processed_dataframe(path:str, feature:int, sra:str, age:int) -> pd.DataFrame:  
    df   = kmer_counting(path)
    data = df.T
    data.rename(columns = data.loc['kmer'], inplace=True)
    data.drop('kmer', inplace=True)
    data['feature']     = feature
    data['SRR']         = sra
    data['Age']         = age
    return data
    
def kmer_counting(path:str) -> pd.DataFrame:
    data_raw = pd.read_csv(path, sep=" ", names=['kmer', 'counting'])
    data_raw["counting"] = data_raw.counting/data_raw.counting.sum()
    data_raw["counting"] = data_raw["counting"].astype("float64")
    return data_raw

if __name__ == '__main__':
    main()