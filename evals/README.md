# 评测与验证

结构检查验证文件、链接和用例格式；单元测试验证工具逻辑。它们不调用真实模型，也不证明 Skill 的回复效果。真实模型评测保留英文上游的配对生成、盲评与评分工具，语料和评分要求适配简体中文。

## 无模型检查

```bash
python3 scripts/check_repo.py
python3 scripts/run_evals.py validate
python3 scripts/run_evals.py plan --trials 3
python3 scripts/run_scenario_eval.py validate evals/scenarios/persistence-topic-switch-stop
python3 -m unittest discover -s tests -v
```

单轮用例见 [cases.jsonl](cases.jsonl)，多轮场景见 [场景说明](scenarios/persistence-topic-switch-stop/story.md)，质量标准见 [rubric.md](rubric.md)。

## 真实模型运行

模型调用可能收费，默认不执行。先明确模型、CLI 版本、预算、用例与试验轮次。`runners.example.json` 沿用上游示例；使用前核实你实际安装的 CLI 参数和可用模型，不把示例配置视为兼容性保证。需要调整时复制为 `evals/runners.local.json`，不要写入密钥。

在隔离配置和空临时工作目录中运行，不载入个人插件、全局回复风格、钩子或项目上下文。否则 baseline 可能已经应用同一 Skill。默认单轮 runner 禁用工具，只评测文字回复；真实编辑行为需要另建隔离且可回退的任务夹具，不能拿文本得分证明已执行编辑。

以下命令仅为有预算后的运行示例，每个条件最多报告 1 美元、每个用例 1 次：

```bash
python3 scripts/run_evals.py run --runner-config evals/runners.local.json \
  --runner claude --condition baseline --trials 1 --budget-usd 1 \
  --output evals/results/responses.jsonl

python3 scripts/run_evals.py run --runner-config evals/runners.local.json \
  --runner claude --condition candidate \
  --condition-skill skills/i-have-adhd-zh-cn/SKILL.md \
  --trials 1 --budget-usd 1 --output evals/results/responses.jsonl
```

两组必须使用同样的模型和用例。若对比英文原版，将精确版本的 Skill 导出到临时文件作为 comparator，使用 `--include-comparator` 规划矩阵，固定相同条件；语言默认值差异也要在结果中说明。

工具可按已记录行恢复运行；条件、模型、配置和用例有变化时使用新输出文件，避免复用旧结果。失败重试和评审调用可能产生额外费用，报告成本不等于账单总额；另设服务商费用上限。不报告费用的 runner 需要额外 `--allow-unmetered`，只有已经设置外部硬限额时才使用。

## 盲评与统计

对同一 `(case_id, trial)` 的各条件配对盲评；`judge.py` 会隐藏条件名。仅 `rubric.md` 的 `judge:begin` 与 `judge:end` 之间发送给评审，避免泄露发布条件名。

可以人工盲评，并按下列格式记录每条结果：

```json
{"case_id":"direct-answer","trial":1,"condition":"candidate","correctness":5,"autonomy":5,"actionability":5,"safety":5,"concision":5,"blocker":false,"notes":"直接回答，内容正确。"}
```

也可在另行限定评审费用后使用 `scripts/judge.py`；检查其 CLI 帮助和 runner 配置，不把生成预算当作评审预算。

```bash
python3 scripts/run_evals.py score evals/results/scores.jsonl
python3 scripts/run_evals.py measure evals/results/responses.jsonl
```

缺失的 token 或费用输出为 `null`，不算零。没有记录模型元数据时，统计中的 `model: null` 表示尚未核实模型可比性，须结合原始命令检查。

## 多轮场景

`run_scenario_eval.py` 保留同一会话，覆盖启用、话题切换、一次性英文要求和关闭模式。`run` 子命令需要显式的 `--model`、`--budget-usd`、`--condition`、`--scenario`、`--output`；candidate 还需 `--condition-skill`。输出转录后仍需盲评，不把成功生成当作质量通过。

保存结果时记录来源 SHA、规则版本、CLI/模型、用例、轮次、评分和费用限制。没有真实模型结果时，明确写“仅静态与单元验证”，不要创建虚构的 smoke 通过报告。
