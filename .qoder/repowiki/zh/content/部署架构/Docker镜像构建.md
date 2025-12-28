# Docker镜像构建

<cite>
**本文档中引用的文件**   
- [Dockerfile](file://Dockerfile)
- [Dockerfile-ollama-local](file://Dockerfile-ollama-local)
- [run.sh](file://run.sh)
- [api/main.py](file://api/main.py)
- [api/requirements.txt](file://api/requirements.txt)
- [package.json](file://package.json)
</cite>

## 目录
1. [简介](#简介)
2. [项目结构](#项目结构)
3. [核心组件](#核心组件)
4. [架构概述](#架构概述)
5. [详细组件分析](#详细组件分析)
6. [依赖分析](#依赖分析)
7. [性能考虑](#性能考虑)
8. [故障排除指南](#故障排除指南)
9. [结论](#结论)

## 简介
本文档详细分析了DeepWiki项目中Docker镜像的构建过程，重点解析了如何通过多阶段构建流程分别构建前端Next.js应用和后端FastAPI服务的生产镜像。文档将深入探讨Dockerfile的结构设计、多阶段构建策略、前后端集成方式以及启动脚本的实现机制。同时，对比了标准Dockerfile与Dockerfile-ollama-local在功能上的差异，特别是后者如何在构建时自动集成Ollama本地AI服务。通过本指南，开发者可以全面理解DeepWiki的容器化部署方案，并掌握针对不同硬件架构的构建方法。

## 项目结构
DeepWiki项目采用前后端分离的架构设计，前端基于Next.js框架构建，后端采用Python FastAPI实现。项目根目录下包含`src/`目录存放前端源码，`api/`目录存放后端API代码，以及两个Dockerfile文件用于不同场景的镜像构建。

```mermaid
graph TD
A[项目根目录] --> B[src/]
A --> C[api/]
A --> D[Dockerfile]
A --> E[Dockerfile-ollama-local]
A --> F[package.json]
A --> G[api/requirements.txt]
B --> H[Next.js前端应用]
C --> I[FastAPI后端服务]
D --> J[标准生产镜像]
E --> K[集成Ollama的本地镜像]
```

**Diagram sources**
- [Dockerfile](file://Dockerfile)
- [Dockerfile-ollama-local](file://Dockerfile-ollama-local)

**Section sources**
- [Dockerfile](file://Dockerfile)
- [Dockerfile-ollama-local](file://Dockerfile-ollama-local)

## 核心组件
DeepWiki的核心组件包括基于Next.js的前端用户界面和基于FastAPI的后端API服务。前端负责提供交互式界面和可视化功能，后端负责处理业务逻辑、与AI模型交互以及管理数据流。两个Dockerfile文件定义了不同的构建策略：标准Dockerfile用于生产环境部署，而Dockerfile-ollama-local则专为本地开发和离线推理设计，集成了Ollama AI服务。

**Section sources**
- [Dockerfile](file://Dockerfile)
- [Dockerfile-ollama-local](file://Dockerfile-ollama-local)
- [api/main.py](file://api/main.py)

## 架构概述
DeepWiki的Docker构建架构采用多阶段构建（multi-stage build）策略，有效分离了构建环境和运行环境，显著减小了最终镜像的体积。构建过程分为四个主要阶段：Node.js依赖安装、前端构建、Python依赖安装和最终镜像组装。这种设计确保了构建过程中所需的开发工具和依赖不会被包含在最终的运行时镜像中。

```mermaid
graph TD
subgraph "构建阶段"
A[node:20-alpine] --> B[安装Node.js依赖]
B --> C[构建Next.js应用]
D[python:3.11-slim] --> E[安装Python依赖]
end
subgraph "最终镜像"
F[python:3.11-slim] --> G[安装Node.js运行时]
G --> H[复制Python依赖]
H --> I[复制前端构建产物]
I --> J[集成启动脚本]
end
C --> I
E --> H
```

**Diagram sources**
- [Dockerfile](file://Dockerfile#L1-L107)

## 详细组件分析

### 多阶段构建流程分析
DeepWiki的Docker构建流程通过多阶段构建实现了高效的镜像优化。整个流程始于两个独立的基础镜像：`node:20-alpine`用于前端构建，`python:3.11-slim`用于后端依赖管理。

#### 前端构建阶段
```mermaid
graph TD
A[node:20-alpine] --> B[安装npm依赖]
B --> C[复制源码]
C --> D[执行npm run build]
D --> E[生成.next/standalone和.next/static]
```

**Diagram sources**
- [Dockerfile](file://Dockerfile#L10-L28)
- [package.json](file://package.json)

#### 后端依赖安装阶段
```mermaid
graph TD
F[python:3.11-slim] --> G[创建虚拟环境]
G --> H[安装requirements.txt中的依赖]
H --> I[生成/opt/venv]
```

**Diagram sources**
- [Dockerfile](file://Dockerfile#L30-L36)
- [api/requirements.txt](file://api/requirements.txt)

#### 最终镜像组装阶段
```mermaid
graph TD
J[python:3.11-slim] --> K[安装Node.js运行时]
K --> L[复制Python虚拟环境]
L --> M[复制前端构建产物]
M --> N[创建启动脚本start.sh]
N --> O[设置CMD指令]
```

**Diagram sources**
- [Dockerfile](file://Dockerfile#L38-L107)
- [run.sh](file://run.sh)

**Section sources**
- [Dockerfile](file://Dockerfile#L1-L107)

### 启动脚本机制分析
启动脚本`start.sh`是DeepWiki容器运行的核心，负责并行启动前后端服务。该脚本首先加载环境变量，检查关键API密钥的配置状态，然后以后台进程方式同时启动FastAPI后端和Next.js服务。

```mermaid
graph TD
A[启动start.sh] --> B[加载.env文件]
B --> C[检查OPENAI_API_KEY和GOOGLE_API_KEY]
C --> D[后台启动python -m api.main]
C --> E[后台启动node server.js]
D --> F[等待任一进程结束]
E --> F
F --> G[退出容器]
```

**Diagram sources**
- [Dockerfile](file://Dockerfile#L88-L97)
- [api/main.py](file://api/main.py)

**Section sources**
- [Dockerfile](file://Dockerfile#L80-L107)
- [api/main.py](file://api/main.py)

### Dockerfile-ollama-local特殊构建分析
`Dockerfile-ollama-local`在标准构建流程的基础上增加了Ollama服务的集成，使其能够在容器内运行本地AI模型。

#### Ollama集成流程
```mermaid
graph TD
A[ollama_base阶段] --> B[根据TARGETARCH下载对应架构的Ollama]
B --> C[解压并安装Ollama二进制文件]
C --> D[启动ollama serve]
D --> E[拉取nomic-embed-text模型]
E --> F[拉取qwen3:1.7b模型]
F --> G[将Ollama二进制文件复制到最终镜像]
```

**Diagram sources**
- [Dockerfile-ollama-local](file://Dockerfile-ollama-local#L40-L70)

#### 启动脚本差异分析
与标准Dockerfile相比，`Dockerfile-ollama-local`的启动脚本首先启动Ollama服务，然后再启动应用服务，确保AI模型服务的可用性。

```mermaid
graph TD
A[启动start.sh] --> B[后台启动ollama serve]
B --> C[加载.env文件]
C --> D[检查API密钥]
D --> E[后台启动python -m api.main]
D --> F[后台启动node server.js]
E --> G[等待任一进程结束]
F --> G
G --> H[退出容器]
```

**Diagram sources**
- [Dockerfile-ollama-local](file://Dockerfile-ollama-local#L100-L108)

**Section sources**
- [Dockerfile-ollama-local](file://Dockerfile-ollama-local#L1-L116)

## 依赖分析
DeepWiki项目的依赖管理通过Docker多阶段构建得到了有效优化。前端依赖通过`package.json`和`package-lock.json`管理，后端依赖通过`api/requirements.txt`管理。构建过程中，各阶段的依赖被隔离处理，最终镜像仅包含运行时必需的依赖。

```mermaid
graph TD
subgraph "前端依赖"
A[package.json] --> B[Node.js模块]
B --> C[Next.js框架]
C --> D[React库]
end
subgraph "后端依赖"
E[requirements.txt] --> F[FastAPI]
F --> G[google-generativeai]
G --> H[ollama]
H --> I[adalflow]
end
subgraph "最终镜像"
J[Node.js运行时] --> K[前端静态资源]
L[Python虚拟环境] --> M[后端API服务]
end
C --> K
F --> M
```

**Diagram sources**
- [package.json](file://package.json)
- [api/requirements.txt](file://api/requirements.txt)

**Section sources**
- [package.json](file://package.json)
- [api/requirements.txt](file://api/requirements.txt)

## 性能考虑
DeepWiki的Docker构建策略充分考虑了性能和资源利用效率。通过使用轻量级基础镜像（alpine和slim），显著减小了镜像体积。多阶段构建避免了将构建工具和开发依赖包含在最终镜像中，提高了容器启动速度和安全性。同时，启动脚本中的并行服务启动机制确保了应用的快速响应。

## 故障排除指南
在构建和运行DeepWiki Docker镜像时可能遇到的常见问题及解决方案：

1. **API密钥警告**：启动时若未设置`OPENAI_API_KEY`或`GOOGLE_API_KEY`，容器会发出警告。解决方案是通过环境变量或挂载`.env`文件提供这些密钥。
2. **架构不匹配**：使用`Dockerfile-ollama-local`时，若`TARGETARCH`参数设置错误，会导致Ollama下载失败。应根据目标硬件正确设置`arm64`或`amd64`。
3. **证书问题**：若需要自定义CA证书，可通过构建参数`CUSTOM_CERT_DIR`指定证书目录，镜像构建时会自动更新证书。
4. **端口冲突**：默认使用8001端口（后端）和3000端口（前端），若发生冲突，可通过环境变量`PORT`进行修改。

**Section sources**
- [Dockerfile](file://Dockerfile#L80-L97)
- [Dockerfile-ollama-local](file://Dockerfile-ollama-local#L100-L108)

## 结论
DeepWiki的Docker构建方案展示了现代化Web应用容器化的最佳实践。通过多阶段构建，项目实现了构建环境与运行环境的完全分离，确保了最终镜像的安全性和轻量化。标准Dockerfile与`Dockerfile-ollama-local`的设计体现了灵活性和可扩展性，既能满足生产环境的部署需求，又能支持本地AI模型的集成。启动脚本的精心设计确保了前后端服务的协调运行。开发者可以根据具体需求选择合适的构建方案，并通过简单的构建命令为不同硬件架构生成优化的镜像。