# 认证API

<cite>
**本文档中引用的文件**   
- [route.ts](file://src/app/api/auth/status/route.ts)
- [route.ts](file://src/app/api/auth/validate/route.ts)
- [api.py](file://api/api.py)
- [config.py](file://api/config.py)
</cite>

## 目录
1. [简介](#简介)
2. [核心端点分析](#核心端点分析)
3. [认证流程与安全机制](#认证流程与安全机制)
4. [请求与响应示例](#请求与响应示例)
5. [环境变量配置](#环境变量配置)
6. [架构图](#架构图)

## 简介
本文档详细说明了本系统中与认证相关的API端点。重点阐述了前端Next.js应用如何通过API路由作为代理，将认证请求转发至后端FastAPI服务。文档详细描述了`/auth/status`和`/api/auth/validate`两个核心端点的功能、交互流程以及它们在保护敏感操作（如维基缓存删除）中的安全作用。

**Section sources**
- [route.ts](file://src/app/api/auth/status/route.ts)
- [route.ts](file://src/app/api/auth/validate/route.ts)
- [api.py](file://api/api.py)

## 核心端点分析

### `/auth/status` 端点
此端点用于查询系统当前的认证状态。前端应用通过调用此端点来确定用户是否需要提供授权码才能执行某些操作。

- **前端实现**: 位于 `src/app/api/auth/status/route.ts`，它接收来自浏览器的GET请求，并将其代理转发至后端服务器的`/auth/status`端点。
- **后端实现**: 位于 `api/api.py` 中的 `get_auth_status()` 函数。该函数直接返回一个JSON对象 `{auth_required: boolean}`，其布尔值由环境变量 `WIKI_AUTH_MODE` 决定。

### `/api/auth/validate` 端点
此端点用于验证用户提交的授权码是否有效。

- **前端实现**: 位于 `src/app/api/auth/validate/route.ts`，它接收来自浏览器的POST请求，提取请求体中的授权码，并将其转发至后端服务器的`/auth/validate`端点。
- **后端实现**: 位于 `api/api.py` 中的 `validate_auth_code()` 函数。该函数接收一个包含授权码的JSON请求体，将其与环境变量 `WIKI_AUTH_CODE` 中存储的正确码进行比对，并返回 `{success: boolean}` 结果。

**Section sources**
- [route.ts](file://src/app/api/auth/status/route.ts#L1-L31)
- [route.ts](file://src/app/api/auth/validate/route.ts#L1-L34)
- [api.py](file://api/api.py#L100-L110)

## 认证流程与安全机制

系统的认证流程设计为前后端分离的代理模式，确保了安全逻辑的集中管理。

1.  **状态查询**: 前端在需要保护的页面加载时，首先调用 `/auth/status`。如果返回 `auth_required: true`，前端将提示用户输入授权码。
2.  **授权码验证**: 用户输入授权码后，前端调用 `/api/auth/validate` 端点进行验证。
3.  **敏感操作保护**: 当用户尝试执行敏感操作（如通过 `DELETE /api/wiki_cache` 删除维基缓存）时，后端会检查 `WIKI_AUTH_MODE`。如果为 `true`，则必须在请求中提供有效的 `authorization_code` 查询参数，否则将返回401未授权错误。

这种设计将认证逻辑完全置于后端控制之下，前端仅作为请求的转发者，有效防止了客户端绕过认证。

**Section sources**
- [api.py](file://api/api.py#L100-L110)
- [api.py](file://api/api.py#L480-L495)
- [config.py](file://api/config.py#L44-L45)

## 请求与响应示例

### 查询认证状态
**请求**
```http
GET /api/auth/status HTTP/1.1
Host: your-frontend-domain.com
```

**响应 (需要认证)**
```json
{
  "auth_required": true
}
```

**响应 (无需认证)**
```json
{
  "auth_required": false
}
```

### 验证授权码
**请求**
```http
POST /api/auth/validate HTTP/1.1
Host: your-frontend-domain.com
Content-Type: application/json

{
  "code": "your-secret-code"
}
```

**响应 (验证成功)**
```json
{
  "success": true
}
```

**响应 (验证失败)**
```json
{
  "success": false
}
```

**Section sources**
- [route.ts](file://src/app/api/auth/status/route.ts)
- [route.ts](file://src/app/api/auth/validate/route.ts)

## 环境变量配置

认证行为由两个关键的环境变量控制，它们在 `api/config.py` 文件中被读取和解析。

- **`DEEPWIKI_AUTH_MODE`**: 一个布尔值，用于开启或关闭全局认证。当设置为 `true`、`1` 或 `t` 时，系统将要求所有敏感操作提供授权码。其值被解析后存储在 `WIKI_AUTH_MODE` 变量中。
- **`DEEPWIKI_AUTH_CODE`**: 存储系统所期望的授权码字符串。当 `WIKI_AUTH_MODE` 为 `true` 时，用户提交的码必须与此环境变量的值完全匹配才能通过验证。

**Section sources**
- [config.py](file://api/config.py#L44-L45)

## 架构图

以下图表展示了认证请求在前端和后端之间的代理流程。

```mermaid
flowchart TD
A[前端浏览器] --> |GET /api/auth/status| B[Next.js API路由<br/>/src/app/api/auth/status/route.ts]
B --> |GET /auth/status| C[FastAPI后端<br/>/api/api.py]
C --> |{auth_required: true/false}| B
B --> |{auth_required: true/false}| A
A --> |POST /api/auth/validate| D[Next.js API路由<br/>/src/app/api/auth/validate/route.ts]
D --> |POST /auth/validate| C
C --> |{success: true/false}| D
D --> |{success: true/false}| A
A --> |DELETE /api/wiki_cache?authorization_code=...| E[FastAPI后端<br/>/api/api.py]
E --> |检查 WIKI_AUTH_MODE| F{需要认证?}
F --> |是| G[检查 authorization_code]
G --> |匹配 WIKI_AUTH_CODE?| H{有效?}
H --> |是| I[执行删除]
H --> |否| J[返回 401]
F --> |否| I
```

**Diagram sources**
- [route.ts](file://src/app/api/auth/status/route.ts)
- [route.ts](file://src/app/api/auth/validate/route.ts)
- [api.py](file://api/api.py)
- [config.py](file://api/config.py)