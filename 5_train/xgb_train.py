import argparse
import pandas as pd
import xgboost

def train(xtrain, ytrain, bp):
		
    lr = bp['learning_rate'][0]
    n = bp['n_estimates'][0]
    d = bp['max_depth'][0]

    xgb_model = xgboost.XGBRegressor(learning_rate=lr,
                                     n_estimators=n,
                                     max_depth=d,
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
        '--best_params',
        type=str,
        help="best params csv"
    )
    args = argument_parser.parse_args()
    xtrain = pd.read_csv(args.xtrain)
    ytrain = pd.read_csv(args.ytrain)
    bp_df = pd.read_csv(args.best_params)
    
    xgb_model = train(xtrain, ytrain, bp_df)
    xgb_model.save_model(f'/xgb_model.model')
