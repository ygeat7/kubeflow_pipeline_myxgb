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
    return ypred

def evaluation(ytest, ypred):
    mae = mean_absolute_error(ytest, ypred)
    return mae
    
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
    argument_parser.add_argument(
        '--num',
        type=int,
        help="Building Number"
    )
    
    args = argument_parser.parse_args()
    xtest = pd.read_csv(args.xtest)
    ytest = pd.read_csv(args.ytest)
    model_num = args.num
    
    model_new = load_model(args.model)
    ypred_new = test(xtest, ytest, model_new)
    mae_new = evaluation(ytest, ypred_new)
    
    try:    
        model_old = load_model(f'/app/model/xgb_model_{model_num}.model')
        ypred_old = test(xtest, ytest, model_old)
        mae_old = evaluation(ytest, ypred_old)
        
        metrics = {
          'metrics': [{
              'name': 'MAE (New Model)',
              'numberValue':  mae_new,
            },{
              'name': 'MAE (Old Model)',
              'numberValue':  mae_old,
            }]}
        print(metrics) 
        import json
        with open('/mlpipeline-metrics.json','w') as f:
            json.dump(metrics, f)

        if mae_new < mae_old : 
            model_new.save_model(f'/app/model/xgb_model_{model_num}.model')
    except:
        model_new.save_model(f'/app/model/xgb_model_{model_num}.model')
        
        metrics = {
          'metrics': [{
              'name': 'MAE (New Model)',
              'numberValue':  mae_new,
            }]}
        print(metrics)
        import json
        with open('/mlpipeline-metrics.json','w') as f:
            json.dump(metrics, f)
