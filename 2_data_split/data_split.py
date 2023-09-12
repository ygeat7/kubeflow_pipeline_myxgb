import argparse
import pandas as pd
from sklearn.model_selection import train_test_split

def get_train_test_data(dataset):
    
    train, test = train_test_split(dataset, test_size=0.2, random_state=0)
    print('shape of training data : ', train.shape)
    print('shape of testing data : ', test.shape)
    
    X_train = train.drop(columns=['power'], axis=1)
    y_train = train['power']
    X_test = test.drop(columns=['power'], axis=1)
    y_test = test['power']
    
    return X_train, X_test, y_train, y_test

if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument(
        '--dataset',
        type=str,
        help="Input data csv"
    )
    args = argument_parser.parse_args()
    dataset = args.dataset
    dataset = pd.read_csv(dataset)
    
    X_train, X_test, y_train, y_test = get_train_test_data(dataset)
    
    X_train.to_csv('/xtrain.csv', index=False)
    X_test.to_csv('/xtest.csv', index=False)
    y_train.to_csv('/ytrain.csv', index=False)
    y_test.to_csv('/ytest.csv', index=False)
