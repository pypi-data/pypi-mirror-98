[![semantic-release](https://img.shields.io/badge/%20%20%F0%9F%93%A6%F0%9F%9A%80-semantic--release-e10079.svg)](https://github.com/semantic-release/semantic-release)

[![License: AGPL v3](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](https://www.gnu.org/licenses/agpl-3.0)

> Project hosting the trainer for generic estimation models.

## _AI_ EASIER.AI Trainer Library

Regarding the way to accurately estimate next possible values based on the context information, the trainer makes use of the Python-based framework [Keras](https://keras.io/) that operates on top of [TensorFlow](https://www.tensorflow.org/) Google's Deep Learning framework. 

Training the models
----  

The trainer is defined as a microservice so that it is easy to be run and deployed in any use case and infrastructure. In addition, it is fully configurable and adaptable for scenario.

With the data produced by the sensors every day, a database is collected for every entity/id so that a predictive model can be produced for each entity. This model will recognize and detect the patterns in the data so that it is able to forecast (predict), considering some context input data, the next value(s) of the time series; or to estimate the value of a specific target feature. 

In order to train the model, an [Elasticsearch](https://www.elastic.co/) database is used to obtain the data. Models are stored in [MINIO](https://min.io) so that they can be loaded from other microservices.


Configuration
----

There are several parameters that can be modified to change how the system learns. These parameters are enclosed in the file `./config/config_trainer_estimation.ini.sample`, and are explained here:


## Configuration parameters guide

INFERENCE section:

* __data_type__: can be `timeseries` or `features` and stands for the type of the data to train the model. If the datatype is `features`, the next two parameters are ignored. 
* __num_forecasts__: Number of values that the system will output when a prediction is requested, when the data_type is `timeseries`.
* __num_previous_measures__: This parameter affects the learning algorithm itself, it stands for the length of the time series, which is the number of previous values considered for the learning. 

ML_INITIAL section:
* __initial_train__: Perform an initial training with all the data available, if there is no previous model to load (true/false)
* __time_window_to_initial__: Period of time for looking back for data in elasticsearch for the initial training. One year is 1y

ML section:

* __algorithm__: Name of the algorithm to be used as Neural Network, currently 'lstm' (default), 'phasedlstm' and 'dense' models are available.
* __learning_rate__: Float number indicating the learning rate for the model. It is recommended to start with a small number as 0.001.
* __epoch_internal__: Number of times the full training set is passed though the neural network for a specific batch size. Default is 50
* __epoch_external__: Number of times the batch_size is increased and the neural network is retrained (epoch_internal times). Default is 1
* __batch_size__: Number of examples or size of the batches in which each epoch_internal is divided. Default is 200 (increases with each epoch_external)
* __initial_validation_split__: Percentage of validation examples used to test the model when training (for the optimizing function). Default is 0.05 
* __validation_split_multiplayer__: Multiplier of the validation split used in each epoch_external. Default is 1.75
* __batch_size_multiplier__: Multiplier of the size of the batches for every epoch external. Default is 1.5
* __minimum_samples__: Minimum number of samples to train the system
* __training_size__: Number of samples which will be used to train the model
* __time_window_to__: Period of time for looking back for data in elasticsearch. One week is 1w. One month would be 1M
* __time_window_from__: Time to start looking back to for data in elasticsearch. Default is now
* __resample__: Resample yes/no
* __resample_time__: Can be empty - Delta time between measures used to resample the timeseries. This will put data every resample_time SECONDS (if there is no data, previous value is used)
* __delta_max_std__: Maximum time in SECONDS between measures to consider the time series as synchronous

The format for time_window parameters follows [Date Math](https://www.elastic.co/guide/en/elasticsearch/reference/current/common-options.html#date-math) from elasticsearch API.

ELASTIC section:

* __index_entities__: Name of the index that stores the entities
* __index_data__: Name of the index that stores the data
* __index_scalers__: Name of the index that stores the  scalers
* __index_predictions__: Name of the index that stores the predictions
* __index_models__: Name of the index that stores the models. __It is overwritten by the environment variable TRAINING_RESULTS_ID__
* __mapping_data__: Name of the mapping that defines the format in the index of data
* __mapping_entities__: Name of the mapping that defines the format in the index of entities
* __mapping_models__: Name of the mapping that defines the format in the index of models
* __mapping_predictions__: Name of the mapping that defines the format in the index of predictions


DATA section:

* __time_index__: Column label used for indexing data (timestamp column), typically `timestamp`
* __inference_features__: Name of the feature(s) that is/are going to be forecasted
* __dataset_features__: Name of the other features used only for training


ELK section

* __elastic_host__: Hostname of elasticsearch. Example: localhost
* __elastic_port__: Port of communication with elasticsearch. Example: `9200` (default of elasticsearch)
 

MINIO section

* __minio_host__: Hostname of MINIO. Example: minio
* __minio_port__: Port of communication with MINIO (default is `9000`)
* __minio_access__: Access key (username) configured in MINIO
* __minio_secret__: Secret key (password) configured in MINIO

Instructions
----

Use this command to launch the container:
 

```
docker run -e ELASTIC_HOST=[$ELASTIC_HOST] -e ELASTIC_PORT=[$ELASTIC_PORT] -e MINIO_ACCESS_KEY=[$MINIO_ACCESS_KEY] -e MINIO_SECRET_KEY=[$MINIO_SECRET_KEY] -e MINIO_SERVICE_HOST=[$MINIO_HOST] -e MINIO_SERVICE_PORT=[$MINIO_PORT] -e TRAINING_RESULTS_ID=[$TRAINING_RESULTS_ID] -e INPUT_FEATURES=[$INPUT_FEATURES] -e PREDICTION_FEATURES=[$PREDICTION_FEATURES] -v ./config/:/usr/app/src/config --name trainer easierai/trainer:1.0  
``` 

Apart from the basic environment variables, you can perform a more advanced configuration by overriding the configuration file inside the trainer ([./config/config.ini](./config/config.ini) to the docker file: `/usr/app/src/config/config.ini`) by passing a volume to the docker image (__notice that the volume is a folder named config in which there is a file named `config.ini`__) adding the tag `-v` to the docker command.

**Notice:**
* Variables `MINIO_ACCESS_KEY` and `MINIO_SECRET_KEY` are, respectively, the username and password of the MINIO service deployed, check the configuration of this service to know more.
* Appart from those variable, you must specify at least @tag (for example 1.1) and the folder that contains the configuration file as a volume. Make sure that inside the folder `./config` there should be a file called `config.ini` with the configuration file previously explained. 
* In addition, you should specify the environment variables for the elasticsearch host, the elasticsearch port and minio host and port. If you do not provide them, the ones in the config.ini file will be used. You should also open the port used as REST API and make sure you use a different port than the inferencer if you plan to launch both on the same machine.
As you can see, there are a few more variables you need to configure:

* ELASTIC_HOST: elasticsearch host IP or hostname.
* ELASTIC_PORT: elasticsearch port.
* MINIO_SERVICE_HOST: MINIO host IP or hostname.
* MINIO_SERVICE_PORT: MINIO port.
* MINIO_ACCESS: MINIO access key (username for the MINIO repository)
* MINIO_SECRET: MINIO secret key (password for the MINIO repository)

You can also add this piece of code in your docker-compose file:

```
  trainer:
    image: easierai/trainer:1.0
    container_name: trainer
    environment:
      NODE_ENV: development
      ELASTIC_HOST: 127.0.0.1
      ELASTIC_PORT: 9200
      MINIO_SERVICE_HOST: 127.0.0.1
      MINIO_SERVICE_PORT:9000
      MINIO_ACCESS: username
      MINIO_SECRET: password
      TRAINING_RESULTS_ID: experiment-001
      INPUT_FEATURES: ratio,free
      INFERENCE_FEATURES: ratio
```