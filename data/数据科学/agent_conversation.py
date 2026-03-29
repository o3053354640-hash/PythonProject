import sys
import os

# Fix encoding for Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
else:
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

os.environ['PYTHONIOENCODING'] = 'utf-8'

# LangChain imports
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain

# Get API key from environment variable
DASHSCOPE_API_KEY = os.environ.get("DASHSCOPE_API_KEY", "").strip()
if not DASHSCOPE_API_KEY:
    print("🚨 错误: 未设置环境变量 DASHSCOPE_API_KEY")
    print("   请设置环境变量后再运行，示例 (PowerShell): $env:DASHSCOPE_API_KEY='你的密钥'")
    sys.exit(1)

# Initialize model with API key from environment
llm = ChatTongyi(
    model="qwen-turbo",  # Use cheaper model for testing
    dashscope_api_key=DASHSCOPE_API_KEY,
    temperature=0.7,
    streaming=False  # Disable streaming for simple testing
)

# Initialize memory and chain
memory = ConversationBufferMemory()
chain = ConversationChain(llm=llm, memory=memory, verbose=False)

print("=== Starting English Conversation Test ===")
print("=" * 40)

# Test 1: Simple introduction
response1 = chain.invoke({"input": "Hello, please introduce yourself briefly."})
print("Q1: Hello, please introduce yourself briefly.")
print(f"A1: {response1['response']}\n")

# Test 2: Follow-up question with memory
response2 = chain.invoke({"input": "What was my first question to you?"})
print("Q2: What was my first question to you?")
print(f"A2: {response2['response']}\n")

# Test 3: Another follow-up
response3 = chain.invoke({"input": "Can you summarize our conversation so far?"})
print("Q3: Can you summarize our conversation so far?")
print(f"A3: {response3['response']}\n")

# Test 4: Knowledge question
response4 = chain.invoke({"input": "What is LangChain and what is it used for?"})
print("Q4: What is LangChain and what is it used for?")
print(f"A4: {response4['response']}\n")

print("=" * 40)
print("✅ Test completed successfully!")