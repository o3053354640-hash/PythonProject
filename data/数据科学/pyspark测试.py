import findspark

# 1. 自动定位本地 Spark 路径
# 如果你没配环境变量，也可以手动指定路径：findspark.init("C:/spark-3.x.x-bin-hadoop3")
findspark.init()

import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.functions import udf, col
from pyspark.sql.types import StringType, StructType, StructField, IntegerType, FloatType
import time


def main():
    # 2. 创建 SparkSession
    # 如果本地有版本冲突，这里最容易报错。使用 findspark 后会稳定很多。
    spark = SparkSession.builder \
        .appName("IncomeAnalysis_Fixed_with_FindSpark") \
        .master("local[*]") \
        .config("spark.sql.execution.arrow.pyspark.enabled", "true") \
        .getOrCreate()

    try:
        # 定义 UDF 的返回结构
        result_schema = StructType([
            StructField("category", StringType(), True),
            StructField("living_standard", StringType(), True),
            StructField("per_capita_income", FloatType(), True),
            StructField("adjusted_income", FloatType(), True)
        ])

        # 定义分类函数
        def advanced_income_category(income, city, family_members):
            inc = float(income or 0)
            fam = family_members if (family_members and family_members > 0) else 1
            per_capita = inc / fam

            cost_factors = {"北京": 1.5, "上海": 1.5, "深圳": 1.4, "广州": 1.3}
            factor = cost_factors.get(city, 1.0)
            adj_income = per_capita / factor

            # 简化分类逻辑以便测试
            cat = "高收入" if adj_income > 50000 else "普通"
            return {
                "category": f"{cat} ({city})",
                "living_standard": "良好" if adj_income > 50000 else "一般",
                "per_capita_income": per_capita,
                "adjusted_income": adj_income
            }

        income_udf = udf(advanced_income_category, result_schema)

        # 3. 创建测试数据
        data = [("张三", 150000, "北京", 3), ("李四", 50000, "成都", 1)]
        schema = ["Name", "Income", "City", "Family_Members"]
        df = spark.createDataFrame(data, schema=schema)

        # 4. 执行逻辑
        print("--- 正在执行分析 ---")
        df_final = df.withColumn("Analysis", income_udf(col("Income"), col("City"), col("Family_Members")))

        # 展示结果（触发 Action）
        df_final.select("Name", "City", "Analysis.*").show()

    except Exception as e:
        print(f"运行中出现异常: {e}")
    finally:
        # 5. 安全关闭
        print("正在关闭 Spark 会话...")
        spark.stop()


if __name__ == "__main__":
    main()