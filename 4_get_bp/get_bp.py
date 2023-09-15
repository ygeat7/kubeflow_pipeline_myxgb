from kubeflow.katib import KatibClient
import yaml
import pandas as pd
import time
import argparse
	
def get_experiemt_xgb(yaml_path):
    
    with open(yaml_path, "r") as yaml_file:
        test_yaml = yaml.load(yaml_file)

    name = test_yaml['metadata']['name']
    namespace = test_yaml['metadata']['namespace']

    katib_client = KatibClient()
    
    time.sleep(60)
    while True:
        time.sleep(10)
        if katib_client.get_experiment_status(name,namespace) == 'Succeeded':
             
            experiment = katib_client.get_experiment(name=name,namespace=namespace)
         
            lr=experiment['status']['currentOptimalTrial']['parameterAssignments'][0]['value']
            n=experiment['status']['currentOptimalTrial']['parameterAssignments'][1]['value']
            d=experiment['status']['currentOptimalTrial']['parameterAssignments'][2]['value']
            
            df = pd.DataFrame({'learning_rate':lr,'n_estimates':n,'max_depth':d},index=[0])
            df.to_csv('/best_params.csv',index=False)
            
            katib_client.delete_experiment(name,namespace)
            
            break
    
if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument(
        '--expyaml',
        type=str,
        help="exp yaml file path"
    )
    args = argument_parser.parse_args()
    yaml_path = args.expyaml
    get_experiemt_xgb(yaml_path)
