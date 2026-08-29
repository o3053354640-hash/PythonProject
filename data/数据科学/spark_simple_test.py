from pyspark.sql import SparkSession


def main():
    spark = SparkSession.builder \
        .appName("IncomeAnalysis_Pandas") \
        .master("local[*]") \
        .getOrCreate()

    try:
        data = [("张三", 150000, "北京", 3), ("李四", 50000, "成都", 1)]
        df = spark.createDataFrame(data, ["Name", "Income", "City", "Family_Members"])

        # 转换为 Pandas 处理
        pandas_df = df.toPandas()

        # 使用 Pandas 处理所有逻辑
        city_factor = {"北京": 1.5, "上海": 1.5, "深圳": 1.4, "广州": 1.3}

        # 人均收入
        pandas_df["per_capita_income"] = pandas_df["Income"] / pandas_df["Family_Members"]

        # 城市因子
        pandas_df["factor"] = pandas_df["City"].map(city_factor).fillna(1.0)

        # 调整后收入
        pandas_df["adjusted_income"] = pandas_df["per_capita_income"] / pandas_df["factor"]

        # 类别
        pandas_df["category"] = pandas_df["adjusted_income"].apply(
            lambda x: "高收入" if x > 50000 else "普通"
        )

        # 生活水平
        pandas_df["living_standard"] = pandas_df["adjusted_income"].apply(
            lambda x: "良好" if x > 50000 else "一般"
        )

        # 转回 Spark DataFrame（可选）
        result = spark.createDataFrame(
            pandas_df[["Name", "City", "category", "living_standard",
                       "per_capita_income", "adjusted_income"]]
        )

        result.show()

    except Exception as e:
        print(f"错误: {e}")
    finally:
        spark.stop()


if __name__ == "__main__":
    main()