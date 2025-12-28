# API参考

<cite>
**本文档中引用的文件**   
- [api.py](file://api/api.py)
- [simple_chat.py](file://api/simple_chat.py)
- [config.py](file://api/config.py)
- [route.ts](file://src/app/api/chat/stream/route.ts)
- [route.ts](file://src/app/api/auth/status/route.ts)
- [route.ts](file://src/app/api/auth/validate/route.ts)
- [route.ts](file://src/app/api/models/config/route.ts)
</cite>

## 目录
1. [简介](#简介)
2. [/chat/completions/stream](#chatcompletionsstream)
3. [/auth/status](#authstatus)
4. [/auth/validate](#authvalidate)
5. [/models/config](#modelsconfig)
6. [认证方式](#认证方式)
7. [错误处理](#错误处理)
8. [性能建议](#性能建议)

## 简介
本API参考文档详细描述了deepwiki-open项目中的所有RESTful API端点。文档涵盖了HTTP方法、URL路径、请求头、请求体结构、响应格式与状态码等关键信息。特别说明了流式接口`/chat/completions/stream`的SSE（Server-Sent Events）实现机制与客户端处理方式，以及认证相关端点的代理后端逻辑。每个端点都标注了其对应的前后端文件路径，便于开发者查阅源码。

## /chat/completions/stream

### 概述
流式聊天补全端点，用于实时获取AI生成的响应。该端点支持多种模型提供商，并通过Server-Sent Events (SSE) 实现流式传输。

### HTTP方法
`POST`

### URL路径
`/chat/completions/stream`

### 请求头
- `Content-Type: application/json`
- `Accept: text/event-stream`

### 请求体结构
```json
{
  "repo_url": "string",
  "messages": [
    {
      "role": "user|assistant",
      "content": "string"
    }
  ],
  "filePath": "string",
  "token": "string",
  "type": "string",
  "provider": "string",
  "model": "string",
  "language": "string",
  "excluded_dirs": "string",
  "excluded_files": "string",
  "included_dirs": "string",
  "included_files": "string"
}
```

### 响应格式
流式文本响应，使用Server-Sent Events (SSE) 格式：
```
data: {chunk of text}

data: {another chunk of text}

data: [DONE]
```

### 状态码
- `200`: 成功，开始流式传输
- `400`: 请求参数错误
- `500`: 服务器内部错误

### 示例请求
```json
{
  "repo_url": "https://github.com/user/repo",
  "messages": [
    {
      "role": "user",
      "content": "What is this repository about?"
    }
  ],
  "provider": "google",
  "model": "gemini-1.5-flash"
}
```

### 示例响应
```
data: This repository is about

data: building AI-powered documentation

data: [DONE]
```

### SSE实现机制
后端使用`StreamingResponse`返回`text/event-stream`类型的数据。每个响应块以`data: `开头，最后以`data: [DONE]`结束。前端通过EventSource或fetch API接收并处理这些事件。

### 客户端处理方式
1. 使用fetch API发起POST请求
2. 设置`Accept: text/event-stream`头
3. 通过`.body.getReader()`读取流式数据
4. 将接收到的文本块拼接显示

### 前后端文件路径
- **前端**: `src/app/api/chat/stream/route.ts`
- **后端**: `api/simple_chat.py`

**Section sources**
- [simple_chat.py](file://api/simple_chat.py#L1-L690)
- [route.ts](file://src/app/api/chat/stream/route.ts#L1-L113)

## /auth/status

### 概述
检查认证状态端点，用于确定是否需要对wiki进行认证。

### HTTP方法
`GET`

### URL路径
`/auth/status`

### 请求头
- `Content-Type: application/json`

### 响应格式
```json
{
  "auth_required": boolean
}
```

### 状态码
- `200`: 成功，返回认证状态
- `500`: 服务器内部错误

### 示例响应
```json
{
  "auth_required": true
}
```

### 代理后端逻辑
该端点作为代理，将请求转发到后端API `/auth/status`。它从环境变量`SERVER_BASE_URL`获取目标服务器基础URL，然后使用`fetch`向后端服务发起GET请求，并将响应转发给客户端。

### 前后端文件路径
- **前端**: `src/app/api/auth/status/route.ts`
- **后端**: `api/api.py`

**Section sources**
- [api.py](file://api/api.py#L1-L635)
- [route.ts](file://src/app/api/auth/status/route.ts#L1-L32)

## /auth/validate

### 概述
验证授权码端点，用于检查提供的授权码是否正确。

### HTTP方法
`POST`

### URL路径
`/auth/validate`

### 请求头
- `Content-Type: application/json`

### 请求体结构
```json
{
  "code": "string"
}
```

### 响应格式
```json
{
  "success": boolean
}
```

### 状态码
- `200`: 成功，返回验证结果
- `500`: 服务器内部错误

### 示例请求
```json
{
  "code": "secret123"
}
```

### 示例响应
```json
{
  "success": true
}
```

### 代理后端逻辑
该端点作为代理，将请求转发到后端API `/auth/validate`。它从环境变量`SERVER_BASE_URL`获取目标服务器基础URL，然后使用`fetch`向后端服务发起POST请求，并将响应转发给客户端。

### 前后端文件路径
- **前端**: `src/app/api/auth/validate/route.ts`
- **后端**: `api/api.py`

**Section sources**
- [api.py](file://api/api.py#L1-L635)
- [route.ts](file://src/app/api/auth/validate/route.ts#L1-L35)

## /models/config

### 概述
获取模型配置端点，返回可用的模型提供商及其模型列表。

### HTTP方法
`GET`

### URL路径
`/models/config`

### 请求头
- `Accept: application/json`

### 响应格式
```json
{
  "providers": [
    {
      "id": "string",
      "name": "string",
      "supportsCustomModel": boolean,
      "models": [
        {
          "id": "string",
          "name": "string"
        }
      ]
    }
  ],
  "defaultProvider": "string"
}
```

### 状态码
- `200`: 成功，返回模型配置
- `500`: 服务器内部错误

### 示例响应
```json
{
  "providers": [
    {
      "id": "google",
      "name": "Google",
      "supportsCustomModel": true,
      "models": [
        {
          "id": "gemini-1.5-flash",
          "name": "Gemini 1.5 Flash"
        }
      ]
    }
  ],
  "defaultProvider": "google"
}
```

### 前后端文件路径
- **前端**: `src/app/api/models/config/route.ts`
- **后端**: `api/api.py`

**Section sources**
- [api.py](file://api/api.py#L1-L635)
- [route.ts](file://src/app/api/models/config/route.ts#L1-L49)

## 认证方式
本API使用API Key进行认证。API Key需要通过环境变量配置：
- `OPENAI_API_KEY`: OpenAI API密钥
- `GOOGLE_API_KEY`: Google API密钥
- `OPENROUTER_API_KEY`: OpenRouter API密钥
- `DEEPWIKI_AUTH_CODE`: DeepWiki认证码

对于需要认证的wiki，客户端需要在请求中提供正确的授权码。认证状态由`WIKI_AUTH_MODE`环境变量控制，当其值为`true`时启用认证。

## 错误处理
API采用标准的HTTP状态码进行错误处理：

### 常见错误状态码
- `400 Bad Request`: 请求参数错误或缺失
- `401 Unauthorized`: 未授权访问
- `500 Internal Server Error`: 服务器内部错误

### 错误响应格式
```json
{
  "error": "string"
}
```

### 特殊错误处理
- 流式响应中的错误会作为文本块返回，而不是HTTP错误
- 模型调用超时或失败时，系统会尝试降级处理
- RAG检索失败时会记录警告但继续处理请求

## 性能建议
1. **流式传输**: 对于长响应，使用`/chat/completions/stream`端点以获得更好的用户体验
2. **缓存**: 利用wiki缓存机制减少重复计算
3. **连接复用**: 对于WebSocket连接，保持连接复用以减少握手开销
4. **批量处理**: 在可能的情况下，将多个小请求合并为单个大请求
5. **超时设置**: 为所有HTTP请求设置合理的超时时间
6. **错误重试**: 实现指数退避重试机制处理临时性错误