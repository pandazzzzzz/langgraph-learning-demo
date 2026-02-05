# 快速开始指南

欢迎来到LangGraph学习之旅！本指南将帮助你快速搭建开发环境并运行第一个LangGraph应用。

## 📋 前置要求

在开始之前，请确保你的系统满足以下要求：

- **Python 3.9+** - 推荐使用Python 3.10或更高版本
- **Git** - 用于版本控制
- **文本编辑器** - 推荐VS Code、PyCharm或其他支持Python的IDE
- **OpenAI API账户** - 用于访问GPT模型（必需）

## 🛠️ 环境搭建

### 1. 克隆项目

```bash
git clone <your-repo-url>
cd langgraph-learning-demo
```

### 2. 创建虚拟环境

```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境
# Windows
venv\Scripts\activate

# macOS/Linux
source venv/bin/activate
```

### 3. 安装依赖

```bash
# 安装基础依赖
pip install -r requirements.txt

# 或者使用开发模式安装（推荐）
pip install -e ".[dev,jupyter]"
```

### 4. 配置环境变量

```bash
# 复制环境变量模板
cp .env.example .env

# 编辑.env文件，添加你的API密钥
# 至少需要配置OPENAI_API_KEY
```

在`.env`文件中添加：
```env
OPENAI_API_KEY=your_openai_api_key_here
```

### 5. 验证安装

```bash
# 运行环境验证脚本
python -c "
from src.core.utils import validate_environment, print_validation_summary
results = validate_environment()
print_validation_summary(results)
"
```

## 🚀 运行第一个示例

### 基础聊天机器人

```bash
# 运行基础聊天机器人示例
python src/examples/basic_chatbot.py
```

这个示例将展示：
- 如何创建简单的状态图
- 如何定义节点和边
- 如何管理对话状态
- 基础的LLM集成

### 预期输出

```
🚀 Starting LangGraph Basic Chatbot Example

📊 Graph Structure Analysis
==============================
Nodes in the graph:
  • chatbot

Edges in the graph:
  • chatbot → __end__

Entry points:
  • Input schema: <class 'dict'>

🤖 LangGraph Basic Chatbot Demo
========================================
Type 'quit' to exit the conversation
========================================

👤 You: Hello!
🤖 Bot: Hello! How can I help you today?
```

## 📚 学习路径

### 🎯 第一周：基础概念
1. **理解LangGraph核心概念**
   - 状态图（StateGraph）
   - 节点（Nodes）
   - 边（Edges）
   - 状态管理

2. **完成基础练习**
   - 修改聊天机器人的响应风格
   - 添加简单的条件逻辑
   - 实现基础的对话历史管理

### 🔧 第二周：工具集成
1. **学习工具绑定**
   - 外部API调用
   - 函数工具集成
   - 错误处理

2. **实践项目**
   - 构建天气查询机器人
   - 集成计算器功能
   - 添加网络搜索能力

### 🏗️ 第三周：RAG系统
1. **构建检索系统**
   - 向量数据库集成
   - 文档处理和索引
   - 相似性搜索

2. **实现生成增强**
   - 上下文检索
   - 答案生成
   - 质量评估

### 🤝 第四周：多智能体
1. **多智能体协作**
   - 智能体通信
   - 任务分工
   - 结果聚合

2. **高级项目**
   - 客服系统
   - 研究助手
   - 内容生成器

## 🧪 运行测试

```bash
# 运行所有测试
pytest

# 运行特定模块测试
pytest tests/unit/test_basic_chatbot.py -v

# 运行属性测试
pytest tests/property/ --hypothesis-show-statistics

# 生成测试覆盖率报告
pytest --cov=src --cov-report=html
```

## 📖 文档结构

```
docs/
├── getting-started.md      # 本文档
├── tutorials/              # 详细教程
│   ├── module01-basics.md
│   ├── module02-state.md
│   ├── module03-tools.md
│   ├── module04-rag.md
│   ├── module05-multi.md
│   └── module06-advanced.md
└── api-reference/          # API参考文档
    ├── core.md
    ├── modules.md
    └── examples.md
```

## 🔧 开发工具配置

### VS Code配置

创建`.vscode/settings.json`：
```json
{
    "python.defaultInterpreterPath": "./venv/bin/python",
    "python.linting.enabled": true,
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "black",
    "python.testing.pytestEnabled": true,
    "python.testing.pytestArgs": ["tests"]
}
```

### 代码格式化

```bash
# 格式化代码
black src/ tests/

# 排序导入
isort src/ tests/

# 检查代码质量
flake8 src/ tests/

# 类型检查
mypy src/
```

## ❓ 常见问题

### Q: 安装依赖时出现错误怎么办？

A: 尝试以下解决方案：
```bash
# 升级pip
pip install --upgrade pip

# 清理缓存
pip cache purge

# 重新安装
pip install -r requirements.txt --no-cache-dir
```

### Q: OpenAI API调用失败？

A: 检查以下几点：
1. API密钥是否正确配置
2. 账户是否有足够的余额
3. 网络连接是否正常
4. 是否设置了正确的代理（如果需要）

### Q: 如何切换到其他LLM提供商？

A: 修改示例代码中的LLM初始化：
```python
# 使用Anthropic Claude
from langchain_anthropic import ChatAnthropic
llm = ChatAnthropic(model="claude-3-sonnet-20240229")

# 使用本地Ollama
from langchain_community.llms import Ollama
llm = Ollama(model="llama2")
```

## 🎯 下一步

恭喜！你已经成功搭建了LangGraph学习环境。现在可以：

1. **深入学习Module 01** - 查看`docs/tutorials/module01-basics.md`
2. **完成练习题** - 查看`exercises/module01/`目录
3. **参与社区讨论** - 访问项目的GitHub Discussions
4. **贡献代码** - 提交你的改进和新功能

准备好开始你的LangGraph学习之旅了吗？让我们开始吧！🚀