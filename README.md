# AIMVQAGPT

**AIMVQAGPT** (AI Machine Vision Q&A GPT ) 是一套企业级本地化 RAG 智能问答系统， 目的是解决TE Connectivity 的AIMV 技术文档查询依赖人工翻阅（平均 30 分钟/次），跨部门技术支持响应超 1 天，且受数据合规与私有化部署的硬性约束等问题。

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
**功能演示**移步个人B站视频：[AIMVQAGPT功能演示]()
- **Ollama / OpenAI API 集成**：支持 Ollama 本地模型及 OpenAI 兼容 API
- **RAG 检索增强生成**：支持上传文档并在对话中引用
- **Function Calling**：可为模型绑定自定义工具（如 Web 搜索等），由 LLM 自动选择并调用
- **多模型并行对话**：同时使用多个模型获取最优回答
- **权限管理 (RBAC)**：细粒度的角色和权限控制
- **多语言支持**：内置国际化 (i18n) 支持
- **响应式设计**：适配桌面、笔记本和移动设备

- **PWA 支持**：支持安装为移动端 App

## 开发模式

如需进行本地开发调试，请参考 [启动命令速查](docs/STARTUP_COMMANDS.md)。

## 参考

[openwebui](https://github.com/open-webui/open-webui)

## 许可证

本项目基于 [BSD-3-Clause License](LICENSE) 开源。

