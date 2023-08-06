## Machine Learning Platform client SDK for python


## 使用说明

此SDK目标为了方便算法接入mlp，推荐使用此SDK实现算法服务

1. SDK提供什么功能？

    - 启动web服务，并封装对接mlp的接口
    - 提供好用的util类，如log类、minio访问类等
    - 提供大部分算法都会碰到的问题的解决方案，比如多副本信息同步，python多开进程进行模型预测，训练任务排队等等

    如果有需要的功能sdk没有实现，建议提给mlp小组加以实现，因为别人可能有一样的需求，尽量标准化

2. 哪些功能需要算法模块实现？

    算法模块主要关注训练，预测这两个功能
    
    其他工程问题如模型加载内存控制，模型版本管理等，请交给mlp
    
    所以请把算法服务设计得尽量轻量，一般情况下不要依赖其他中间件如mysql（除非算法部分需要依赖，比如依赖es做搜索等）


### 1. 实现对接mlp的接口
继承AlgorithmBase类和PredictorBase类实现相应方法

包括train, load, unload, status, predict, generate_model_id方法

（0.3.18及之后版本一般情况下只需实现train,load,predict即可，unload， ）

通过register函数注册到到app上即可，SDK自动实现对接mlp的接口

可参考example目录下的示例


#### train方法
train方法接受训练数据和参数，生成模型并存储到minio（可为逻辑模型，即预测所依赖的数据都可称为模型）

0.3.18及之后版本，训练方法会被异步调用，方法内部无需显式开启线程/进程，如果训练失败，抛出异常或返回False，正常返回认为训练成功
之前版本需要手动开启异步，此方法结束后训练接口才会返回

|字段名|说明|
|---|---|
|data_config.location|训练数据文件minio路径，格式为tsv，没有header，具体列名按照算法类别不同而不同，格式：/path/to/your/data，不带桶信息，固定为ml-platform-data|
|model_id|mlp指定的模型id，也可自己生成，在train方法中返回即可|
|model_path|此版本没有用上|
|parameter|训练超参，dict类型，可在mlp上配置，也可在调用mlp训练接口时传入|
|parameter.pretrain_model|预训练模型minio存储路径，格式：bucket/path/to/your/data，带有桶信息|
|extend|扩展字段|


### generate_model_id方法
默认随机生成uuid作为model_id并传入train方法，如果需要自定义，可以覆盖此方法。
|字段名|说明|
|extend|扩展字段|


#### load和unload方法
加载/卸载完成后才返回，不要使用异步方式加载。load方法返回的是Predictor对象，用来预测，把预测时依赖的数据全部加载起来放入Predictor对象

unload方法的默认实现是在内存释放load方法返回的对象，如果没有特别需要无需实现卸载方法

|字段名|说明|
|---|---|
|model_id|模型加载起来后的使用id|
|model_path|待加载模型文件存储的位置，如果不为None则从此路径加载，带有桶名|


#### predict方法
模型预测时调用的方法，不同类型算法需返回格式不同

|字段名|说明|
|---|---|
|features|特征，dict类型，不同算法类别有不同特征|
|params|预测时参数，dict类型，标准预测参数有threshold和top_n|


#### status方法
！0.3.18及之后版本有默认实现，即train方法正常返回认为训练完成，抛出异常或返回False认为训练失败，如无特别需要，无需实现此方法

训练状态查询，通过model_id查询训练状态，可接受的状态有 init, training, error, completed, unknown

|字段名|说明|
|---|---|
|model_id|模型id|


### 2. 说明
扩展字段内容：

|字段名|说明|
|---|---|
|extend.remote_ip|调用方ip，即训练数据文件，预训练模型，以及最终生成的模型的存储地址|
|extend.dict_location|字典文件minio路径，格式不限|
|extend.extra_location|额外数据文件minio路径，格式不限|
|extend.app_id|机器人id，如果不属于某机器人则为None|

**如果需要一个算法服务为多个mlp提供服务，在连接minio时都需要通过extend.remote_ip获取调用方ip，连接此ip上的minio，不要直接去连接本地minio**

minio数据包括训练数据，预训练模型，生成的模型的存储路径

### 3. tips

- 推荐通过ml_platform_client.logger.log来输出日志，可使格式标准并可以输出请求uuid，方便排错
- 推荐通过ml_platform_client.minio_accessor.MinIOAccessor来访问minio文件，此类会在本地建立本地文件缓存，提升minio访问效率，如有必要还可把本地缓存路径挂载到docker外


## 不同算法格式说明


### 1. 分类算法

#### 训练数据表头
|字段名|说明|
|---|---|
|sentence|输入语料|
|label|预测标签|
|posneg|正例反例，1表示正例，0表示反例|

#### 预测格式

```json
[
    {
        "label":"标签", //预测标签
        "score":100, //预测分数在0-100之间
        "other_info": [ //其他信息（如果不需要可不填）
            {
                "key": "xxx",
                "value": "xxx"
            }
        ]
    }
]
```

### 2. 序列标注算法：

#### 训练数据表头：
|字段名|说明|
|---|---|
|sentence|输入语料，样例：\<START:PER\>特朗普\<END\>是\<START:LOC\>美国\<END\>总统。

#### 预测格式

```json
[
    {
        "score": 100, //分数
        "entity_list": [ //抽取到的实体
            {
                "name": "特朗普",
                "start_pos": 0,
                "end_pos": 2,
                "label": "PER",
                "score": 100
            },
            {
                "name": "美国",
                "start_pos": 4,
                "end_pos": 5,
                "label": "LOC",
                "score": 100
            }
        ]
    }
]
```


## 更新日志

- 0.3.16: 

    - 训练接口extend中加入remote_ip

    - 优化日志，打印更详细的日志信息
    
    - 修复ml_platform_client.logger.log日志工具，解决日志打印多遍问题
    
    - 接口异常时返回200而不是500，仅用status字段区分
    
    - 修复load和unload时可能出现的数据不一致的bug，从而导致predict失败

- 0.3.18:

    - 异步方式调用训练，无需手动再开启异步
    
    - 提供默认status方法实现

    - 升级到0.3.18时，注意train方法返回model_id方式弃用，如需自定义model_id，请实现generate_model_id方法

## 版本适配

0.3.9及以下适配2.1.6或以下mlp

0.3.16及以上的0.3.X适配2.1.7 mlp

0.4.X适配2.1.8及以上mlp

推荐版本：0.3.16

0.4.X仍在开发中


## 安装

通过pip安装

    pip install ml-platform-client

推荐安装稳定版本，比如

    pip install ml-platform-client==0.3.16

或者是升级到指定的稳定版本

    pip install -U ml-platform-client==0.3.16


## SDK todo list
1. 模型加载时，需处理同时发来的其他对此模型的加载请求，避免重复加载
2. 增加训练任务排队，可控制允许同时执行多少训练任务


## FAQ

1. 不依赖mysql如何持久化模型信息？

    mlp负责记录模型的训练记录和模型信息，算法服务只需提供基本的训练功能，即把数据集转化为模型文件，并存入minio指定位置

2. 多副本如何同步模型加载信息？

    SDK中提供ml_platform_client.load_checker.Checker类来完成，可参考example
    
    Checker通过查询mlp的mysql表获取需要加载哪些模型的信息

    注意：未来会推出mlp集群模式，此模式下不能使用Checker，完全托付给mlp服务端来调用

3. 内置模型如何管理？

    最佳实践为把内置模型上传至mlp模型仓库（YOLO仓库完成后直接上传至YOLO），交付给mlp托管
    
    如果此内置模型无法通过模型文件加载（如意图内置模型），需要到mlp页面接入，并配置为不可加载/卸载，此方案不推荐

4. 算法需要使用GPU怎么办？
    
    目前mlp不参与GPU管理，需要算法实现时自主连接GPU

5. 无需生成模型的算法如聚类如何接入？

    mlp流程目前包含训练、预测两个阶段。针对聚类算法，可在训练阶段持久化所有配置到minio，加载时从minio读取到内存，预测阶段执行真正的聚类逻辑
