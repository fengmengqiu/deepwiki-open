# DeepWiki 源码运行指南

本指南将帮助你从源码运行 DeepWiki 项目。

## ✅ 前置条件

已安装以下软件：
- ✅ Python 3.12.3 (已检测到)
- ✅ Node.js v22.17.0 (已检测到)
- ✅ npm 10.9.2 (已检测到)
- ✅ uv (Python 包管理器，已检测到)

## 📦 依赖安装

### ✅ 后端依赖 (已完成)

后端使用 Python 和 FastAPI，依赖已通过 uv 安装完成：

```bash
# 后端依赖已安装在虚拟环境中
# 虚拟环境位置: /home/fmq/develop/deepwiki-open/.venv
```

**安装的主要依赖包括：**
- FastAPI (Web 框架)
- uvicorn (ASGI 服务器)
- adalflow (RAG 框架)
- faiss-cpu (向量数据库)
- google-generativeai (Google Gemini)
- openai (OpenAI API)
- tiktoken (Token 计数)
- pydantic, numpy, requests 等

### ✅ 前端依赖 (已完成)

前端使用 Next.js 15 和 React 19，依赖已通过 npm 安装完成：

```bash
# 前端依赖已安装
# 共安装 631 个包
```

**安装的主要依赖包括：**
- Next.js 15.3.1 (React 框架)
- React 19.0.0 (UI 库)
- TypeScript (类型系统)
- Tailwind CSS (样式框架)
- Mermaid (图表渲染)
- react-markdown (Markdown 渲染)
- next-intl (国际化)

## 🔑 配置 API Keys

### 步骤 1: 创建 .env 文件

```bash
# 复制模板文件
cp .env.example .env
```

### 步骤 2: 编辑 .env 文件并填入你的 API Keys

**最小配置 (至少需要以下之一)：**

#### 选项 A: 使用 Google Gemini (推荐)
```bash
# 在 .env 文件中设置
GOOGLE_API_KEY=你的_Google_API_密钥
DEEPWIKI_EMBEDDER_TYPE=google
```

获取 Google API Key: https://makersuite.google.com/app/apikey

#### 选项 B: 使用 OpenAI
```bash
# 在 .env 文件中设置
OPENAI_API_KEY=你的_OpenAI_API_密钥
DEEPWIKI_EMBEDDER_TYPE=openai
```

获取 OpenAI API Key: https://platform.openai.com/api-keys

#### 选项 C: 使用本地 Ollama (无需 API Key)
```bash
# 在 .env 文件中设置
DEEPWIKI_EMBEDDER_TYPE=ollama
OLLAMA_HOST=http://localhost:11434
```

首先需要安装并运行 Ollama: https://ollama.ai

### 可选配置

查看 `.env.example` 文件了解所有可用的配置选项，包括：
- OpenRouter (访问多种模型)
- Azure OpenAI
- AWS Bedrock
- 自定义 OpenAI 端点
- 日志配置
- 身份验证

## 🚀 运行项目

### 方法 1: 分别启动后端和前端 (推荐开发使用)

**终端 1 - 启动后端 API:**

```bash
# 激活虚拟环境并启动 API 服务器
source .venv/bin/activate
python -m api.main

# 后端将运行在 http://localhost:8001
```

**终端 2 - 启动前端:**

```bash
# 在新终端中启动前端开发服务器
npm run dev

# 前端将运行在 http://localhost:3000
```

### 方法 2: 使用 Docker Compose (推荐生产使用)

```bash
# 确保 .env 文件已配置
docker-compose up

# 访问 http://localhost:3000
```

## 📝 使用 DeepWiki

1. 打开浏览器访问 http://localhost:3000
2. 输入 GitHub/GitLab/BitBucket 仓库 URL
3. (可选) 配置模型和过滤规则
4. 点击 "Generate Wiki" 开始生成文档
5. 等待 AI 分析代码并生成交互式 Wiki

### 支持的仓库类型

- GitHub: `https://github.com/owner/repo`
- GitLab: `https://gitlab.com/owner/repo`
- BitBucket: `https://bitbucket.org/owner/repo`

### 私有仓库

如需访问私有仓库，点击 "+ Add access tokens" 并输入：
- GitHub: Personal Access Token (需要 `repo` 权限)
- GitLab: Personal Access Token
- BitBucket: App Password

## 🧪 运行测试

```bash
# 激活虚拟环境
source .venv/bin/activate

# 运行所有测试
pytest

# 运行特定类型的测试
pytest -m unit          # 单元测试
pytest -m integration   # 集成测试
pytest -m network       # 需要网络的测试

# 使用测试运行器脚本
python tests/run_tests.py              # 所有测试
python tests/run_tests.py --unit       # 单元测试
python tests/run_tests.py --integration # 集成测试
python tests/run_tests.py --api        # API 测试

# 查看测试覆盖率
pytest --cov=api --cov-report=html
```

## 🔍 验证安装

### 检查后端

```bash
# 激活虚拟环境
source .venv/bin/activate

# 检查 Python 版本和位置
python --version
which python

# 测试导入主要模块
python -c "import fastapi; import adalflow; import google.generativeai; print('✅ 后端依赖正常')"
```

### 检查前端

```bash
# 检查 Node.js 版本
node --version

# 检查已安装的包
npm list --depth=0

# 验证 TypeScript
npx tsc --version
```

### 检查 API 服务器

```bash
# 启动后端后，在新终端运行：
curl http://localhost:8001

# 应该返回 API 信息
```

## 🐛 常见问题

### 问题 1: Python 模块未找到

**解决方案：** 确保激活了虚拟环境

```bash
source .venv/bin/activate
```

### 问题 2: 端口已被占用

**解决方案：** 修改 .env 文件中的端口

```bash
# 后端端口
PORT=8002

# 同时需要更新前端连接地址
SERVER_BASE_URL=http://localhost:8002
```

### 问题 3: API Key 无效

**解决方案：**
1. 检查 .env 文件是否在项目根目录
2. 确认 API Key 没有额外的空格或引号
3. 验证 API Key 是否有效且有足够配额

### 问题 4: 前端无法连接后端

**解决方案：**
1. 确认后端正在运行 (http://localhost:8001)
2. 检查 CORS 配置
3. 查看浏览器控制台错误信息

### 问题 5: Ollama 连接失败

**解决方案：**
1. 确认 Ollama 服务正在运行: `ollama serve`
2. 检查 OLLAMA_HOST 配置
3. 拉取所需模型: `ollama pull llama3`

## 📂 重要目录

- `api/` - Python 后端代码
- `src/` - Next.js 前端代码
- `.venv/` - Python 虚拟环境
- `node_modules/` - Node.js 依赖
- `api/config/` - 配置文件 (generator.json, embedder.json, repo.json)
- `tests/` - 测试代码
- `~/.adalflow/` - 数据存储目录
  - `repos/` - 克隆的仓库
  - `databases/` - FAISS 向量数据库
  - `wikicache/` - 生成的 Wiki 缓存

## 🔧 开发工具

### 后端开发

```bash
# 激活虚拟环境
source .venv/bin/activate

# 启动开发服务器 (自动重载)
python -m api.main

# 运行代码格式化
black api/

# 运行类型检查
mypy api/
```

### 前端开发

```bash
# 启动开发服务器 (Turbopack，快速热重载)
npm run dev

# 构建生产版本
npm run build

# 运行 ESLint
npm run lint

# 启动生产服务器
npm start
```

## 📚 更多信息

- 完整文档: [README.md](README.md)
- API 文档: [api/README.md](api/README.md)
- 架构说明: [CLAUDE.md](CLAUDE.md)
- 测试指南: [tests/README.md](tests/README.md)
- Ollama 使用: [Ollama-instruction.md](Ollama-instruction.md)

## 🆘 获取帮助

- GitHub Issues: https://github.com/AsyncFuncAI/deepwiki-open/issues
- Discord: https://discord.com/invite/VQMBGR8u5v
- Twitter/X: [@sashimikun_void](https://x.com/sashimikun_void)

---

**祝你使用愉快！** 🎉

如有问题，请查看日志文件: `api/logs/application.log`
