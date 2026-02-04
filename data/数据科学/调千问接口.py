import dashscope
from dashscope import Generation

# 设置 API Key（建议用环境变量）
dashscope.api_key = "sk-576bbbbd188340069daeed2ac9208640"  # 替换为你的 DashScope API Key

# 调用通义千问（例如 qwen-max 模型）
response = Generation.call(
    model="qwen-max",  # 可选: qwen-turbo, qwen-plus, qwen-max, qwen-3 等
    messages=[
        {"role": "system", "content": "你是一个乐于助人的助手。"},
        {"role": "user", "content": "请用中文介绍一下你自己。"}
    ]
)

# 打印结果
if response.status_code == 200:
    print(response.output.text)
else:
    print("请求失败:", response.code, response.message)