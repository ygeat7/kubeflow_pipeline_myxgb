import argparse
import pandas as pd
import xgboost
from sklearn.metrics import mean_absolute_error


def load_model(file):
    xgb_load = xgboost.XGBRegressor()
    xgb_load.load_model(file)
    return xgb_load

def test(xtest, ytest, xgb_load):
    ypred = xgb_load.predict(xtest)
    mae = mean_absolute_error(ytest, ypred)
    print(f'Mean Absolute Error (MAE): {mae}')
    
if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument(
        '--xtest',
        type=str,
        help="xtest data csv"
    )
    argument_parser.add_argument(
        '--ytest',
        type=str,
        help="ytest data csv"
    )
    argument_parser.add_argument(
        '--model',
        type=str,
        help="xgb model"
    )
    args = argument_parser.parse_args()
    xtest = pd.read_csv(args.xtest)
    ytest = pd.read_csv(args.ytest)
    model = load_model(args.model)      
    test(xtest, ytest, model)
