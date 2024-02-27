### **KG与LLM协同，python后端**

# 一、后端启动

1. 安装项目的依赖库，进入backend/src/中运行

```jsx
pip install -r requirements.txt
```

2. 完成环境配置，设置node4j数据库等信息，在根目录下新建.env文件，可以照此填写

```jsx
OPENAI_KEY=sk-XXXXXXXXXXXXXXXXXXX
NEO4J_URL=neo4j://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASS=aowang
MODEL_NAME=gpt-3.5-turbo
```

3. 开启后端，进入backend/src/中运行

```jsx
python3 main.py
```

# 二、图谱相关（<font color="red">若有部署好的图谱，可跳过此步，在环境变量中配置neo4j的url、账号、密码即可</font>）

### 图谱下载与启动
1. 可以选择本地部署neo4j数据库，或使用官方的云端数据库。本项目使用本地部署的neo4j 4.2.26版本
2. 首先在本机安装openjdk11版本

```jsx
sudo apt install openjdk-11-jre-headless
```

3. 下载neo4j 4.2.26版本
4. 解压下载的安装包：

```jsx
tar -axvf neo4j-community-4.4.26-unix.tar.gz
```

5. 进入neo4j的根目录，启动neo4j

```jsx
./bin/neo4j start
```

### 导入图谱dump数据

1. 首先停止正在运行的neo4j，在根目录中运行

```jsx
./bin/neo4j stop
```

2. 修改配置文件，进入 gedit conf\neo4j.conf，第9行下面填加：

```jsx
# The name of the default database
#dbms.default_database=neo4j
dbms.active_database=ming.db    \\<数据库名字>.db
```

3. 进入bin文件夹中，运行

```jsx
neo4j-admin load --from=<需要导入文件的地址> --database=<导入的数据库> --force

neo4j-admin load --from=/home/aowang/history-knowledge-graph-neo4j.dump --database=mingchao.db --force //例子
```

4. 导入时版本升级报错，解决方法：在配置为文件中将 dbms.allow_upgrade=true 打开

# 三、前端调用

1. 前端调用方法，可以参考根目录下的myChat.js

```jsx
    const response = await axios.get("http://127.0.0.1:7860/predict", {
        params: { message: userInput },
      });
```
2. 进入[http://0.0.0.0:7860/](http://0.0.0.0:7860/)查看后端响应情况
3. 进入[http://localhost:7474](http://localhost:7474/)查看neo4j数据库情况

**感谢https://github.com/ongdb-contrib/langchain2ongdb 的优秀工作！！**
