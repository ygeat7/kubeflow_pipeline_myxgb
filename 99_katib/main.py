import pandas as pd
import xgboost
import argparse
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

def train():
	X_train = pd.read_csv('data/xtrain.csv')
	y_train = pd.read_csv('data/ytrain.csv')
	
	xtrain, xtest, ytrain, ytest = train_test_split(X_train, y_train, test_size=0.2)
	
	parser = argparse.ArgumentParser()
	parser.add_argument('--learning_rate', required=False, type=float, default=0.1)
	parser.add_argument('--n_estimators', required=False, type=int, default=100)
	parser.add_argument('--max_depth', required=False, type=int, default=5)
	args = parser.parse_args()
	
	xgb_model = xgboost.XGBRegressor(learning_rate=args.learning_rate,
	                                 n_estimators=args.n_estimators,
	                                 max_depth=args.max_depth,
	                                 gamma=0,
	                                 subsample=0.75,
	                                 colsample_bytree=1)
	xgb_model.fit(xtrain,ytrain)
	pred = xgb_model.predict(xtest)
	mae = mean_absolute_error(ytest, pred)
	
	print('mae='+str(mae))

if __name__ == '__main__':		
	train()
