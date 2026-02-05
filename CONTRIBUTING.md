# 贡献指南

感谢你对LangGraph学习项目的关注！我们欢迎各种形式的贡献，包括代码、文档、示例、测试用例和反馈建议。

## 🤝 如何贡献

### 报告问题
- 使用GitHub Issues报告bug或提出功能请求
- 提供详细的问题描述和复现步骤
- 包含相关的错误信息和环境信息

### 提交代码
1. Fork本项目
2. 创建特性分支 (`git checkout -b feature/amazing-feature`)
3. 提交更改 (`git commit -m 'Add amazing feature'`)
4. 推送到分支 (`git push origin feature/amazing-feature`)
5. 创建Pull Request

### 改进文档
- 修正错别字和语法错误
- 添加缺失的文档
- 改进现有文档的清晰度
- 翻译文档到其他语言

### 添加示例
- 创建新的学习示例
- 改进现有示例的质量
- 添加更多实际应用场景

## 📋 开发规范

### 代码风格
- 使用Black进行代码格式化
- 遵循PEP 8编码规范
- 使用有意义的变量和函数名
- 添加适当的类型注解

### 测试要求
- 为新功能添加单元测试
- 确保所有测试通过
- 保持测试覆盖率在80%以上
- 添加属性测试验证通用性质

### 文档要求
- 为新功能添加文档字符串
- 更新相关的README文件
- 添加使用示例
- 保持文档与代码同步

## 🧪 开发环境设置

```bash
# 克隆你的fork
git clone https://github.com/your-username/langgraph-learning-demo.git
cd langgraph-learning-demo

# 设置开发环境
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 安装开发依赖
pip install -e ".[dev,jupyter]"

# 安装pre-commit钩子
pre-commit install
```

## 🔍 代码质量检查

在提交代码前，请运行以下检查：

```bash
# 代码格式化
black src/ tests/ exercises/
isort src/ tests/ exercises/

# 代码质量检查
flake8 src/ tests/ exercises/
mypy src/

# 运行测试
pytest tests/ -v --cov=src

# 运行属性测试
pytest tests/property/ --hypothesis-show-statistics
```

## 📝 提交信息规范

使用清晰、描述性的提交信息：

```
类型(范围): 简短描述

详细描述（可选）

- 相关问题: #123
- 破坏性变更: 描述任何破坏性变更
```

类型包括：
- `feat`: 新功能
- `fix`: 错误修复
- `docs`: 文档更新
- `style`: 代码格式化
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

## 🏷️ Pull Request指南

### PR标题
使用清晰、描述性的标题，格式与提交信息类似。

### PR描述
包含以下信息：
- 变更的简要描述
- 相关的issue编号
- 测试说明
- 破坏性变更（如有）
- 截图或演示（如适用）

### PR检查清单
- [ ] 代码遵循项目的编码规范
- [ ] 添加了适当的测试
- [ ] 所有测试通过
- [ ] 更新了相关文档
- [ ] 提交信息清晰明确

## 🎯 贡献类型

### 🐛 Bug修复
- 修复现有功能的错误
- 改进错误处理
- 修正文档中的错误

### ✨ 新功能
- 添加新的学习模块
- 实现新的示例项目
- 增加工具集成

### 📚 文档改进
- 改进现有文档
- 添加新的教程
- 翻译文档

### 🧪 测试增强
- 添加缺失的测试
- 改进测试覆盖率
- 添加性能测试

### 🎨 用户体验
- 改进代码示例
- 优化学习路径
- 增强交互性

## 🌟 认可贡献者

我们会在以下地方认可贡献者：
- README.md中的贡献者列表
- 发布说明中的感谢
- 项目网站的贡献者页面

## 📞 获取帮助

如果你需要帮助或有疑问：

1. **查看现有文档** - 先查看README和文档
2. **搜索现有issues** - 可能已有相关讨论
3. **创建新issue** - 描述你的问题或想法
4. **参与讨论** - 在GitHub Discussions中交流

## 🎉 感谢

感谢每一位贡献者的努力！正是因为有了你们的参与，这个项目才能不断改进，帮助更多人学习LangGraph。

特别感谢：
- 提供反馈和建议的用户
- 报告bug的测试者
- 改进文档的编辑者
- 贡献代码的开发者

让我们一起构建更好的LangGraph学习体验！🚀