from kubeflow.katib import KatibClient
import yaml
import argparse

def create_experiement_xgb(test_yaml):
    katib_client = KatibClient()
    
    with open(test_yaml, "r") as yaml_file:
        experiment_config = yaml.load(yaml_file)
		
    namespace = experiment_config['metadata']['namespace']

    try:
        katib_client.create_experiment(experiment_config, namespace)
    except:
        pass
    
if __name__ == "__main__":
    argument_parser = argparse.ArgumentParser()
    argument_parser.add_argument(
        '--expyaml',
        type=str,
        help="Input test yaml"
    )
    args = argument_parser.parse_args()
    test_yaml = args.expyaml
    create_experiement_xgb(test_yaml)
