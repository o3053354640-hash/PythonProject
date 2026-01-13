from pyspark.sql import SparkSession
from pyspark.sql.functions import avg, expr

# 创建SparkSession
spark = SparkSession.builder.appName("AgeGroupAnalysis").getOrCreate()

# 读取CSV数据
df = spark.read.option("header", True).option("inferSchema", True).csv(r"c:\Users\QQQQQ\Desktop\k_means_sample.csv")

# 按Age分组，计算Income的中位数和SpendingScore的平均值
result = df.groupBy("Age").agg(
    expr("percentile_approx(Income, 0.5)").alias("Income_Median"),
    avg("SpendingScore").alias("SpendingScore_Avg")
)

# 显示结果
result.show()