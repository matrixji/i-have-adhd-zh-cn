# 简体中文版维护指南

本仓库基于 `ayghri/i-have-adhd`，参考 `panda850819/i-have-adhd-zh-tw`，只发布标准简体中文 Skill。

## 文件地图

- `skills/i-have-adhd-zh-cn/SKILL.md`：公开规则的唯一来源。
- `skills/i-have-adhd-zh-cn/LICENSE`：随 Skill 分发的原始许可，须与根目录一致。
- `README.md`、`INSTALL.md`：定位与安装，不宣称提供插件或常驻钩子。
- `docs/upstream.json`、`docs/upstream.md`：已审查的来源版本及同步原则。
- `scripts/`、`tests/`、`evals/`：结构检查、复用的上游评测工具和简体中文用例。

修改前阅读目标文件及相关测试。公开 Skill 默认用自然简体中文，保留技术原文、用户指定格式、任务完整性和宿主权限边界。不要机械简繁转换，也不要把台湾用词规则直接搬到简体版。

## 维护约定

1. 英文上游是规则与通用评测工具的来源；繁体版只作本地化和验证方法参考。
2. 不整仓覆盖或自动合并上游。先比较旧基线、新版本和本地内容，再按文件与语义迁移，详见 `docs/upstream.md`。
3. 维护用 Skills 位于项目本地 `.agents/skills/`，不得暂存、提交或作为公开 Skill 打包。公开产品仍放在 `skills/i-have-adhd-zh-cn/`。
4. 若本地存在 `.agents/skills/sync-adhd-upstream/SKILL.md`，上游同步任务先读取它；新克隆没有该文件时按 `docs/upstream.md` 执行即可。
5. 只报告实际执行的验证；结构测试不等于模型行为评测。模型调用需要明确的模型、隔离方式和费用预算，不默认运行。

## 检查

```bash
python3 scripts/check_repo.py
python3 -m unittest discover -s tests -v
python3 scripts/run_evals.py validate
python3 scripts/run_scenario_eval.py validate evals/scenarios/persistence-topic-switch-stop
git diff --check
```

贡献说明见 [CONTRIBUTING.md](CONTRIBUTING.md)。不要推送、发布或替用户安装全局配置，除非任务包含这些操作。
