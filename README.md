*LLM课程期末作业*

# AI智能体协作学习系统

基于AgentScope框架的双智能体协作系统，用于神经网络和深度学习知识的问答与审核。

## 功能特点

- **问题回答者Agent**：负责生成解答、讲解、举例、追问等
- **检查者Agent**：审核答案、纠错、评估学生水平、给反馈等
- 支持从PDF文档中提取知识作为训练素材
- 智能体协作机制，确保答案准确性

## 安装依赖

```bash
pip install -r requirements.txt
```

## 配置

1. 复制 `.env.example` 到 `.env`
2. 在 `.env` 文件中配置你的API密钥：
   - 支持OpenAI API
   - 支持国内大模型API（如通义千问、文心一言等）

## 使用方法(需要输入一个参数——页数，否则只能默认读取前10页内容)

```bash
python main.py 50
```

## 项目结构

- `main.py` - 主程序入口
- `pdf_reader.py` - PDF文本提取模块
- `agents.py` - 智能体定义
- `config.py` - 配置文件
- `data/` - 存放PDF素材

