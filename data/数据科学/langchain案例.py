import os

try:
    from langchain_community.chat_models import ChatTongyi
    from langchain_core.messages import HumanMessage, SystemMessage
except ModuleNotFoundError as exc:
    raise ModuleNotFoundError(
        "未安装 LangChain 依赖。请先执行：\n"
        "  pip install langchain langchain-community\n"
        "如果你已安装过，请确认当前运行的是同一个 Python 环境。"
    ) from exc

# 优先读取环境变量，避免把真实密钥写死到代码里
api_key = (
    os.getenv("DASHSCOPE_API_KEY")
    or os.getenv("TONGYI_API_KEY")
    or os.getenv("QWEN_API_KEY")
)

if not api_key:
    raise RuntimeError(
        "未设置 API Key。请先设置环境变量：DASHSCOPE_API_KEY / TONGYI_API_KEY / QWEN_API_KEY\n"
        "PowerShell 示例：$env:DASHSCOPE_API_KEY='你的key'"
    )

# 初始化 Qwen 聊天模型（默认 qwen-turbo）
chat = ChatTongyi(
    model="qwen-max",  # 可选: qwen-turbo, qwen-plus, qwen-max
    dashscope_api_key=api_key,
    temperature=0.7,
    streaming=False,  # 设为 True 可启用流式输出
)

messages = [
    SystemMessage(content="你是一个专业的 Python 教练。"),
    HumanMessage(content="如何用 Python 读取一个 JSON 文件？"),
]

# 调用模型
response = chat.invoke(messages)
print("🤖 回答：", response.content)
