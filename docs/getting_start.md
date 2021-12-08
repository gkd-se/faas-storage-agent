# 使用说明
以下内容介绍本项目的使用方法，也可参考.github/目录下的ci脚本理解整个项目的部署流程。本项目使用的前置条件是已经建立好了kubernetes集群并在其上部署了openfaas框架。本项目实验条件为单机并用docker模拟node创建集群，操作过程见步骤0。若已有集群环境可忽略相关步骤。

## 0. 集群配置
1. 安装docker，并登录docker账号，接下来的openfaas平台和用于模拟物理集群的k3d都依赖于docker。https://github.com/openfaas/workshop/blob/master/lab1.md。   
2. 安装kubernetes集群并在其上安装openfaas平台。openfaas平台本质上是由网关、执行引擎、性能监视器等部件组成的kubernetes分布式应用。安装过程参考:https://github.com/openfaas/workshop/blob/master/lab1b.md 在参考文档中提供了多种在单机上模拟集群和使用集群服务提供商的方式。本项目使用K3D方案，利用docker模拟node，可以以极为轻量的方式在本地模拟集群，安装使用的过程如下：
```shell
wget -q -O - https://raw.githubusercontent.com/rancher/k3d/main/install.sh | bash

k3d cluster create CLUSTER_NAMCLUSTER_NAME -s MASTER_NUM -a AGENT_NUM
```
可以根据实验机器能力配置模拟集群的规模。
## 1. 部署认证服务器
1. 安装Django
    ```
    pip3 install django
    ```
2. 安装Django OAuth Toolkit
    ```
    pip3 install django-oauth-toolkit
    ```
3. 创建管理员用户

    ```
    cd auth_server
    python manage.py createsuperuser

    Username: wiliam
    Email address: me@wiliam.dev
    Password:
    Password (again):
    Superuser created successfully.
    ```
4. 启动认证服务器
    ```
    python3 manage.py runserver localhost:10087
    ```
5. 创建应用   
    1. 浏览器中打开 http://localhost:10087/o/applications/register/。
    2. 将Client type设置为Confidential，Authorization grant type设置为Client credentials。
    3. 记录下Client id 和 Client secret。
    4. 重复以上过程，分别为用户函数以及代理服务器创建应用，并记录Client id 和 Client secret。
    5. 访问http://localhost:10087/admin/oauth2_provider/application/ 查看创建结果，例如有agent_server和openfaas_app。
6. 创建token
    1. 访问http://localhost:10087/admin/oauth2_provider/accesstoken/点击右上角ADD ACCESS TOKEN按键创建token。
    2. 设置scope，示例如下。首行为namespace权限设置，以ns开头，示例中表示该函数可新建或删除某个ns。后各行表示该token对某个ns中数据的操作权限，以data开头，例如本示例第二行表示可对名为test_ns的明明空间执行set、get等操作，第三行同理。
        ```
        ns create_ns delete_ns
        data test_ns set get delete exists
        data no_del_ns set get exits
        ```
## 2. 部署存储代理服务器
1. 初始化环境变量
将上文步骤中获得的id、secret以及认证服务地址信息存入环境变量。另本项目采用redis作为示例数据库，因此需将其地址信息一并填入环境变量。
    ```
    export auth_url="http://localhost:10087/o/token/"
    export sa_client_id=<openfaas_app_id>
    export sa_client_secret=<openfaas_app_secret>
    export sas_client_id=<agent_server_id>
    export sas_client_secret=<agent_server_secret>
    export redis_hostname="localhost"
    ```
2. 编译运行agent_server
    ```
    pushd ${workdir}/agent_server/
    cargo build
    popd
    ```
3. 构建成容器并上传到docker hub。
    ```
    sudo docker login -u <DOCKERHUB_USERNAME> -p <DOCKERHUB_TOKEN>
    arch=`arch`
    image_name="whysdocker/sa-${arch}:latest"
    pushd ${workdir}/docker/agent/
    rm ./app/agent_server
    mv ${workdir}/agent_server/target/debug/agent_server ./app/
    sudo docker build -t $image_name .
    sudo docker push $image_name
    popd
    ```
4. 运行或更新集群中的Daemonset应用。
    ```
    arch=`arch`
    yaml="agent-ds-${arch}.yaml"
    pushd ${workdir}/yaml/agent/
    sudo kubectl delete daemonset sa-ds -n openfaas-fn
    sudo kubectl create -f $yaml
    popd
    ```
## 3. 部署及调用openfaas函数应用
利用faas-cli和本仓库的template可以生成应用并编写业务逻辑，使用方法可查看faas-cli的帮助。在此以本项目tests目录下为集成测试而设计的函数应用为例展示应用过程。
1. 部署测试函数
    ```
    pushd ${workdir}/tests/integration_tests/wheel
    sudo faas-cli up -f wheel.yml
    popd
    ```
2. 运行测试函数，可通过命令行，也可打开openfaas管理页面点击invoke按键调用。由于部署需要一定时间，因此上一步完成后需等待一段时间再进行测试。
    ```
    sleep 20s
    echo | faas-cli invoke wheel
    ```
3. 查看返回结果，若一切正常则结果如下
    ```
    token :  test_token
    create_ns test ... ok
    connect_ns test ... ok
    set test ... ok
    exists test ... ok
    get test ... ok
    delete test ... ok
    exists test ... ok
    get test ... ok
    delete_ns test ... ok
    connect_ns test ... ok
    delete_ns test ... ok
    test result: ok. 11 passed; 0 failed
    ```