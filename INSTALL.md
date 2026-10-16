# 安装 i-have-adhd-zh-cn

使用标准 Agent Skill 格式，通过 [skills CLI](https://github.com/vercel-labs/skills) 安装；不需要插件市场、后台钩子或运行时扩展。

## 从 GitHub 安装

仓库发布后，安装到当前项目：

```bash
npx skills add matrixji/i-have-adhd-zh-cn --skill i-have-adhd-zh-cn
```

安装到用户全局目录：

```bash
npx skills add matrixji/i-have-adhd-zh-cn --skill i-have-adhd-zh-cn -g
```

按 CLI 提示选择目标助手和安装方式。安装后打开新会话，让宿主重新发现 Skill。

## 从本地仓库安装

在要使用 Skill 的项目中执行，将路径替换为本仓库的实际位置：

```bash
npx skills add /path/to/i-have-adhd-zh-cn/skills/i-have-adhd-zh-cn
```

这里直接指向公开 Skill 子目录，避免扫描本地开发工具。也可把该目录完整复制到宿主支持的 skills 目录；请同时保留目录内的 `LICENSE`。手动复制的安装需要手动更新或移除。

## 检查安装

列出远程仓库可用的 Skill，不执行安装：

```bash
npx skills add matrixji/i-have-adhd-zh-cn --list
```

应包含 `i-have-adhd-zh-cn`。列出当前项目已安装的 Skill：

```bash
npx skills list
```

检查全局安装时使用 `npx skills list -g`。

## 持续应用

安装后，在对话中明确要求：

```text
使用 i-have-adhd-zh-cn Skill；本次会话持续应用，直到我说“关闭 ADHD 模式”。
```

Skill 被加载后要求本次会话持续应用；实际发现、加载和上下文保留机制由宿主决定。它不会自动修改全局配置，也不能保证每个新会话都会加载。

如果希望每个会话都应用，可自行在宿主的项目或用户指令文件中加入：

```text
每次回复都使用已安装的 i-have-adhd-zh-cn Skill。
```

在已支持 `AGENTS.md` 的环境中，可将这一行放进项目的 `AGENTS.md`。如果加入了常驻指令，停用时也要移除该行，避免后续会话重新启用。

## 更新与移除

通过 CLI 安装的项目级 Skill：

```bash
npx skills update i-have-adhd-zh-cn -p
npx skills remove i-have-adhd-zh-cn
```

全局安装：

```bash
npx skills update i-have-adhd-zh-cn -g
npx skills remove i-have-adhd-zh-cn -g
```

这些命令管理已安装的副本。维护这个简体仓库、迁移英文上游属于另一项工作，见[上游同步说明](docs/upstream.md)。

## 常见问题

**找不到 Skill**：确认安装或列出的名称是 `i-have-adhd-zh-cn`，并打开新会话。仓库尚未推送时使用本地路径安装。

**仍回复英文**：确认宿主加载的是 `skills/i-have-adhd-zh-cn/SKILL.md`，检查是否同时启用了原版或其他语言规则。用户明确指定英文或固定输出格式时，本 Skill 会遵从该要求。

**没有持续应用**：使用上面的明确启用指令；需要常驻时按宿主支持的方法加入指令文件。仅安装成功不代表每轮一定自动加载。
