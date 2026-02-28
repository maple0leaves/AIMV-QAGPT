# AIMVQAGPT 启动命令速查

本文档用于快速启动 AIMVQAGPT 项目的关键进程：

- Ollama（模型服务）
- Backend（FastAPI）
- Frontend（Vite 开发服务器）

## 0) 一条命令启动（Docker Compose，推荐给其他用户）

从 GitHub 克隆后，一条命令即可启动（含 Ollama + WebUI）：

```bash
git clone https://github.com/maple0leaves/AIMVQAGPT.git
cd AIMVQAGPT
docker compose up --build
```

启动完成后访问 `http://localhost:3000`。首次构建约需 5–15 分钟，后续启动可省略 `--build`。

## 1) 推荐启动顺序（3 个终端，开发模式）

### 终端 A：启动 Ollama（优化参数）

```bash
cd /home/te/te/TE/open-webui-main/open-webui-main/backend
./dev-ollama.sh
```

### 终端 B：启动后端

```bash
cd /home/te/te/TE/open-webui-main/open-webui-main/backend
./dev.sh
```

### 终端 C：启动前端

```bash
cd /home/te/te/TE/open-webui-main/open-webui-main
npm install
npm run dev
```

说明：

- `npm install` 只需要首次执行，或依赖变更后执行。
- 默认情况下，前端会跑在 `5173` 端口（Vite）。

## 2) 默认访问地址

- Ollama: `http://127.0.0.1:11434`
- Backend: `http://127.0.0.1:8080`
- Frontend: `http://127.0.0.1:5173`

访问说明：

- 日常使用时，请访问后端地址：`http://127.0.0.1:8080`
- `http://127.0.0.1:5173` 主要用于前端开发调试

## 3) 常用健康检查命令

在任意终端执行：

```bash
curl http://127.0.0.1:11434/api/version
curl http://127.0.0.1:11434/api/tags
curl http://127.0.0.1:8080/health
```

## 4) 常用端口/参数覆盖

### 后端改端口

```bash
cd /home/te/te/TE/open-webui-main/open-webui-main/backend
PORT=8081 ./dev.sh
```

### Ollama 临时覆盖参数

```bash
cd /home/te/te/TE/open-webui-main/open-webui-main/backend
OLLAMA_CONTEXT_LENGTH=8192 OLLAMA_KEEP_ALIVE=30m ./dev-ollama.sh
```

### 前端改端口

```bash
cd /home/te/te/TE/open-webui-main/open-webui-main
npm run dev -- --port 5050
```

## 5) 停止服务

在每个运行中的终端按一次 `Ctrl + C` 即可。
