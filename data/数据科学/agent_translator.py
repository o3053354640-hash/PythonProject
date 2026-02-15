import os
from langchain_community.chat_models import ChatTongyi
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

MODEL_NAME = "qwen-turbo"
DASHSCOPE_API_KEY = "sk-576bbbbd188340069daeed2ac9208640"  # 替换为你的真实密钥


def create_translation_agent():
    llm = ChatTongyi(
        model=MODEL_NAME,
        temperature=0.1,
        dashscope_api_key=DASHSCOPE_API_KEY
    )

    translation_prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "你是一位专业的、精确的中文到英文翻译智能体。你的唯一任务是将用户提供的中文文本"
            "完整、准确地翻译成自然流畅的英文。请严格遵守：只返回英文翻译结果，不要包含任何额外解释、注释或原文。"
        ),
        ("user", "{text}"),
    ])

    translation_chain = translation_prompt | llm | StrOutputParser()
    return translation_chain


def run_translator():
    print("✨ 中文-英文翻译智能体 (基于 LangChain + Qwen) ✨")
    print("---------------------------------------------------------")
    print(f"使用的模型: {MODEL_NAME}")

    if not DASHSCOPE_API_KEY or DASHSCOPE_API_KEY == "sk-your-real-api-key-here":
        print("🚨 请在代码中设置有效的 DASHSCOPE_API_KEY！")
        return

    try:
        translator_chain = create_translation_agent()
    except Exception as e:
        print(f"初始化模型失败: {e}")
        return

    while True:
        try:
            chinese_text = input("\n请输入要翻译的中文文本 (输入 'exit' 退出): \n&gt; ")
            if chinese_text.lower() == 'exit':
                print("程序退出。再见！")
                break
            if not chinese_text.strip():
                continue

            print("\n🤖 正在翻译...")
            english_translation = translator_chain.invoke({"text": chinese_text})

            print("\n✅ 英文翻译结果:")
            print("-----------------")
            print(english_translation.strip())
            print("-----------------")

        except KeyboardInterrupt:
            print("\n程序中断退出。再见！")
            break
        except Exception as e:
            print(f"\n运行时发生错误: {e}")
            break


if __name__ == "__main__":
    run_translator()