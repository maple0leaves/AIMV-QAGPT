# Open WebUI + Ollama（`qwen3-vl:32b`）慢响应排查与优化记录

## 1. 问题现象

- 使用 Open WebUI 通过 Ollama 调用 `qwen3-vl:32b`。
- 单轮问答经常需要 1-2 分钟。
- 典型表现：首次特别慢，连续对话也明显卡顿。

## 2. 根因分析

### 2.1 上下文窗口过大（核心原因）

`qwen3-vl:32b` 默认 `context length` 为 `262144`。  
该值会显著抬高 KV cache 占用，导致：

- 显存压力极大；
- 部分计算/缓存落到 CPU；
- 生成速度显著下降。

### 2.2 RAG/Embedding 与主模型竞争显存（次要但明显）

当 `rag.embedding_engine=ollama` 且 embedding 模型也走 Ollama 时，聊天过程中可能触发 `/api/embed`。  
在大模型显存本就紧张的情况下，容易出现模型装载/驱逐切换，进一步拉长耗时。

### 2.3 冷启动加载成本高

`qwen3-vl:32b` 本身较大，冷启动加载时间不可避免。  
若 `keep_alive` 较短或模型频繁被挤出显存，会反复支付这段加载成本。

## 3. 已实施的优化

## 3.1 新增 Ollama 低延迟启动脚本

新增文件：`backend/dev-ollama.sh`

默认参数：

- `OLLAMA_CONTEXT_LENGTH=8192`
- `OLLAMA_KEEP_ALIVE=30m`
- `OLLAMA_NUM_PARALLEL=1`
- `OLLAMA_MAX_LOADED_MODELS=1`
- `OLLAMA_FLASH_ATTENTION=true`

作用：限制上下文窗口、减少并发/多模型抢占、尽量维持热加载。

## 3.2 优化 WebUI 启动脚本提示

更新文件：`backend/dev.sh`

- 保留原有启动行为；
- 增加提示，提醒使用 `./dev-ollama.sh` 启动 Ollama 优化参数。

## 3.3 写入模型默认参数（数据库）

已更新 `backend/data/webui.db` 中模型参数：

- `qwen3-vl:32b` -> `num_ctx=8192`, `num_predict=1024`
- `qwen3-vl32bte` -> 保留原 `system`，并追加 `num_ctx=8192`, `num_predict=1024`

作用：避免每次在 UI 手动调参。

## 3.4 `num_predict` 和 `num_ctx` 要在哪里修改

可按以下 3 种方式修改，按优先级推荐如下：

### A. 模型级（推荐）- Open WebUI 模型编辑页

适用场景：希望该模型长期默认使用某组参数。

- 进入 `Workspace -> Models -> Edit Model`；
- 在 `Model Params -> Advanced Params` 中修改：
  - `Context Length` = `num_ctx`
  - `Max Tokens (num_predict)` = `num_predict`
- 保存模型后，对该模型会持续生效。

界面确认（你截图对应关系）：

- 红框中的 `Context Length` 就是 `num_ctx`；
- 红框中的 `Max Tokens (num_predict)` 就是 `num_predict`；
- 同一页下方出现 `Prompt suggestions`，通常表示你在“模型编辑页”，不是会话临时设置页。

推荐值（速度/长度平衡）：

- `num_ctx=8192`
- `num_predict=1024`

### B. 会话级（临时）- 聊天界面高级参数

适用场景：临时测试，不想改模型默认值。

- 在聊天页面打开“高级参数”；
- 同样可修改 `Context Length`（`num_ctx`）和 `Max Tokens (num_predict)`。

说明：该方式通常只对当前会话或当前聊天参数生效，优先级高于模型默认值。

### C. Ollama 服务级（全局）- 启动脚本环境变量

适用场景：希望从 Ollama 服务层面限制/约束默认上下文。

- 文件：`backend/dev-ollama.sh`
- 关键项：`OLLAMA_CONTEXT_LENGTH=8192`

说明：

- 该方式主要影响上下文窗口（`num_ctx`）的全局默认行为；
- 修改后需重启 `./dev-ollama.sh` 才会生效。

## 4. 标准启动流程（推荐）

在两个终端中分别执行：

### 终端 A：启动 Ollama（优化参数）

```bash
cd /home/te/te/TE/open-webui-main/open-webui-main/backend
./dev-ollama.sh
```

### 终端 B：启动 Open WebUI

```bash
cd /home/te/te/TE/open-webui-main/open-webui-main/backend
./dev.sh
```

> 注意：启动前请先停止旧的 `ollama serve`，避免新旧参数混用。

## 5. 验证方法

## 5.1 验证 Ollama 启动参数是否生效

查看启动日志中是否出现：

- `OLLAMA_CONTEXT_LENGTH:8192`
- `OLLAMA_KEEP_ALIVE:30m`

## 5.2 验证模型参数是否生效

在 Open WebUI 选择对应模型后，检查高级参数中的：

- `num_ctx = 8192`
- `num_predict = 1024`

## 5.3 验证时延变化

预期表现：

- 首次请求（冷启动）明显快于原先配置；
- 连续请求（热启动）进一步下降到数秒到十几秒量级（与提示词长度、输出长度、是否触发检索相关）。

## 6. 进一步优化建议（可选）

若仍希望更快，可按顺序尝试：

1. `num_ctx` 从 `8192` 降到 `4096`；
2. `num_predict` 从 `1024` 按需调整到 `768` 或 `512`；
3. 纯文本问答尽量使用非 VL 模型；
4. 非必要时关闭 RAG/Embedding 或避免与大模型共用同一 Ollama 实例。

## 7. 回滚方案

如需回退到默认行为：

1. 不使用 `./dev-ollama.sh`，改为普通 `ollama serve`；
2. 在模型参数中删除/还原 `num_ctx`、`num_predict`；
3. 或恢复数据库中模型参数为原值（备份后再操作）。

## 8. 经验结论

对于 `qwen3-vl:32b`，性能调优优先级通常为：

1. 先控制 `num_ctx`；
2. 再控制 `num_predict`；
3. 最后处理多模型竞争（embedding/rerank/chat）。

这三步通常能把“分钟级等待”降到“秒级到十几秒”。
