# LLM客户端集成

<cite>
**本文档中引用的文件**   
- [openai_client.py](file://api/openai_client.py)
- [google_embedder_client.py](file://api/google_embedder_client.py)
- [azureai_client.py](file://api/azureai_client.py)
- [bedrock_client.py](file://api/bedrock_client.py)
- [dashscope_client.py](file://api/dashscope_client.py)
- [openrouter_client.py](file://api/openrouter_client.py)
- [ollama_patch.py](file://api/ollama_patch.py)
- [config.py](file://api/config.py)
- [rag.py](file://api/rag.py)
</cite>

## 目录
1. [简介](#简介)
2. [OpenAI客户端](#openai客户端)
3. [Google嵌入客户端](#google嵌入客户端)
4. [Azure AI客户端](#azure-ai客户端)
5. [AWS Bedrock客户端](#aws-bedrock客户端)
6. [阿里云通义千问客户端](#阿里云通义千问客户端)
7. [OpenRouter客户端](#openrouter客户端)
8. [Ollama客户端](#ollama客户端)
9. [模型参数对比](#模型参数对比)
10. [配置示例](#配置示例)
11. [常见问题解决方案](#常见问题解决方案)

## 简介
本文档详细介绍了DeepWiki项目中集成的各种大型语言模型（LLM）客户端的实现方式和认证机制。文档涵盖了OpenAI、Google、Azure AI、AWS Bedrock、阿里云通义千问、OpenRouter和Ollama等主要提供商的客户端实现，重点说明了`openai_client.py`如何封装OpenAI API调用，`google_embedder_client.py`如何使用Google Generative AI SDK，以及`ollama_patch.py`的特殊作用。此外，文档还对比了不同客户端的模型参数差异，提供了各提供商的配置示例和常见问题解决方案。

## OpenAI客户端
`openai_client.py`文件实现了`OpenAIClient`类，该类作为OpenAI API的组件包装器，支持嵌入和聊天补全API，包括多模态功能。该客户端通过`adalflow.core.model_client.ModelClient`基类进行扩展，提供了统一的接口来与OpenAI服务进行交互。

`OpenAIClient`的初始化接受可选的API密钥、聊天补全解析器、输入类型、基础URL、环境变量基础URL名称和环境变量API密钥名称等参数。推荐通过设置`OPENAI_API_KEY`环境变量来提供API密钥，而不是直接在代码中传递。客户端支持同步和异步调用，通过`init_sync_client`和`init_async_client`方法分别初始化同步和异步客户端实例。

该客户端支持多种模型类型，包括`EMBEDDER`、`LLM`和`IMAGE_GENERATION`。对于嵌入模型，输入被转换为API特定的格式并传递给`embeddings.create`方法。对于LLM模型，输入被转换为消息格式，并支持流式调用。对于图像生成模型，支持DALL-E 3和DALL-E 2模型，可以生成、编辑或创建图像变体。

**Section sources**
- [openai_client.py](file://api/openai_client.py#L1-L630)

## Google嵌入客户端
`google_embedder_client.py`文件实现了`GoogleEmbedderClient`类，该类作为Google AI嵌入API的组件包装器。该客户端通过Google AI API提供对Google嵌入模型的访问，支持语义相似性、检索和分类等任务。

`GoogleEmbedderClient`的初始化接受可选的API密钥和环境变量API密钥名称参数。与OpenAI客户端类似，推荐通过设置`GOOGLE_API_KEY`环境变量来提供API密钥。客户端在初始化时调用`_initialize_client`方法，使用API密钥配置`google.generativeai`库。

该客户端主要支持`EMBEDDER`模型类型。`convert_inputs_to_api_kwargs`方法将输入转换为Google AI API格式，确保输入为字符串或字符串序列，并设置默认的任务类型为`SEMANTIC_SIMILARITY`和默认模型为`text-embedding-004`。`call`方法处理API调用，支持单个文本嵌入和批量嵌入，而`acall`方法由于Google AI Python客户端目前不支持异步，因此回退到同步调用。

**Section sources**
- [google_embedder_client.py](file://api/google_embedder_client.py#L1-L231)

## Azure AI客户端
`azureai_client.py`文件实现了`AzureAIClient`类，该类作为Azure OpenAI API的客户端包装器。该类支持嵌入和聊天补全API调用，用户可以通过`Embedder`和`Generator`组件简化与Azure OpenAI模型的交互。

`AzureAIClient`的初始化支持两种认证方式：API密钥或Azure Active Directory (AAD)令牌认证。客户端通过`init_sync_client`和`init_async_client`方法初始化同步和异步客户端实例。初始化时，客户端会检查`AZURE_OPENAI_ENDPOINT`和`AZURE_OPENAI_VERSION`环境变量是否已设置。

该客户端支持`EMBEDDER`和`LLM`模型类型。`convert_inputs_to_api_kwargs`方法将输入转换为API特定格式，对于嵌入模型，输入被转换为`input`参数；对于LLM模型，输入被转换为消息格式。`call`和`acall`方法分别处理同步和异步API调用，支持流式调用。

**Section sources**
- [azureai_client.py](file://api/azureai_client.py#L1-L488)

## AWS Bedrock客户端
`bedrock_client.py`文件实现了`BedrockClient`类，该类作为AWS Bedrock API的组件包装器。AWS Bedrock提供了一个统一的API，可以访问各种基础模型，包括Amazon自己的模型和第三方模型如Anthropic Claude。

`BedrockClient`的初始化接受AWS访问密钥ID、AWS秘密访问密钥、AWS区域和AWS角色ARN等参数。客户端通过`init_sync_client`方法初始化同步客户端，支持通过IAM角色进行身份验证。`_get_model_provider`方法从模型ID中提取提供商名称，`_format_prompt_for_provider`方法根据提供商的要求格式化提示。

该客户端主要支持`LLM`模型类型。`call`方法处理同步API调用，根据模型提供商（如Anthropic、Amazon、Cohere、AI21）格式化请求体并调用`invoke_model` API。`acall`方法目前回退到同步调用，因为boto3不支持原生异步。`convert_inputs_to_api_kwargs`方法将输入转换为API特定格式，支持温度和top_p等模型参数。

**Section sources**
- [bedrock_client.py](file://api/bedrock_client.py#L1-L318)

## 阿里云通义千问客户端
`dashscope_client.py`文件实现了`DashscopeClient`类，该类作为阿里云通义千问API的组件包装器。该客户端通过OpenAI兼容的API提供对阿里云Qwen和其他模型的访问。

`DashscopeClient`的初始化接受API密钥、工作区ID、聊天补全解析器、输入类型、基础URL、环境变量基础URL名称、环境变量API密钥名称和环境变量工作区ID名称等参数。客户端通过`_prepare_client_config`方法准备客户端配置，确保API密钥已提供，并将工作区ID存储在客户端实例中。

该客户端支持`LLM`和`EMBEDDER`模型类型。`convert_inputs_to_api_kwargs`方法将输入转换为API特定格式，对于LLM模型，输入被转换为消息格式，并在请求头中添加工作区ID；对于嵌入模型，文档对象的文本被提取并传递给API。`call`方法处理API调用，对于非流式调用，`enable_thinking`必须为false，并通过`extra_body`参数传递。

**Section sources**
- [dashscope_client.py](file://api/dashscope_client.py#L1-L914)

## OpenRouter客户端
`openrouter_client.py`文件实现了`OpenRouterClient`类，该类作为OpenRouter API的组件包装器。OpenRouter提供了一个统一的API，可以通过单个端点访问数百个AI模型。

`OpenRouterClient`的初始化通过`init_sync_client`和`init_async_client`方法初始化同步和异步客户端实例。客户端使用`requests`和`aiohttp`库直接与OpenRouter API进行交互。`convert_inputs_to_api_kwargs`方法将AdalFlow输入转换为OpenRouter API格式，支持LLM生成。

`acall`方法处理异步API调用，使用`aiohttp.ClientSession`发送POST请求到`https://openrouter.ai/api/v1/chat/completions`。请求头包括授权令牌、内容类型、HTTP引用和X-Title。`_process_async_streaming_response`方法处理异步流式响应，解析SSE数据并提取内容。客户端还包含错误处理逻辑，返回生成器以在流式响应中显示错误消息。

**Section sources**
- [openrouter_client.py](file://api/openrouter_client.py#L1-L526)

## Ollama客户端
`ollama_patch.py`文件包含`check_ollama_model_exists`函数和`OllamaDocumentProcessor`类，用于处理Ollama模型的特殊需求。`check_ollama_model_exists`函数检查Ollama模型是否存在，通过向Ollama主机发送GET请求到`/api/tags`端点来获取可用模型列表。

`OllamaModelNotFoundError`是当Ollama模型未找到时引发的自定义异常。`OllamaDocumentProcessor`类作为数据组件，处理Ollama嵌入的文档，由于Adalflow Ollama客户端不支持批量嵌入，因此需要逐个处理每个文档。该类在`__call__`方法中遍历文档，为每个文档获取嵌入，并验证嵌入大小的一致性。

在`rag.py`文件中，`RAG`类在初始化时检查是否使用Ollama嵌入器，如果是，则调用`check_ollama_model_exists`函数验证模型是否存在，如果不存在则引发异常。这确保了在尝试使用Ollama模型之前，模型已正确安装。

**Section sources**
- [ollama_patch.py](file://api/ollama_patch.py#L1-L105)
- [rag.py](file://api/rag.py#L1-L446)

## 模型参数对比
不同LLM提供商的模型参数存在显著差异，主要体现在模型名称、温度、top_p、最大令牌数等参数上。以下是各提供商的主要参数对比：

| 提供商 | 模型名称 | 温度 | top_p | 最大令牌数 | 其他参数 |
| --- | --- | --- | --- | --- | --- |
| OpenAI | gpt-4o, gpt-3.5-turbo | 0.7 | 0.8 | 4096 | num_ctx, frequency_penalty |
| Google | gemini-pro, gemini-pro-vision | 0.7 | 0.8 | 8192 | top_k |
| Azure AI | gpt-35-turbo, gpt-4 | 0.7 | 0.8 | 4096 | api_version |
| AWS Bedrock | anthropic.claude-3-sonnet-20240229-v1:0 | 0.7 | 0.8 | 4096 | model_id |
| 阿里云通义千问 | qwen-turbo, qwen-plus | 0.7 | 0.8 | 8192 | workspace_id |
| OpenRouter | openai/gpt-4o, anthropic/claude-3-sonnet | 0.7 | 0.8 | 4096 | provider |
| Ollama | llama2, mistral | 0.7 | 0.8 | 2048 | num_ctx, num_gpu |

**Section sources**
- [config.py](file://api/config.py#L1-L388)

## 配置示例
以下是各提供商的配置示例，展示了如何在环境中设置必要的环境变量。

### OpenAI配置
```bash
export OPENAI_API_KEY="your_openai_api_key"
export OPENAI_BASE_URL="https://api.openai.com/v1"
```

### Google配置
```bash
export GOOGLE_API_KEY="your_google_api_key"
```

### Azure AI配置
```bash
export AZURE_OPENAI_API_KEY="your_azure_api_key"
export AZURE_OPENAI_ENDPOINT="https://your-endpoint.openai.azure.com/"
export AZURE_OPENAI_VERSION="2023-05-15"
```

### AWS Bedrock配置
```bash
export AWS_ACCESS_KEY_ID="your_aws_access_key_id"
export AWS_SECRET_ACCESS_KEY="your_aws_secret_access_key"
export AWS_REGION="us-east-1"
export AWS_ROLE_ARN="your_aws_role_arn"
```

### 阿里云通义千问配置
```bash
export DASHSCOPE_API_KEY="your_dashscope_api_key"
export DASHSCOPE_WORKSPACE_ID="your_workspace_id"
export DASHSCOPE_BASE_URL="https://dashscope.aliyuncs.com/compatible-mode/v1"
```

### OpenRouter配置
```bash
export OPENROUTER_API_KEY="your_openrouter_api_key"
```

### Ollama配置
```bash
export OLLAMA_HOST="http://localhost:11434"
```

**Section sources**
- [config.py](file://api/config.py#L1-L388)

## 常见问题解决方案
### API密钥设置
确保为每个提供商正确设置API密钥环境变量。如果密钥未设置，客户端将引发`ValueError`异常。例如，`OpenAIClient`要求`OPENAI_API_KEY`环境变量必须已设置。

### 模型拉取命令
对于Ollama模型，如果模型不存在，需要使用`ollama pull`命令安装模型。例如：
```bash
ollama pull llama2
ollama pull mistral
```

### 连接问题
确保Ollama服务正在运行，并且`OLLAMA_HOST`环境变量指向正确的主机和端口。如果无法连接到Ollama，`check_ollama_model_exists`函数将返回`False`。

### 嵌入大小不一致
在使用Ollama嵌入器时，可能会遇到嵌入大小不一致的问题。`OllamaDocumentProcessor`类在处理文档时会验证嵌入大小的一致性，如果发现不一致的嵌入大小，将跳过该文档。

### 令牌限制
某些模型有令牌限制，如果输入文本的令牌数超过限制，API调用将失败。使用`count_tokens`函数估算输入文本的令牌数，并确保其在模型的限制范围内。

**Section sources**
- [ollama_patch.py](file://api/ollama_patch.py#L1-L105)
- [data_pipeline.py](file://api/data_pipeline.py#L1-L882)