<p align="center">
  <img src="./logo.png" alt="i-have-adhd" width="140" />
</p>

# i-have-adhd-zh-cn

答案先行，少些空话，把事情做完。

面向 AI 编程助手的简体中文 Agent Skill。让回复更容易扫读、开始行动和跟上进度；适用于编程、排错、解释和日常交流。使用这种风格不代表你有 ADHD，也不能用于诊断或治疗。

## 安装

```bash
npx skills add matrixji/i-have-adhd-zh-cn --skill i-have-adhd-zh-cn
```

本项目使用标准 Skill 格式，无需安装平台插件。全局安装、本地安装、持续应用、更新和移除方法见 [INSTALL.md](INSTALL.md)。仓库发布前可从本地路径安装。

## 回复会怎样变化

修改前：

> 这是一个很好的问题！让我分析一下。你的认证流程涉及中间件、token 验证和 cookie 处理。`src/auth.ts` 中的 `verifyToken` 可能使用了旧版 API。你可以考虑更新它，然后运行测试。顺便说一句，也可以检查其他依赖。希望这对你有帮助！

修改后，假设助手确实完成了编辑和测试：

> 已更新 `src/auth.ts` 的 `verifyToken`，认证测试全部通过。
>
> - 按项目锁定的依赖版本调整 token 验证。
> - `npm test -- auth.spec.ts`：12 项通过。

这是回复风格示例，不是本仓库的执行记录。助手有工具和权限时应完成工作；不能执行时，应明确说明限制和真正需要你处理的步骤。

## 核心规则

- **答案先行**：直接回答，执行后用结果开头。
- **自然简体中文**：代码、命令、路径、API 和错误原文保持不变。
- **减少执行负担**：助手完成权限范围内的工作，只留下必要的用户操作。
- **进度可见**：如实区分已修改、已验证和仍受阻的事项。
- **完整且准确**：保留详解、取舍、安全信息与指定格式，不为简短而漏项。

完整规则见 [SKILL.md](skills/i-have-adhd-zh-cn/SKILL.md)。启用后本次会话持续应用；说“关闭 ADHD 模式”可退出。是否自动加载由宿主决定，见[持续应用](INSTALL.md#持续应用)。

## 来源与范围

本项目基于 [ayghri/i-have-adhd](https://github.com/ayghri/i-have-adhd)，参考 [panda850819/i-have-adhd-zh-tw](https://github.com/panda850819/i-have-adhd-zh-tw) 的独立 Skill、本地化文档与验证方式。原始设计归功于 Ayoub Ghriss 及上游贡献者；繁体版的本地化实践归功于其维护者。

这是非官方简体中文衍生版本。与繁体版一样，本项目只提供标准 Skill，不提供上游的 Claude/Codex 插件市场、钩子、Cursor 镜像或其他运行时扩展。需要这些集成时，请使用原版；不要在同一会话同时启用互相冲突的回复风格。

上游历史保留在 Git 中，已审查的版本记录在 [docs/upstream.json](docs/upstream.json)。同步和迁移原则见 [docs/upstream.md](docs/upstream.md)。

## 验证

```bash
python3 scripts/check_repo.py
python3 -m unittest discover -s tests -v
python3 scripts/run_evals.py validate
python3 scripts/run_scenario_eval.py validate evals/scenarios/persistence-topic-switch-stop
```

静态检查和单元测试不会调用付费模型，也不能证明真实模型一定遵守规则。单轮评测、多轮持续性评测与评分办法见 [evals/README.md](evals/README.md)。

## 许可与致谢

沿用 [MIT License](LICENSE)，完整保留 `Copyright (c) 2026 Ayoub Ghriss`。繁体版参考文件中的贡献按 MIT 条件使用；简体版新增与修改由本项目维护者负责。

上游概念参考 J. Russell Ramsay 与 Anthony L. Rostain 的 *The Adult ADHD Tool Kit*，并调整为适用于语言模型的回复规则。该书及其内容不包含在本仓库的 MIT 授权范围内。
