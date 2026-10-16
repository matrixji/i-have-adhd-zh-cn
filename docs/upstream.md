# 上游同步与迁移

英文来源是 [ayghri/i-have-adhd](https://github.com/ayghri/i-have-adhd)，本地化方法参考 [panda850819/i-have-adhd-zh-tw](https://github.com/panda850819/i-have-adhd-zh-tw)。已审查的完整提交 SHA 记录在 [upstream.json](upstream.json)；它表示已审查到该版本，不表示照搬其全部内容。

## 保留与取舍

| 来源内容 | 简体版处理方式 |
| --- | --- |
| 英文 `skills/i-have-adhd/SKILL.md` | 按语义迁移到 `skills/i-have-adhd-zh-cn/SKILL.md`，保留最新规则意图 |
| 繁体中文 Skill、文档、结构验证方式 | 作为参考，重新编写自然简体中文，不机械转换或继承地区禁词 |
| 英文 `scripts/run_evals.py`、`judge.py`、`run_scenario_eval.py` 及对应测试 | 保留通用评测工具；新增本地结构验证，使用简体中文用例和评分说明 |
| `README.md`、`INSTALL.md`、贡献与维护说明 | 按本仓库定位维护，安装目标始终是 `matrixji/i-have-adhd-zh-cn` |
| 插件清单、marketplace、钩子、Cursor 镜像、Pi/OMP/OpenCode 扩展、多语言文档 | 不随简体版分发；上游增加集成时先评估，不自动恢复 |
| `LICENSE`、`logo.png` | 保留来源与版权；Skill 目录携带相同许可 |

原版侧重“下一步行动”；简体版参考繁体版，区分直接回答、助手执行和真正需要用户操作的情况。保留明确结果、工具范围内自主完成、持续生效、完整性优先、不编造时间或验证结果等约束。

## 同步步骤

1. 确认工作区状态，保留用户未提交的修改。检查并按需配置两个只读来源 remote：`upstream` 与 `reference-zh-tw`，地址以 `upstream.json` 为准，`origin` 保持为自己的仓库。
2. 获取来源分支。比较基线与新提交的整仓文件清单、提交日志及关键文件差异，检查新增、删除和重命名。来源回退或改写历史时先说明差异，不能直接把基线前移。
3. 对每项变化记录“迁移、改写、已有等效内容、暂不采用”及原因。按旧上游、新上游、本地三方对照修改；英文是规则来源，繁体版是参考。不可用新上游整仓覆盖，也不可把两个来源的同一改动重复应用。
4. 更新受影响的规则、示例、用例、评分和文档。运行 [AGENTS.md](../AGENTS.md#检查) 的检查，核对版权、安装命令、技术原文与本地 Skill 的排除状态。必要的模型评测单独说明预算、配置与结果。
5. 所有新提交已审查且迁移后的本地检查通过后，才更新对应的 `reviewed_commit`，在本文件记录重要取舍。还有未审查内容时保留旧基线。提交和推送按当前任务授权执行。

同步时可先读取精确版本的原文：

```bash
git show upstream/main:skills/i-have-adhd/SKILL.md
git show reference-zh-tw/main:skills/i-have-adhd-zh-tw/SKILL.md
```

旧版本使用 `upstream.json` 中相应的完整 SHA。同步不是简单的简繁转换，也不保证两边规则逐字相同。

## 本地维护 Skill

项目本地的 `.agents/skills/sync-adhd-upstream/SKILL.md` 提供上述工作流与差异报告脚本。它不随仓库发布；通过 `.git/info/exclude` 本地排除，不改变公开产品的安装范围。新克隆没有它时，仍可使用本文完成同步。

## 初始迁移记录

基于 `upstream.json` 记录的两份版本创建简体版，保留英文上游 Git 历史及通用评测工具。参考繁体版的标准 Skill 分发方式和回答优先原则，重写简体中文规则、安装说明和评测语料。明确区分会话内持续生效与宿主自动加载，不承诺标准 Skill 能替代后台钩子。
