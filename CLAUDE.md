# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

DeepWiki is an AI-powered documentation generator that automatically creates interactive wikis from GitHub/GitLab/BitBucket repositories. The system uses a Python FastAPI backend for AI processing and RAG (Retrieval Augmented Generation), with a Next.js frontend for the user interface.

## Technology Stack

- **Backend**: Python 3.12+, FastAPI, uvicorn
- **Frontend**: Next.js 15.3, React 19, TypeScript, Tailwind CSS
- **AI/ML**: AdalFlow framework, FAISS vector database, multiple LLM providers (LiteLLM, Google Gemini, OpenAI, Azure, OpenRouter, Ollama, DashScope)
- **Embeddings**: Supports OpenAI, Google AI, and Ollama embedders
- **Default Provider**: LiteLLM (company internal deployment)

## Development Commands

### Backend (Python API)

```bash
# Install dependencies (using uv - preferred)
uv sync

# Or using pip
pip install -r api/requirements.txt

# Start API server (from project root)
python -m api.main
# Server runs on http://localhost:8001

# Run tests
python tests/run_tests.py              # All tests
python tests/run_tests.py --unit       # Unit tests only
python tests/run_tests.py --integration # Integration tests only
python tests/run_tests.py --api        # API tests only
pytest                                 # Using pytest directly
pytest -m unit                         # Run unit tests with pytest
pytest -m integration                  # Run integration tests with pytest
```

### Frontend (Next.js)

```bash
# Install dependencies
npm install
# Or
yarn install

# Start development server
npm run dev
# Or
yarn dev
# Runs on http://localhost:3000 with Turbopack

# Build for production
npm run build

# Start production server
npm start

# Lint code
npm run lint
```

### Docker

```bash
# Build image
docker build -t deepwiki-open .

# Run with Docker Compose (recommended)
docker-compose up

# Pull from GitHub Container Registry
docker pull ghcr.io/asyncfuncai/deepwiki-open:latest
```

## Architecture

### High-Level Data Flow

1. **User Input** → User enters GitHub/GitLab/BitBucket repository URL
2. **Repository Cloning** → Backend clones repo to `~/.adalflow/repos/`
3. **Document Processing** → Files are read, filtered, and chunked using TextSplitter
4. **Embedding Creation** → Code is embedded using selected embedder (OpenAI/Google/Ollama)
5. **Vector Storage** → Embeddings stored in FAISS database at `~/.adalflow/databases/`
6. **Wiki Generation** → AI generates structured wiki pages with Mermaid diagrams
7. **Caching** → Generated wikis cached at `~/.adalflow/wikicache/`
8. **Interactive Q&A** → RAG enables chat with repository context

### Backend Architecture

The Python backend follows a modular provider-based architecture:

#### Core Modules

- **`api/main.py`**: Entry point, initializes FastAPI server
- **`api/api.py`**: Main FastAPI app with REST endpoints, wiki generation, cache management
- **`api/websocket_wiki.py`**: WebSocket handler for real-time wiki generation streaming
- **`api/simple_chat.py`**: HTTP streaming endpoint for chat completions (alternative to WebSocket)
- **`api/data_pipeline.py`**: Repository operations - cloning, file reading, document processing, embedding creation
- **`api/rag.py`**: RAG implementation using FAISS retriever, manages conversation memory
- **`api/config.py`**: Configuration loader, environment variable handling, provider setup

#### AI Provider Clients

Each provider has its own client module implementing a common interface:

- **`api/litellm_client.py`**: LiteLLM unified proxy (company internal, supports Claude, GPT, Gemini) - **DEFAULT**
- **`api/openai_client.py`**: OpenAI GPT models (supports custom base URL for enterprise)
- **`api/openrouter_client.py`**: OpenRouter API (access to multiple models)
- **`api/azureai_client.py`**: Azure OpenAI integration
- **`api/dashscope_client.py`**: Alibaba DashScope (Qwen models, DeepSeek)
- **`api/bedrock_client.py`**: AWS Bedrock integration
- **`api/google_embedder_client.py`**: Google AI embeddings (text-embedding-004)
- **`api/ollama_patch.py`**: Ollama local model support with custom document processor

All clients support streaming responses and are configured via JSON files in `api/config/`.

**LiteLLM Client**: Extends OpenAIClient since LiteLLM is OpenAI-compatible. Uses custom environment variables (`LITELLM_API_KEY`, `LITELLM_BASE_URL`) to connect to internal company deployment at `https://litellm-internal.123u.com/`.

#### Configuration System

DeepWiki uses JSON configuration files for flexibility:

- **`api/config/generator.json`**: Defines LLM providers, models, parameters (temperature, top_p)
- **`api/config/embedder.json`**: Embedder configuration, retriever settings, text splitter config
- **`api/config/repo.json`**: File filters, excluded/included patterns, repository limits
- **`api/config/lang.json`**: Internationalization language mappings

Configuration files support environment variable substitution using `${ENV_VAR}` syntax.

Set custom config directory: `DEEPWIKI_CONFIG_DIR=/path/to/config`

#### Key Workflows

**Wiki Generation Flow** (`api/api.py` + `api/websocket_wiki.py`):
1. Parse repository URL and validate access
2. Clone repository using `download_repo()` from data_pipeline
3. Create document database with `create_or_load_db()` (includes filtering, chunking, embedding)
4. Generate wiki structure with AI (sections, pages, importance ranking)
5. Generate individual wiki pages with RAG-enhanced context
6. Auto-fix Mermaid diagram syntax errors
7. Cache complete wiki structure as JSON

**RAG Chat Flow** (`api/rag.py` + `api/simple_chat.py`/`api/websocket_wiki.py`):
1. Initialize RAG instance with selected provider/model
2. Prepare retriever with `prepare_retriever()` (loads or creates embeddings)
3. Query FAISS retriever for relevant code chunks
4. Construct prompt with retrieved context + conversation history
5. Stream AI response with citations to source files
6. Update conversation memory for multi-turn dialogs

**DeepResearch Feature**:
- Multi-turn research with up to 5 iterations
- Uses specialized prompts: `DEEP_RESEARCH_FIRST_ITERATION_PROMPT`, `DEEP_RESEARCH_INTERMEDIATE_ITERATION_PROMPT`, `DEEP_RESEARCH_FINAL_ITERATION_PROMPT`
- Automatically continues research until conclusion reached
- Maintains research context across iterations

### Frontend Architecture

Next.js app using App Router architecture:

#### Key Pages

- **`src/app/page.tsx`**: Homepage - repository input, configuration, wiki generation trigger
- **`src/app/wiki/[owner]/[repo]/page.tsx`**: Wiki viewer with tree navigation
- **`src/app/api/**/route.ts`**: API route handlers for backend communication

#### Core Components

- **`src/components/ConfigurationModal.tsx`**: Model selection, file filters, generation options
- **`src/components/ProcessedProjects.tsx`**: Shows previously generated wikis with cache management
- **`src/components/WikiTreeView.tsx`**: Hierarchical navigation for wiki sections/pages
- **`src/components/Mermaid.tsx`**: Renders Mermaid diagrams with svg-pan-zoom
- **`src/components/Markdown.tsx`**: Markdown rendering with syntax highlighting
- **`src/components/TokenInput.tsx`**: Secure input for private repository access tokens

#### State Management

- **`src/contexts/LanguageContext.tsx`**: i18n context for multi-language support
- Component-level state with React hooks (useState, useEffect)
- Cache management via localStorage (repo configs, processed projects)

#### Frontend-Backend Communication

- WebSocket for streaming wiki generation: `ws://localhost:8001/ws/generate-wiki`
- HTTP streaming for chat: `POST /chat/completions/stream`
- REST API calls to FastAPI backend on port 8001

## Environment Variables

Required/optional environment variables (create `.env` in project root):

```bash
# LiteLLM (Company Internal - DEFAULT PROVIDER)
LITELLM_API_KEY=<key>          # Company internal LiteLLM API key
LITELLM_BASE_URL=<url>         # Default: https://litellm-internal.123u.com/

# AI Provider API Keys (Optional - for alternative providers)
GOOGLE_API_KEY=<key>           # For Google Gemini + Google AI embeddings
OPENAI_API_KEY=<key>           # For OpenAI models + embeddings
OPENROUTER_API_KEY=<key>       # For OpenRouter models (optional)
AZURE_OPENAI_API_KEY=<key>     # For Azure OpenAI (optional)
AZURE_OPENAI_ENDPOINT=<url>    # Azure endpoint (optional)
AZURE_OPENAI_VERSION=<version> # Azure API version (optional)
AWS_ACCESS_KEY_ID=<key>        # For AWS Bedrock (optional)
AWS_SECRET_ACCESS_KEY=<key>    # For AWS Bedrock (optional)

# Configuration
DEEPWIKI_EMBEDDER_TYPE=openai  # Embedder: openai|google|ollama (default: openai)
OLLAMA_HOST=http://localhost:11434  # Ollama server (default: localhost)
OPENAI_BASE_URL=<url>          # Custom OpenAI endpoint (optional)
DEEPWIKI_CONFIG_DIR=<path>     # Custom config directory (optional)

# Server
PORT=8001                      # API server port (default: 8001)
SERVER_BASE_URL=http://localhost:8001  # API base URL

# Authentication (optional)
DEEPWIKI_AUTH_MODE=true        # Enable auth mode (optional)
DEEPWIKI_AUTH_CODE=<secret>    # Auth code for wiki generation (optional)

# Logging
LOG_LEVEL=INFO                 # Logging level: DEBUG|INFO|WARNING|ERROR
LOG_FILE_PATH=api/logs/application.log  # Log file path
```

## Project-Specific Patterns

### Provider-Based Model Selection

DeepWiki uses a flexible provider system:
- All providers configured in `api/config/generator.json`
- Each provider has a dedicated client class in `api/*_client.py`
- Client classes implement common interface for initialization and streaming
- Providers support both predefined and custom models via `supportsCustomModel` flag
- Frontend sends `provider` and `model` parameters with each request

### RAG Implementation

- Uses AdalFlow's `FAISSRetriever` for vector search
- Custom `Memory` class manages conversation history (fixes AdalFlow's Conversation class bugs)
- Conversation stored as list of `DialogTurn` objects with UUIDs
- Token counting with tiktoken to prevent context overflow (max 7500 tokens)
- Retriever returns top-k relevant documents with similarity scores

### Mermaid Diagram Auto-Fixing

The system automatically detects and fixes common Mermaid syntax errors:
- Malformed node definitions
- Invalid arrow syntax
- Unclosed quotes
- Missing semicolons
- Uses regex patterns and LLM-based repair if needed

### File Filtering System

Repository processing supports inclusion/exclusion filters:
- **Excluded dirs**: Patterns for directories to skip (e.g., `node_modules`, `.git`)
- **Excluded files**: File patterns to ignore (e.g., `*.lock`, `*.min.js`)
- **Included dirs**: Allowlist for specific directories
- **Included files**: Allowlist for specific file patterns
- Configured in `api/config/repo.json` with defaults
- Overridable per-request via frontend configuration

### Caching Strategy

Three levels of caching:
1. **Repository cache**: Cloned repos in `~/.adalflow/repos/<owner>/<repo>/`
2. **Embedding cache**: FAISS indexes in `~/.adalflow/databases/<repo_url_hash>/`
3. **Wiki cache**: Generated wikis in `~/.adalflow/wikicache/<hash>.json`

Cache invalidation via API endpoints or frontend UI.

### Internationalization (i18n)

- Frontend uses `next-intl` for translations
- Language files in `src/messages/<lang>.json`
- Supported: English, Chinese, Japanese, Spanish, Korean, Vietnamese, French, Russian, Portuguese
- Language selection passed to backend for localized wiki generation
- Backend prompts in `api/prompts.py` support language-specific generation

## Common Development Tasks

### Adding a New AI Provider

1. Create client module: `api/new_provider_client.py`
2. Implement streaming interface (see existing clients as reference)
3. Add provider to `api/config.py` CLIENT_CLASSES
4. Configure in `api/config/generator.json`:
   ```json
   "new_provider": {
     "default_model": "model-name",
     "supportsCustomModel": true,
     "models": { "model-name": { "temperature": 0.7 } }
   }
   ```
5. Update frontend `ConfigurationModal.tsx` to include new provider option

### Modifying RAG Behavior

- Retriever configuration: `api/config/embedder.json` → `retriever` section
- Change top_k retrieved documents: modify `top_k` value
- Adjust text chunking: modify `text_splitter` settings (chunk_size, chunk_overlap)
- System prompts: edit `api/prompts.py` → `RAG_SYSTEM_PROMPT`, `RAG_TEMPLATE`

### Customizing Wiki Generation

- Wiki structure prompt: `api/prompts.py` → `WIKI_STRUCTURE_PROMPT`
- Page generation prompt: `api/prompts.py` → `WIKI_PAGE_GENERATION_PROMPT`
- Generation logic: `api/api.py` → `generate_wiki()` function
- Mermaid diagram prompts in same file control visual generation

### Running Tests for Specific Components

```bash
# Test Google embedder
pytest tests/unit/test_google_embedder.py -v

# Test API endpoints (requires running server)
pytest tests/api/test_api.py -v

# Test with specific markers
pytest -m "unit and not slow" -v
pytest -m network -v  # Tests requiring network

# Run with coverage
pytest --cov=api --cov-report=html
```

## Important Notes

- **Embedder consistency**: Once a repository is embedded with a specific embedder (OpenAI/Google/Ollama), stick with it. Switching embedders requires re-embedding (different vector spaces).
- **Token limits**: OpenAI embeddings have 8192 token limit. Code is automatically chunked to stay within limits.
- **FAISS indexes**: Not compatible across different embedding dimensions. Deleting cache required when changing embedder types.
- **Private repos**: Require personal access tokens with `repo` scope (GitHub) or equivalent permissions (GitLab/BitBucket).
- **WebSocket vs HTTP streaming**: Both supported for chat. WebSocket preferred for wiki generation (better real-time updates).
- **Model context windows**: Different models have different context limits. Configure wisely to avoid truncation.
- **Logging**: All modules use Python's logging module. Set `LOG_LEVEL=DEBUG` for verbose output during development.
- **AdalFlow dependency**: The project uses AdalFlow framework for RAG/embeddings. Custom patches applied (see `api/ollama_patch.py` and custom Memory class in `rag.py`).

## Useful File Locations

- Main API routes: `api/api.py`
- WebSocket handlers: `api/websocket_wiki.py`
- RAG implementation: `api/rag.py`
- Repository processing: `api/data_pipeline.py`
- Prompts: `api/prompts.py`
- Frontend homepage: `src/app/page.tsx`
- Wiki viewer: `src/app/wiki/[owner]/[repo]/page.tsx`
- Configuration files: `api/config/*.json`
- Test directory: `tests/` (with separate unit/integration/api folders)
