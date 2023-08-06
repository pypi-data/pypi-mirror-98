from selfcheck.algorithm_type import AlgorithmType
from selfcheck.config import SelfCheckConfig, TrainConfig, PredictConfig
from selfcheck.self_check_runner import SelfCheckRunner

if __name__ == '__main__':
    config = SelfCheckConfig(host='172.16.99.29', algorithm_name='km_service', algorithm_port=1972,
                             algorithm_type=AlgorithmType.text_cluster,
                             minio_access_key='24WTCKX23M0MRI6BA72Y',
                             minio_secret_key='6mxoQMf1Lha2q1H3fp3fjNHEZRJJ7LvbC5k3+CQX')

    train_config = TrainConfig()

    with open('../static/cluster_predict.csv') as f:
        data = f.readlines()
    predict_config = PredictConfig(features={'sentences': data})

    task_runner = SelfCheckRunner(config)
    task_runner.run_all(train_config, predict_config)
