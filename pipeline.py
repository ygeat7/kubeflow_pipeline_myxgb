import kfp
import kfp.components as comp
from kfp import dsl

@dsl.pipeline(
    name='jklim-xgb',
    description='jklim xgb test'
)

def jklim_xgb_pipeline(building_num: int=1):
    
    pvc = dsl.PipelineVolume('xgb-pvc')
    
    data_load = dsl.ContainerOp(
        name='data load',
        image='kubeflow-registry.default.svc.cluster.local:30000/xgb_data_load:4.0',
        command=['python', 'data_load.py'],
        arguments=[
            '--num', str(building_num)
        ],
        file_outputs={'dataset' : '/dataset.csv'}
    )
    
    data_split = dsl.ContainerOp(
        name='data split',
        image='kubeflow-registry.default.svc.cluster.local:30000/data_split:4.0',
        arguments=[
            '--dataset', dsl.InputArgumentPath(data_load.outputs['dataset'])
        ],
        command=['python', 'data_split.py'],
        file_outputs={'xtrain' : '/xtrain.csv',
                      'xtest' : '/xtest.csv',
                      'ytrain' : '/ytrain.csv',
                      'ytest' : '/ytest.csv'}
    )

    train = dsl.ContainerOp(
        name='xgb train',
        image='kubeflow-registry.default.svc.cluster.local:30000/xgb_train:4.2',
        arguments=[
            '--xtrain',  dsl.InputArgumentPath(data_split.outputs['xtrain']),
            '--ytrain',  dsl.InputArgumentPath(data_split.outputs['ytrain']),
            '--num', str(building_num)
        ],
        command=['python', 'xgb_train.py'],
        pvolumes={'/app/model': pvc},
        file_outputs={'model' : '/xgb_model.model'}
    )
    
    test = dsl.ContainerOp(
        name='xgb test',
        image='kubeflow-registry.default.svc.cluster.local:30000/xgb_test:4.0',
        arguments=[
            '--xtest',  dsl.InputArgumentPath(data_split.outputs['xtest']),
            '--ytest',  dsl.InputArgumentPath(data_split.outputs['ytest']),
            '--model',  dsl.InputArgumentPath(train.outputs['model'])
        ],
        command=['python', 'xgb_test.py'],
        file_outputs={'mlpipeline-metrics' : '/mlpipeline-metrics.json'}
    )
    
    data_split.after(data_load)
    train.after(data_split)
    test.after(train)

if __name__ == "__main__":
    import kfp.compiler as compiler
    compiler.Compiler().compile(jklim_xgb_pipeline, __file__ + ".tar.gz")
