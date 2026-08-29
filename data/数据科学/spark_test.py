from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.classification import LogisticRegression
from pyspark.sql.functions import col

# --- 第一步：初始化 Spark (打通环境) ---
spark = SparkSession.builder \
    .appName("MiniMLPipeline") \
    .master("local[*]") \
    .getOrCreate()

# --- 第二步：准备数据 (模拟从 HDFS/SQL 读取) ---
# 字段：用户ID, 年龄, 存款金额, 是否购买(标签：1买, 0不买)
data = [
    (1, 25, 10000, 0),
    (2, 45, 80000, 1),
    (3, 35, 50000, 1),
    (4, 20, 5000,  0),
    (5, 55, 120000, 1),
    (6, 30, 15000, 0)
]
columns = ["user_id", "age", "balance", "label"]
df = spark.createDataFrame(data, columns)

# --- 第三步：SQL 处理 (清洗与筛选) ---
# 假设我们只想训练“成年人”的数据
df.createOrReplaceTempView("raw_data")
clean_df = spark.sql("SELECT age, balance, label FROM raw_data WHERE age >= 18")

# --- 第四步：特征工程 (核心转化) ---
# Spark ML 算法要求输入必须是一个叫 "features" 的向量列
# 我们把 'age' 和 'balance' 两个散装特征打包成一个向量
assembler = VectorAssembler(inputCols=["age", "balance"], outputCol="features")
training_prepared = assembler.transform(clean_df)

print("特征工程后的数据预览：")
training_prepared.select("features", "label").show()

# --- 第五步：模型训练 (算法接入) ---
# 创建逻辑回归算法实例
lr = LogisticRegression(featuresCol="features", labelCol="label")

# 训练模型（这就是“练大脑”的过程）
model = lr.fit(training_prepared)

# --- 第六步：预测新数据 (闭环) ---
# 假设现在来了一个新客户：38岁，存款 60000
test_data = spark.createDataFrame([(38, 60000)], ["age", "balance"])
test_prepared = assembler.transform(test_data)

# 使用训练好的模型进行预测
predictions = model.transform(test_prepared)

print("新客户预测结果：")
# prediction 为 1 表示预测会买，0 表示不买
predictions.select("age", "balance", "probability", "prediction").show()

# 停止 Spark
spark.stop()