# pyspark_polars_tutorial_pdf.py
from weasyprint import HTML, CSS
from pygments import highlight
from pygments.lexers import PythonLexer, BashLexer, TextLexer
from pygments.formatters import HtmlFormatter

# --------------------------
# 1. 文档内容
# --------------------------
tutorial_sections = [
    ("数据读取", """
PySpark:
spark.read.csv('data.csv', header=True, inferSchema=True)
spark.read.parquet('data.parquet')

Polars:
pl.read_csv('data.csv')
pl.read_parquet('data.parquet')
"""),
    ("基本操作", """
选择列:
PySpark: df.select('Age','Salary')
Polars: df.select(['Age','Salary'])

过滤:
PySpark: df.filter(df.Age > 30)
Polars: df.filter(pl.col('Age') > 30)

新增列:
PySpark: df.withColumn('Salary_plus', df.Salary*1.1)
Polars: df.with_columns((pl.col('Salary')*1.1).alias('Salary_plus'))

排序:
PySpark: df.orderBy('Age', ascending=False)
Polars: df.sort('Age', descending=True)
"""),
    ("聚合与分组", """
PySpark:
df.groupBy('Dept').agg({'Salary':'mean','Dept':'count'})

Polars:
df.groupby('Dept').agg([pl.count().alias('cnt'), pl.mean('Salary').alias('avg_salary')])
"""),
    ("开窗函数", """
分组排名:
PySpark: rank().over(Window.partitionBy('Dept').orderBy('Age'))
Polars: pl.col('Age').rank().over('Dept')

TopN:
PySpark: df.withColumn('rk', rank().over(Window.partitionBy('Class').orderBy(desc('Score')))).filter('rk<=3')
Polars: pl.col('Score').rank(descending=True).over('Class').alias('rk').filter(pl.col('rk')<=3)
"""),
    ("时间序列 / 滑动窗口", """
PySpark:
F.avg('Sales').over(Window.orderBy('Date').rowsBetween(-6,0))

Polars:
pl.col('Sales').rolling_mean(window_size=7)
"""),
    ("适用场景", """
PySpark:
优势: 分布式计算、大数据处理、集群环境、延迟容忍高
场景: 离线大规模 ETL、海量日志分析、机器学习特征工程

Polars:
优势: 高性能单机、低延迟、表达式式 API、易于原型开发
场景: 单机数据分析、数仓指标计算、风控实时特征处理、小规模 ML 数据处理
""")
]

# --------------------------
# 2. 高亮代码函数
# --------------------------
def highlight_code(code):
    return highlight(code, PythonLexer(), HtmlFormatter())

# --------------------------
# 3. 生成 HTML
# --------------------------
html_sections = ""
toc = "<h2>目录</h2><ul>"
for i, (title, content) in enumerate(tutorial_sections, 1):
    section_id = f"sec{i}"
    toc += f'<li><a href="#{section_id}">{i}. {title}</a></li>'
    html_sections += f'<h2 id="{section_id}">{i}. {title}</h2>\n'
    html_sections += highlight_code(content)

toc += "</ul>"

html_content = f"""
<html>
<head>
<meta charset="utf-8">
<style>
body {{ font-family: Arial, sans-serif; margin: 40px; }}
h1 {{ color: #2E8B57; }}
h2 {{ color: #3CB371; }}
pre {{ padding: 10px; border-radius: 5px; background-color: #f4f4f4; overflow-x: auto; }}
a {{ text-decoration: none; color: #1E90FF; }}
{HtmlFormatter().get_style_defs('.highlight')}
footer {{ position: fixed; bottom: 0; font-size: 12px; text-align: center; width: 100%; color: gray; }}
</style>
</head>
<body>
<h1>PySpark vs Polars 使用要点与适用场景</h1>
{toc}
{html_sections}
<footer>页码：<span class="page"></span></footer>
</body>
</html>
"""

# --------------------------
# 4. 导出 PDF
# --------------------------
HTML(string=html_content).write_pdf("pyspark_polars_tutorial.pdf", stylesheets=[CSS(string="@page { size: A4; margin: 2cm }")])
print("✅ PDF 已生成：pyspark_polars_tutorial.pdf")
