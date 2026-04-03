以下是 **AIMV-QAGPT** 项目的完整结构概览。该项目是一套基于 [Open WebUI](https://github.com/open-webui/open-webui) 二次开发的 **企业级本地化 RAG 智能问答系统**，采用典型的 **前后端分离** 架构：前端使用 **SvelteKit + TailwindCSS**，后端使用 **Python (FastAPI)**，通过 **Docker Compose** 编排部署。

---

## 📁 项目根目录结构

```
AIMV-QAGPT/
├── 📂 backend/                  # 🔧 后端（Python / FastAPI）
├── 📂 src/                      # 🎨 前端（SvelteKit）
├── 📂 cypress/                  # 🧪 E2E 测试（Cypress）
├── 📂 test/                     # 🧪 测试相关
├── 📂 docs/                     # 📖 文档
├── 📂 kubernetes/               # ☸️ Kubernetes / Helm 部署配置
├── 📂 scripts/                  # 📜 辅助脚本
├── 📂 static/                   # 🖼️ 静态资源
│
├── Dockerfile                   # Docker 镜像构建文件
├── docker-compose.yaml          # 主 Docker Compose 配置
├── docker-compose.gpu.yaml      # GPU 支持配置
├── docker-compose.amdgpu.yaml   # AMD GPU 支持配置
├── docker-compose.api.yaml      # API 模式配置
├── docker-compose.data.yaml     # 数据持久化配置
├── docker-compose.a1111-test.yaml
├── docker-compose.playwright.yaml
├── Caddyfile.localhost          # Caddy 反向代理配置
│
├── package.json                 # 前端 npm 依赖
├── package-lock.json
├── pyproject.toml               # 后端 Python 项目配置 (uv/hatch)
├── uv.lock                      # Python 依赖锁定文件
├── hatch_build.py               # 构建钩子
│
├── svelte.config.js             # SvelteKit 配置
├── vite.config.ts               # Vite 构建配置
├── tailwind.config.js           # TailwindCSS 配置
├── tsconfig.json                # TypeScript 配置
├── postcss.config.js            # PostCSS 配置
├── cypress.config.ts            # Cypress 测试配置
├── i18next-parser.config.ts     # i18n 翻译提取配置
│
├── Makefile                     # 常用命令快捷入口
├── run.sh                       # 启动脚本
├── run-compose.sh               # Docker Compose 启动脚本
├── run-ollama-docker.sh         # Ollama 容器启动脚本
├── update_ollama_models.sh      # Ollama 模型更新脚本
├── confirm_remove.sh            # 确认删除脚本
│
├── README.md                    # 项目说明
├── LICENSE                      # BSD-3-Clause 许可证
├── .gitignore
├── 指标1.png                    # 指标截图
└── 指标2.png                    # 指标截图
```

---

## 🔧 `backend/` — 后端（Python / FastAPI）

```
backend/
├── open_webui/                  # 核心后端 Python 包
│   ├── __init__.py
│   ├── main.py                  # 🚀 FastAPI 应用入口（46KB，核心文件）
│   ├── config.py                # ⚙️ 配置管理（74KB，超大配置文件）
│   ├── constants.py             # 常量定义
│   ├── env.py                   # 环境变量处理
│   ├── functions.py             # Function Calling 功能
│   ├── tasks.py                 # 后台任务
│   ├── alembic.ini              # 数据库迁移配置
│   │
│   ├── 📂 routers/             # 🛣️ API 路由层
│   ├── 📂 models/              # 📊 数据模型（ORM）
│   ├── 📂 migrations/          # 🔄 数据库迁移脚本（Alembic）
│   ├── 📂 retrieval/           # 🔍 RAG 检索模块
│   ├── 📂 utils/               # 🔨 工具函数
│   ├── 📂 internal/            # 内部模块
│   ├── 📂 socket/              # 🔌 WebSocket 通信
│   ├── 📂 storage/             # 💾 存储管理
│   ├── 📂 static/              # 后端静态文件
│   └── 📂 test/                # 后端单元测试
│
├── 📂 batch_pdfs/              # 📄 批量 PDF 处理
├── requirements.txt             # Python 依赖
├── dev.sh                       # 开发启动脚本
├── dev-ollama.sh                # 带 Ollama 的开发启动脚本
├── start.sh                     # 生产启动脚本
└── start_windows.bat            # Windows 启动脚本
```

---

## 🎨 `src/` — 前端（SvelteKit + TailwindCSS）

```
src/
├── app.html                     # HTML 入口模板
├── app.css                      # 全局样式
├── app.d.ts                     # TypeScript 类型声明
├── tailwind.css                 # Tailwind 入口
│
├── 📂 lib/                     # 核心前端库
│   ├── index.ts
│   ├── constants.ts             # 前端常量
│   ├── dayjs.js                 # 日期处理
│   ├── emoji-groups.json        # Emoji 数据
│   ├── emoji-shortcodes.json
│   │
│   ├── 📂 apis/                # 🌐 API 请求封装
│   ├── 📂 components/          # 🧩 UI 组件（Svelte）
│   ├── 📂 stores/              # 🗄️ 状态管理（Svelte Store）
│   ├── 📂 types/               # 📝 TypeScript 类型定义
│   ├── 📂 utils/               # 🔨 工具函数
│   ├── 📂 i18n/                # 🌍 国际化翻译文件
│   ├── 📂 pyodide/             # 🐍 浏览器端 Python 运行时
│   └── 📂 workers/             # 👷 Web Worker
│
└── 📂 routes/                  # 📄 SvelteKit 路由/页面
```

---

## 🏗️ 架构总结


| 层级         | 技术栈                            | 说明                            |
| ---------- | ------------------------------ | ----------------------------- |
| **前端**     | SvelteKit + TailwindCSS + Vite | 响应式 Web UI，支持 PWA             |
| **后端**     | Python + FastAPI               | REST API + WebSocket，RAG 检索增强 |
| **LLM 集成** | Ollama / OpenAI API            | 本地模型与云端 API 双支持               |
| **数据库**    | SQLAlchemy + Alembic           | ORM + 数据库迁移管理                 |
| **部署**     | Docker Compose / Kubernetes    | 容器化部署，支持 GPU/AMD GPU          |
| **反向代理**   | Caddy                          | 本地开发反代配置                      |
| **测试**     | Cypress + Playwright           | E2E 端到端测试                     |
| **国际化**    | i18next                        | 多语言支持                         |


这个项目本质上是在 **Open WebUI** 的基础上，针对 TE Connectivity 的 AIMV 技术文档场景进行了定制化开发，重点强化了 **RAG 检索增强生成**和 **Function Calling** 能力，实现了企业级本地化部署的智能问答系统。

---

