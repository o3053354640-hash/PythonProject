import os
import sys
import tempfile
import subprocess

# ========== 1. 强制设置所有环境变量（在导入 pyspark 之前）==========
# Python 路径
os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable

# Java 路径
os.environ['JAVA_HOME'] = r'C:\Program Files\Java\jdk-17'

# Hadoop 路径
os.environ['HADOOP_HOME'] = r'D:\test\hadoop\hadoop-3.4.3'

# 网络配置（解决 Python worker 连接问题）
os.environ['SPARK_LOCAL_IP'] = '127.0.0.1'
os.environ['PYTHONHASHSEED'] = '0'

# 更新 PATH
os.environ['PATH'] = (
        os.environ['JAVA_HOME'] + r'\bin;' +
        os.environ['HADOOP_HOME'] + r'\bin;' +
        os.environ.get('PATH', '')
)

# 创建临时目录（使用用户目录避免权限问题）
temp_dir = os.path.join(os.environ['USERPROFILE'], 'temp', 'spark')
os.makedirs(temp_dir, exist_ok=True)
os.makedirs(os.path.join(temp_dir, 'warehouse'), exist_ok=True)

os.environ['SPARK_LOCAL_DIRS'] = temp_dir
os.environ['SPARK_WORKER_DIR'] = temp_dir

# 禁用 IPv6（Windows 兼容性）
os.environ['JAVA_TOOL_OPTIONS'] = '-Djava.net.preferIPv4Stack=true'

# ========== 2. 导入 pyspark ==========
from pyspark.sql import SparkSession
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.feature import VectorAssembler


def test_spark():
    """测试 Spark 功能"""

    # 创建 SparkSession 带完整配置
    spark = SparkSession.builder \
        .appName("Java17_Spark_Test") \
        .master("local[1]") \
        .config("spark.driver.host", "127.0.0.1") \
        .config("spark.driver.bindAddress", "127.0.0.1") \
        .config("spark.driver.port", "0") \
        .config("spark.sql.warehouse.dir", os.path.join(temp_dir, 'warehouse')) \
        .config("spark.local.dir", temp_dir) \
        .config("spark.sql.shuffle.partitions", "2") \
        .config("spark.driver.memory", "1g") \
        .config("spark.executor.memory", "1g") \
        .config("spark.python.worker.reuse", "false") \
        .config("spark.network.timeout", "600s") \
        .config("spark.executor.heartbeatInterval", "60s") \
        .config("spark.python.worker.timeout", "600") \
        .config("spark.sql.execution.arrow.pyspark.enabled", "false") \
        .getOrCreate()

    try:
        print(f"Spark 版本: {spark.version}")
        print(f"Spark Master: {spark.sparkContext.master}")
        print(f"临时目录: {temp_dir}")
        print("-" * 50)

        # 测试1: 创建简单数据（不涉及 Python UDF）
        print("测试1: 创建 DataFrame...")
        df = spark.range(5)
        print(f"成功创建 {df.count()} 行数据")

        # 测试2: 创建带列的数据
        print("\n测试2: 创建带列的数据...")
        data = [(1, "Alice", 20), (2, "Bob", 25), (3, "Charlie", 30)]
        df2 = spark.createDataFrame(data, ["id", "name", "age"])
        df2.show()

        # 测试3: ML 测试
        print("\n测试3: 机器学习测试...")
        ml_data = spark.createDataFrame([
            (1, 20, 500, 0),
            (2, 45, 8000, 1),
            (3, 30, 3000, 0),
            (4, 50, 10000, 1),
        ], ["id", "age", "income", "label"])

        assembler = VectorAssembler(inputCols=["age", "income"], outputCol="features")
        features_data = assembler.transform(ml_data)

        lr = LogisticRegression(featuresCol="features", labelCol="label")
        model = lr.fit(features_data)

        print(f"模型训练成功！")
        print(f"系数: {model.coefficients}")
        print(f"截距: {model.intercept}")

        # 预测
        predictions = model.transform(features_data)
        print("\n预测结果:")
        predictions.select("id", "age", "income", "label", "prediction").show()

        print("\n" + "=" * 50)
        print(">>> 所有测试通过！Java 17 + Spark 环境正常！")
        print("=" * 50)

        return True

    except Exception as e:
        print(f"错误: {e}")
        import traceback
        traceback.print_exc()
        return False
    finally:
        spark.stop()
        print("\nSpark 已停止")


if __name__ == "__main__":
    success = test_spark()
    if not success:
        print("\n如果仍然失败，请尝试以下操作：")
        print("1. 以管理员身份运行 PyCharm")
        print("2. 临时关闭 Windows Defender 防火墙")
        print("3. 检查是否有杀毒软件阻止 Python 子进程")