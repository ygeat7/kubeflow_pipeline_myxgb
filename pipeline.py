import kfp
import kfp.components as comp
from kfp import dsl

@dsl.pipeline(
    name='xgb-pipeline-katib',
    description='xgb pipeline with katib'
)

def xgb_pipeline_katib(building_num: int=1):
    
    xgb_pvc = dsl.PipelineVolume('xgb-pvc')
    exp_pvc = dsl.PipelineVolume('exp-pvc')
    data_pvc = dsl.PipelineVolume('data-pvc')
    
    data_load = dsl.ContainerOp(
        name='data load',
        image='kubeflow-registry.default.svc.cluster.local:30000/xgb_data_load:5.0',
        command=['python', 'data_load.py'],
        arguments=[
            '--num', str(building_num)
        ],
        file_outputs={'dataset' : '/dataset.csv'}
    )
    
    data_split = dsl.ContainerOp(
        name='data split',
        image='kubeflow-registry.default.svc.cluster.local:30000/data_split:5.5',
        arguments=[
            '--dataset', dsl.InputArgumentPath(data_load.outputs['dataset']),
            '--num', str(building_num)
        ],
        command=['python', 'data_split.py'],
        file_outputs={'xtrain' : '/xtrain.csv',
                      'xtest' : '/xtest.csv',
                      'ytrain' : '/ytrain.csv',
                      'ytest' : '/ytest.csv',
                      'expyaml' : '/test.yaml'},
        pvolumes={'/app/exp': exp_pvc,
		  '/app/data': data_pvc}
    )

    katib_create_exp = dsl.ContainerOp(
        name='create katib experiment',
        image='kubeflow-registry.default.svc.cluster.local:30000/create_exp:5.1',
        arguments=[
            '--expyaml', dsl.InputArgumentPath(data_split.outputs['expyaml'])
        ],
        command=['python', 'create_exp.py'],
    )

    get_best_params = dsl.ContainerOp(
        name='get best params',
        image='kubeflow-registry.default.svc.cluster.local:30000/get_bp:5.3',
        arguments=[
            '--expyaml', dsl.InputArgumentPath(data_split.outputs['expyaml'])
        ],
        command=['python', 'get_bp.py'],
	file_outputs={'best_params' : '/best_params.csv'}
    )

    train = dsl.ContainerOp(
        name='xgb train',
        image='kubeflow-registry.default.svc.cluster.local:30000/xgb_train:5.1',
        arguments=[
            '--xtrain',  dsl.InputArgumentPath(data_split.outputs['xtrain']),
            '--ytrain',  dsl.InputArgumentPath(data_split.outputs['ytrain']),
            '--best_params', dsl.InputArgumentPath(get_best_params.outputs['best_params'])
        ],
        command=['python', 'xgb_train.py'],
        file_outputs={'model' : '/xgb_model.model'}
    )
    
    test = dsl.ContainerOp(
        name='test and evaluation',
        image='kubeflow-registry.default.svc.cluster.local:30000/test_eval:5.1',
        arguments=[
            '--xtest',  dsl.InputArgumentPath(data_split.outputs['xtest']),
            '--ytest',  dsl.InputArgumentPath(data_split.outputs['ytest']),
            '--model',  dsl.InputArgumentPath(train.outputs['model']),
            '--num', str(building_num)
        ],
        command=['python', 'test_eval.py'],
        pvolumes={'/app/model': xgb_pvc},
        file_outputs={'mlpipeline-metrics' : '/mlpipeline-metrics.json'}
    )
    
    data_split.after(data_load)
    katib_create_exp.after(data_split)
    get_best_params.after(katib_create_exp)
    train.after(data_split)
    test.after(train)

if __name__ == "__main__":
    import kfp.compiler as compiler
    compiler.Compiler().compile(xgb_pipeline_katib, __file__ + ".tar.gz")
