"""智能体定义模块"""
import agentscope
from agentscope.agents import DialogAgent
from agentscope.message import Msg
from typing import List, Dict, Any
from config import Config


class AnswererAgent(DialogAgent):
    """问题回答者智能体
    
    负责：
    1. 生成准确的解答
    2. 提供详细的讲解
    3. 举例说明
    4. 适当追问
    """
    
    def __init__(self, name: str, knowledge_base: str = "", **kwargs):
        """
        初始化问题回答者
        
        Args:
            name: 智能体名称
            knowledge_base: 知识库内容
            **kwargs: 其他参数
        """
        super().__init__(
            name=name,
            sys_prompt=self._build_system_prompt(knowledge_base),
            **kwargs
        )
        self.knowledge_base = knowledge_base
    
    def _build_system_prompt(self, knowledge_base: str) -> str:
        """构建系统提示词"""
        prompt = Config.ANSWERER_SYSTEM_PROMPT
        
        if knowledge_base:
            prompt += f"\n\n以下是你可以参考的教材知识：\n{knowledge_base[:8000]}\n"
        
        return prompt
    
    def reply(self, x: Msg = None) -> Msg:
        """
        回复消息
        
        Args:
            x: 输入消息
            
        Returns:
            回复消息
        """
        return super().reply(x)


class CheckerAgent(DialogAgent):
    """检查者智能体
    
    负责：
    1. 审核答案的准确性
    2. 纠错
    3. 评估学生水平
    4. 提供反馈
    """
    
    def __init__(self, name: str, knowledge_base: str = "", **kwargs):
        """
        初始化检查者
        
        Args:
            name: 智能体名称
            knowledge_base: 知识库内容
            **kwargs: 其他参数
        """
        super().__init__(
            name=name,
            sys_prompt=self._build_system_prompt(knowledge_base),
            **kwargs
        )
        self.knowledge_base = knowledge_base
    
    def _build_system_prompt(self, knowledge_base: str) -> str:
        """构建系统提示词"""
        prompt = Config.CHECKER_SYSTEM_PROMPT
        
        if knowledge_base:
            prompt += f"\n\n以下是参考教材知识，用于验证答案的准确性：\n{knowledge_base[:8000]}\n"
        
        return prompt
    
    def check_answer(self, question: str, answer: str) -> Msg:
        """
        检查答案
        
        Args:
            question: 原始问题
            answer: 回答者的答案
            
        Returns:
            审核结果消息
        """
        check_prompt = f"""请审核以下问答：

问题：{question}

回答：{answer}

请从以下几个方面进行审核：
1. 答案的准确性（是否有错误）
2. 答案的完整性（是否遗漏重要内容）
3. 答案的清晰度（是否易于理解）
4. 给出审核结论：通过/需要改进/不通过
5. 如果需要改进，请具体说明如何改进

请给出你的审核结果：
"""
        
        msg = Msg(name="user", content=check_prompt, role="user")
        return self.reply(msg)


def create_agents(knowledge_base: str, model_config: Dict[str, Any]) -> tuple:
    """
    创建智能体
    
    Args:
        knowledge_base: 知识库内容
        model_config: 模型配置
        
    Returns:
        (answerer_agent, checker_agent) 智能体元组
    """
    # 创建问题回答者
    answerer = AnswererAgent(
        name=Config.ANSWERER_NAME,
        knowledge_base=knowledge_base,
        model_config_name="my_model"
    )
    
    # 创建检查者
    checker = CheckerAgent(
        name=Config.CHECKER_NAME,
        knowledge_base=knowledge_base,
        model_config_name="my_model"
    )
    
    return answerer, checker


if __name__ == "__main__":
    # 测试智能体创建
    print("智能体模块加载成功")
    print(f"问题回答者: {Config.ANSWERER_NAME}")
    print(f"检查者: {Config.CHECKER_NAME}")
