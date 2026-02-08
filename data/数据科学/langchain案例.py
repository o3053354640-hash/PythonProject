import os
from langchain_community.chat_models import ChatTongyi
from langchain.schema.messages import HumanMessage, SystemMessage  # 注意路径可能需要调整
# 确保已在环境中设置 API_KEY 或直接替换下面的 None 为你的 api_key 字符串
api_key = os.getenv("TONGYI_API_KEY") or "sk-576bbbbd188340069daeed2ac9208640"
# 初始化 Qwen 聊天模型（默认 qwen-turbo）
chat = ChatTongyi(
    api_key=api_key,
    model="qwen-max",        # 可选: qwen-turbo, qwen-plus, qwen-max
    temperature=0.7,
    streaming=False          # 设为 True 可启用流式输出

messages = [
    SystemMessage(content="你是一个专业的 Python 教练。"),
    HumanMessage(content="如何用 Python 读取一个 JSON 文件？")
]
# 调用模型
response = chat.invoke(messages)
print("🤖 回答：", response.content))
