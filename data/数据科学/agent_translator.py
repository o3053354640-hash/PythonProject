"""
中文-英文翻译智能体 (LangChain + 通义千问)
支持中→英、英→中双向翻译，API 密钥从环境变量读取。

用法:
  交互模式:  python agent_translator.py
  传参翻译:  python agent_translator.py "要翻译的文本"
             python agent_translator.py "Hello world" --direction en2zh
"""
import argparse
import os
import sys
from typing import Literal

from langchain_community.chat_models import ChatTongyi
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# 配置：优先从环境变量读取，避免密钥写死在代码中
MODEL_NAME = os.environ.get("QWEN_MODEL", "qwen-turbo")
DASHSCOPE_API_KEY = os.environ.get("DASHSCOPE_API_KEY", "").strip()

# 翻译方向
Direction = Literal["zh2en", "en2zh"]

SYSTEM_PROMPTS = {
    "zh2en": (
        "你是一位专业的、精确的中文到英文翻译智能体。你的唯一任务是将用户提供的中文文本"
        "完整、准确地翻译成自然流畅的英文。请严格遵守：只返回英文翻译结果，不要包含任何额外解释、注释或原文。"
    ),
    "en2zh": (
        "你是一位专业的、精确的英文到中文翻译智能体。你的唯一任务是将用户提供的英文文本"
        "完整、准确地翻译成自然流畅的中文。请严格遵守：只返回中文翻译结果，不要包含任何额外解释、注释或原文。"
    ),
}


def create_translation_agent(direction: Direction):
    """根据翻译方向创建翻译链。"""
    if not DASHSCOPE_API_KEY:
        raise ValueError("未设置 DASHSCOPE_API_KEY，请在环境变量中配置。")

    llm = ChatTongyi(
        model=MODEL_NAME,
        temperature=0.1,
        dashscope_api_key=DASHSCOPE_API_KEY,
    )

    translation_prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPTS[direction]),
        ("user", "{text}"),
    ])

    return translation_prompt | llm | StrOutputParser()


def translate_once(text: str, direction: Direction) -> str:
    """单次翻译：根据方向和文本返回翻译结果。"""
    if not DASHSCOPE_API_KEY:
        print("🚨 请设置环境变量 DASHSCOPE_API_KEY。", file=sys.stderr)
        sys.exit(1)
    chain = create_translation_agent(direction)
    return chain.invoke({"text": text}).strip()


def run_translator() -> None:
    """运行交互式翻译：先选择方向，再循环输入文本进行翻译。"""
    print("✨ 翻译智能体 (LangChain + 通义千问) ✨")
    print("---------------------------------------------------------")
    print(f"模型: {MODEL_NAME}")

    if not DASHSCOPE_API_KEY:
        print("🚨 请设置环境变量 DASHSCOPE_API_KEY 后再运行。")
        print("   示例 (PowerShell): $env:DASHSCOPE_API_KEY='你的密钥'")
        return

    # 选择翻译方向
    print("\n请选择翻译方向: [1] 中文→英文  [2] 英文→中文")
    choice = input("输入 1 或 2 (默认 1): ").strip() or "1"
    direction: Direction = "en2zh" if choice == "2" else "zh2en"
    dir_label = "英文→中文" if direction == "en2zh" else "中文→英文"

    try:
        chain = create_translation_agent(direction)
    except Exception as e:
        print(f"初始化失败: {e}")
        return

    print(f"\n已启用: {dir_label}。输入 'exit' 退出，'swap' 切换方向。\n")

    while True:
        try:
            prompt = f"\n请输入要翻译的文本 (exit 退出, swap 切换方向):\n> "
            user_input = input(prompt).strip()

            if user_input.lower() == "exit":
                print("再见！")
                break
            if user_input.lower() == "swap":
                direction = "en2zh" if direction == "zh2en" else "zh2en"
                dir_label = "英文→中文" if direction == "en2zh" else "中文→英文"
                chain = create_translation_agent(direction)
                print(f"已切换为: {dir_label}")
                continue
            if not user_input:
                continue

            print("\n🤖 翻译中...")
            result = chain.invoke({"text": user_input})
            print("\n✅ 翻译结果:")
            print("-----------------")
            print(result.strip())
            print("-----------------")

        except KeyboardInterrupt:
            print("\n已中断，再见！")
            break
        except Exception as e:
            print(f"\n错误: {e}")
            # 不因单次错误退出，允许继续输入
            continue


def main() -> None:
    parser = argparse.ArgumentParser(
        description="中文-英文翻译智能体 (LangChain + 通义千问)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python agent_translator.py                     # 交互模式
  python agent_translator.py "你好世界"           # 中文→英文
  python agent_translator.py "Hello" -d en2zh    # 英文→中文
        """,
    )
    parser.add_argument(
        "text",
        nargs="?",
        default=None,
        help="要翻译的文本（不传则进入交互模式）",
    )
    parser.add_argument(
        "-d", "--direction",
        choices=["zh2en", "en2zh"],
        default="zh2en",
        help="翻译方向: zh2en 中→英, en2zh 英→中 (默认 zh2en)",
    )
    args = parser.parse_args()

    if args.text is not None:
        # 传参模式：翻译一次并输出结果后退出
        try:
            result = translate_once(args.text, args.direction)
            print(result)
        except Exception as e:
            print(f"翻译失败: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        # 未传参：交互模式
        run_translator()


if __name__ == "__main__":
    main()
