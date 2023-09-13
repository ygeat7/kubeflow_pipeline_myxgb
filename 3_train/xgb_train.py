import argparse
import pandas as pd
import xgboost

def train(xtrain, ytrain):
    xgb_model = xgboost.XGBRegressor(learning_rate=0.1,
                                     n_estimators=100,
                                     max_depth=10,
                                     gamma=0,
                                     subsample=0.75,
                                     colsample_bytree=1)
    xgb_model.fit(xtrain, ytrain)
    
    return xgb_model
    
if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument(
        '--xtrain',
        type=str,
        help="xtrain data csv"
    )
    argument_parser.add_argument(
        '--ytrain',
        type=str,
        help="ytrain data csv"
    )
    argument_parser.add_argument(
        '--num',
        type=int,
        help="Building Number"
    )
    args = argument_parser.parse_args()
    xtrain = pd.read_csv(args.xtrain)
    ytrain = pd.read_csv(args.ytrain)
    building_num = args.num
    
    xgb_model = train(xtrain, ytrain)
    xgb_model.save_model(f'/xgb_model.model')
    xgb_model.save_model(f'/app/model/xgb_model_{building_num}.model')
