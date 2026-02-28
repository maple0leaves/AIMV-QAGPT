# AIMVQAGPT

**AIMVQAGPT** (AI-powered Medical Visual Question Answering GPT) 是一个基于 [Open WebUI](https://github.com/open-webui/open-webui) 二次开发的 AI 平台，支持多种 LLM（如 Ollama、OpenAI 兼容 API），内置 RAG 检索增强生成能力。

## 快速开始

确保已安装 [Docker](https://docs.docker.com/get-docker/)，然后执行：

```bash
git clone https://github.com/maple0leaves/AIMVQAGPT.git
cd AIMVQAGPT
docker compose up --build
```

启动完成后访问 [http://localhost:3000](http://localhost:3000)。

> 首次构建约需 5–15 分钟（需下载依赖并编译前端），后续启动可省略 `--build`。

## 主要功能

- **Ollama / OpenAI API 集成**：支持 Ollama 本地模型及 OpenAI 兼容 API
- **RAG 检索增强生成**：支持上传文档并在对话中引用
- **Web 搜索集成**：支持 SearXNG、Google PSE、DuckDuckGo 等搜索引擎
- **图像生成**：支持 AUTOMATIC1111、ComfyUI、DALL-E 等
- **多模型并行对话**：同时使用多个模型获取最优回答
- **权限管理 (RBAC)**：细粒度的角色和权限控制
- **多语言支持**：内置国际化 (i18n) 支持
- **响应式设计**：适配桌面、笔记本和移动设备
- **PWA 支持**：支持安装为移动端 App

## 开发模式

如需进行本地开发调试，请参考 [启动命令速查](docs/STARTUP_COMMANDS.md)。

## 许可证

本项目基于 [BSD-3-Clause License](LICENSE) 开源。

## 致谢

本项目基于 [Open WebUI](https://github.com/open-webui/open-webui)（由 [Timothy Jaeryang Baek](https://github.com/tjbck) 创建）进行二次开发，感谢原作者和社区的贡献。
