# LiteLLM 集成文档

本文档说明如何使用公司内部部署的 LiteLLM 服务来运行 DeepWiki。

## 概述

LiteLLM 是一个统一的 LLM 代理服务，提供对多种 AI 模型的访问。公司内部部署的 LiteLLM 服务已集成到 DeepWiki 中，作为默认的模型提供商。

## 配置信息

### 公司内部 LiteLLM 配置

```bash
# API 密钥
LITELLM_API_KEY=sk-wDF58hGeRVZPZwSo_g04FQ

# API 基础 URL
LITELLM_BASE_URL=https://litellm-internal.123u.com/

# 默认模型
DEFAULT_AI_MODEL=claude-haiku-4-5

# 大上下文模型（用于需要更多上下文的场景）
LARGE_CONTEXT_MODEL=claude-sonnet-4-5
```

## 支持的模型

LiteLLM 提供商当前配置了以下模型：

1. **claude-haiku-4-5** (默认)
   - 快速响应
   - 适合大多数文档生成任务
   - 性价比高

2. **claude-sonnet-4-5** (大上下文)
   - 更强大的理解能力
   - 适合复杂代码分析
   - 更大的上下文窗口

3. **gemini-2.5-pro**
   - Google 的高级模型
   - 多模态支持
   - 适合需要视觉理解的任务

所有模型都支持自定义模型名称，你可以在前端界面中输入任何 LiteLLM 支持的模型。

## 快速开始

### 1. 环境配置

已经为你创建了 `.env` 文件，内容如下：

```bash
# LiteLLM API Settings
LITELLM_API_KEY=sk-wDF58hGeRVZPZwSo_g04FQ
LITELLM_BASE_URL=https://litellm-internal.123u.com/

# Embedder Configuration
DEEPWIKI_EMBEDDER_TYPE=openai
OPENAI_API_KEY=your_openai_api_key_here

# Server Configuration
PORT=8001
SERVER_BASE_URL=http://localhost:8001

# Logging
LOG_LEVEL=INFO
LOG_FILE_PATH=api/logs/application.log
```

⚠️ **注意**: 你还需要配置 `OPENAI_API_KEY` 用于代码嵌入（embeddings）。如果没有 OpenAI API Key，可以考虑：
- 使用 Google AI embeddings: `DEEPWIKI_EMBEDDER_TYPE=google` 并配置 `GOOGLE_API_KEY`
- 使用本地 Ollama embeddings: `DEEPWIKI_EMBEDDER_TYPE=ollama`

### 2. 启动服务

**终端 1 - 启动后端:**
```bash
source .venv/bin/activate
python -m api.main
```

**终端 2 - 启动前端:**
```bash
npm run dev
```

### 3. 使用 LiteLLM

1. 打开浏览器访问 http://localhost:3000
2. 在配置中，**Provider** 会自动选择 **Litellm** (默认)
3. **Model** 默认为 **claude-haiku-4-5**
4. 你可以切换到其他模型或输入自定义模型名称

## 架构说明

### 文件结构

```
api/
├── litellm_client.py          # LiteLLM 客户端实现
├── config.py                  # 配置加载器（已更新）
├── config/
│   └── generator.json         # 生成器配置（包含 litellm 提供商）
└── ...

.env                           # 环境变量配置
.env.example                   # 环境变量模板
```

### 工作原理

1. **LiteLLMClient** 继承自 **OpenAIClient**
   - LiteLLM 兼容 OpenAI API 格式
   - 只需自定义 `base_url` 和环境变量名称

2. **配置系统**
   - `api/config/generator.json` 定义 `litellm` 提供商
   - 配置包括默认模型、可用模型和参数（temperature, top_p）
   - 前端自动从 `/api/models/config` 端点获取配置

3. **请求流程**
   ```
   用户请求 → Next.js Frontend → FastAPI Backend → LiteLLMClient → LiteLLM Service → AI Model
   ```

## 技术实现

### LiteLLM 客户端

```python
# api/litellm_client.py
class LiteLLMClient(OpenAIClient):
    """LiteLLM client that extends OpenAIClient"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        env_base_url_name: str = "LITELLM_BASE_URL",
        env_api_key_name: str = "LITELLM_API_KEY",
    ):
        # 使用自定义的环境变量名称
        super().__init__(
            api_key=api_key,
            base_url=base_url or os.getenv(env_base_url_name, default_base_url),
            env_base_url_name=env_base_url_name,
            env_api_key_name=env_api_key_name,
        )
```

### 配置注册

```python
# api/config.py
CLIENT_CLASSES = {
    "LiteLLMClient": LiteLLMClient,
    # ... 其他客户端
}

default_map = {
    "litellm": LiteLLMClient,
    # ... 其他提供商
}
```

### 模型配置

```json
// api/config/generator.json
{
  "default_provider": "litellm",
  "providers": {
    "litellm": {
      "client_class": "LiteLLMClient",
      "default_model": "claude-haiku-4-5",
      "supportsCustomModel": true,
      "models": {
        "claude-haiku-4-5": {
          "temperature": 0.7,
          "top_p": 0.8
        },
        "claude-sonnet-4-5": {
          "temperature": 0.7,
          "top_p": 0.8
        }
      }
    }
  }
}
```

## 测试

运行集成测试脚本：

```bash
source .venv/bin/activate
python test_litellm.py
```

测试内容包括：
- ✅ 客户端导入
- ✅ 环境变量检查
- ✅ 配置加载
- ✅ 客户端初始化
- ✅ 类映射验证
- ✅ API 端点配置

## 常见问题

### Q: 如何切换到其他模型？

A: 在前端配置界面：
1. 点击配置按钮
2. 选择 Provider: **Litellm**
3. 从下拉菜单选择模型或勾选 "Use custom model" 输入自定义模型名

### Q: 如何添加新的 LiteLLM 模型？

A: 编辑 `api/config/generator.json`：

```json
{
  "providers": {
    "litellm": {
      "models": {
        "新模型名称": {
          "temperature": 0.7,
          "top_p": 0.8
        }
      }
    }
  }
}
```

### Q: LiteLLM 和 OpenAI/Google 有什么区别？

A: LiteLLM 是一个统一代理：
- **优势**: 访问多种模型、统一接口、公司内部部署
- **OpenAI/Google**: 直接访问官方 API，可能需要外网访问

### Q: 如何监控 LiteLLM 请求？

A: 查看日志文件：

```bash
tail -f api/logs/application.log
```

设置 DEBUG 级别查看详细日志：

```bash
# 在 .env 中设置
LOG_LEVEL=DEBUG
```

### Q: LiteLLM 连接失败怎么办？

A: 检查以下几点：
1. 确认 API Key 正确
2. 确认网络可以访问 `https://litellm-internal.123u.com/`
3. 查看后端日志错误信息
4. 验证 LiteLLM 服务是否正常运行

## 与其他提供商对比

| 特性 | LiteLLM | Google | OpenAI | Ollama |
|------|---------|--------|--------|--------|
| 部署位置 | 公司内部 | 公有云 | 公有云 | 本地 |
| 网络要求 | 内网 | 外网 | 外网 | 无 |
| 模型选择 | 多种 | Google 系 | OpenAI 系 | 开源模型 |
| 成本 | 内部计费 | 按使用付费 | 按使用付费 | 免费 |
| 速度 | 快（内网） | 中等 | 中等 | 取决于硬件 |

## 下一步

1. ✅ LiteLLM 已集成并设置为默认提供商
2. ⚠️ 需要配置嵌入模型的 API Key（OpenAI/Google/Ollama）
3. 📝 根据实际使用情况调整模型参数
4. 🔧 如需要其他 LiteLLM 支持的模型，编辑 `generator.json`

## 支持

如有问题，请查看：
- 后端日志: `api/logs/application.log`
- 测试脚本: `python test_litellm.py`
- 主文档: `README.md`
- 架构文档: `CLAUDE.md`
