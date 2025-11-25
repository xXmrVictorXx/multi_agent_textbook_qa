"""配置文件"""
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

"""

Sample configuration in Dict form:
{
  "model_name":"qwen2.5:72b",
  "config_name": "qwen",
  "model_type": "openai_chat",
  "api_key": "<api_key>",
  "client_args": {
    "base_url": "<base_url>"
  },
  "generate_args": {
      "temperature": 0.5,
      "stream": true,
  }
}

"""



class Config:
    """系统配置"""
    
    # API配置
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1")
    MODEL_NAME = os.getenv("MODEL_NAME", "qwen3-max")
    
    # PDF路径配置
    PDF_PATH = "data/nndl-book.pdf"
    
    # 默认提取的PDF页数（用于测试）
    DEFAULT_MAX_PAGES = 10  # 初始测试使用较少页面
    
    # Agent配置
    ANSWERER_NAME = "问题回答者"
    CHECKER_NAME = "检查者"
    
    # 系统提示词
    ANSWERER_SYSTEM_PROMPT = """你是一位专业的神经网络和深度学习教师助手。你的任务是：
1. 准确、清晰地回答学生提出的问题
2. 提供详细的讲解和说明
3. 给出相关的例子帮助理解
4. 必要时进行追问以确认学生的理解程度

你的回答应该：
- 基于提供的教材知识
- 准确无误
- 清晰易懂
- 循序渐进
- 富有耐心

如果问题超出了你的知识范围，请诚实地说明。
"""

    CHECKER_SYSTEM_PROMPT = """你是一位严谨的教学质量审核专家。你的任务是：
1. 审核问题回答者给出的答案是否准确
2. 检查答案中是否存在错误或不准确的地方
3. 评估答案的质量和完整性
4. 评估学生可能的理解水平
5. 提供改进建议和补充说明

你的审核应该：
- 专业严谨
- 指出具体的错误或问题
- 提供建设性的反馈
- 考虑学生的学习效果

请以客观、专业的态度进行审核。
"""

    @classmethod
    def validate(cls):
        """验证配置是否完整"""
        if not cls.OPENAI_API_KEY or not cls.OPENAI_API_KEY.strip():
            print("警告: 未配置API密钥，请创建.env文件并配置API密钥")
            print("你可以配置 OPENAI_API_KEY")
            return False
        return True


if __name__ == "__main__":
    Config.validate()
    print(f"模型名称: {Config.MODEL_NAME}")
    print(f"PDF路径: {Config.PDF_PATH}")

