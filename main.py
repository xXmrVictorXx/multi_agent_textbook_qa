"""主程序 - AI智能体协作学习系统"""
import agentscope
from agentscope.message import Msg
from config import Config
from pdf_reader import load_pdf_knowledge
from agents import create_agents
import sys


class CollaborativeLearningSystem:
    """协作学习系统"""
    
    def __init__(self, max_pages: int = None):
        """
        初始化系统
        
        Args:
            max_pages: PDF最大提取页数
        """
        self.knowledge_base = ""
        self.answerer = None
        self.checker = None
        self.max_pages = max_pages or Config.DEFAULT_MAX_PAGES
        self.conversation_history = []
        
    def initialize(self):
        """初始化系统"""
        print("=" * 60)
        print("AI智能体协作学习系统")
        print("=" * 60)
        
        # 1. 验证配置
        print("\n[1/4] 验证配置...")
        if not Config.validate():
            print("\n请按以下步骤配置：")
            print("1. 创建 .env 文件")
            print("2. 添加以下内容：")
            print("   OPENAI_API_KEY=your_api_key_here")
            print("   MODEL_NAME=gpt-3.5-turbo")
            print("\n或者如果你使用其他模型，请相应配置。")
            
            # 尝试使用默认配置继续
            print("\n尝试使用默认配置继续...")
        
        # 2. 初始化AgentScope
        print("\n[2/4] 初始化AgentScope...")
        try:
            agentscope.init(
                model_configs=[
                    {
                        "model_type": "openai_chat",
                        "config_name": "my_model",
                        "model_name": Config.MODEL_NAME,
                        "api_key": Config.OPENAI_API_KEY,
                        "organization": None,
                        "client_args": {
                            "base_url": Config.OPENAI_BASE_URL,
                        }
                    }
                ]
            )
            print("AgentScope初始化成功！")
        except Exception as e:
            print(f"AgentScope初始化失败: {e}")
            print("\n如果你使用的是其他API（如通义千问），请修改config.py中的配置。")
            sys.exit(1)
        
        # 3. 加载知识库
        print(f"\n[3/4] 加载知识库（前{self.max_pages}页）...")
        try:
            self.knowledge_base = load_pdf_knowledge(
                Config.PDF_PATH, 
                max_pages=self.max_pages
            )
            print(f"知识库加载成功！字符数: {len(self.knowledge_base)}")
        except Exception as e:
            print(f"加载知识库失败: {e}")
            print("将在没有知识库的情况下运行...")
            self.knowledge_base = ""
        
        # 4. 创建智能体
        print("\n[4/4] 创建智能体...")
        try:
            self.answerer, self.checker = create_agents(
                self.knowledge_base,
                model_config=None
            )
            print(f"✓ {Config.ANSWERER_NAME} 已创建")
            print(f"✓ {Config.CHECKER_NAME} 已创建")
        except Exception as e:
            print(f"创建智能体失败: {e}")
            sys.exit(1)
        
        print("\n" + "=" * 60)
        print("系统初始化完成！")
        print("=" * 60)
    
    def process_question(self, question: str) -> dict:
        """
        处理问题（协作流程）
        
        Args:
            question: 用户问题
            
        Returns:
            包含答案和审核结果的字典
        """
        print("\n" + "-" * 60)
        print(f"问题: {question}")
        print("-" * 60)
        
        # 第一步：问题回答者回答问题
        print(f"\n[{Config.ANSWERER_NAME}] 正在思考...")
        question_msg = Msg(name="user", content=question, role="user")
        answer_msg = self.answerer.reply(question_msg)
        
        # 处理返回值（可能是Msg对象或字符串）
        if isinstance(answer_msg, Msg):
            answer_content = answer_msg.content
        else:
            answer_content = str(answer_msg)
        
        print(f"\n[{Config.ANSWERER_NAME}] 回答：")
        print(answer_content)
        
        # 第二步：检查者审核答案
        print(f"\n[{Config.CHECKER_NAME}] 正在审核...")
        check_msg = self.checker.check_answer(question, answer_content)
        
        # 处理返回值（可能是Msg对象或字符串）
        if isinstance(check_msg, Msg):
            check_content = check_msg.content
        else:
            check_content = str(check_msg)
        
        print(f"\n[{Config.CHECKER_NAME}] 审核结果：")
        print(check_content)
        
        # 保存对话历史
        result = {
            "question": question,
            "answer": answer_content,
            "check": check_content
        }
        self.conversation_history.append(result)
        
        return result
    
    def run_interactive(self):
        """运行交互式会话"""
        print("\n\n" + "=" * 60)
        print("开始交互式会话")
        print("=" * 60)
        print("\n提示:")
        print("- 输入你的问题，智能体将协作为你解答")
        print("- 输入 'quit' 或 'exit' 退出程序")
        print("- 输入 'history' 查看对话历史")
        print("- 输入 'pages:N' 重新加载前N页知识库")
        print()
        
        while True:
            try:
                # 获取用户输入
                user_input = input("\n请输入你的问题: ").strip()
                
                if not user_input:
                    continue
                
                # 处理特殊命令
                if user_input.lower() in ['quit', 'exit', '退出']:
                    print("\n感谢使用！再见！")
                    break
                
                if user_input.lower() == 'history':
                    self.show_history()
                    continue
                
                if user_input.lower().startswith('pages:'):
                    try:
                        pages = int(user_input.split(':')[1])
                        self.reload_knowledge(pages)
                    except:
                        print("格式错误，请使用 pages:N 的格式，例如 pages:20")
                    continue
                
                # 处理问题
                self.process_question(user_input)
                
            except KeyboardInterrupt:
                print("\n\n程序被中断，退出...")
                break
            except Exception as e:
                print(f"\n错误: {e}")
                import traceback
                traceback.print_exc()
    
    def show_history(self):
        """显示对话历史"""
        if not self.conversation_history:
            print("\n暂无对话历史")
            return
        
        print("\n" + "=" * 60)
        print("对话历史")
        print("=" * 60)
        
        for i, item in enumerate(self.conversation_history, 1):
            print(f"\n[对话 {i}]")
            print(f"问题: {item['question']}")
            print(f"\n回答: {item['answer'][:200]}...")
            print(f"\n审核: {item['check'][:200]}...")
            print("-" * 60)
    
    def reload_knowledge(self, max_pages: int):
        """
        重新加载知识库
        
        Args:
            max_pages: 最大页数
        """
        print(f"\n正在重新加载知识库（前{max_pages}页）...")
        try:
            self.knowledge_base = load_pdf_knowledge(
                Config.PDF_PATH, 
                max_pages=max_pages
            )
            self.max_pages = max_pages
            
            # 重新创建智能体
            self.answerer, self.checker = create_agents(
                self.knowledge_base,
                model_config=None
            )
            print(f"知识库重新加载成功！字符数: {len(self.knowledge_base)}")
        except Exception as e:
            print(f"重新加载知识库失败: {e}")


def main():
    """主函数"""
    # 解析命令行参数
    max_pages = Config.DEFAULT_MAX_PAGES
    if len(sys.argv) > 1:
        try:
            max_pages = int(sys.argv[1])
        except:
            print(f"使用默认页数: {max_pages}")
    
    # 创建系统实例
    system = CollaborativeLearningSystem(max_pages=max_pages)
    
    # 初始化系统
    system.initialize()
    
    # 运行交互式会话
    system.run_interactive()


if __name__ == "__main__":
    main()
