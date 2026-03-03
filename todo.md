1.manim code 对齐
“API 对齐（API grounding）”。
我的建议很明确：不要用长期记忆来解决，而是用 “可执行的规则 + 自动校验 + 约束式生成” 来解决。长期记忆最多只能做补充（存常用模板），但不能当主机制——因为幻觉是“模型概率行为”，记忆并不能保证它不编函数。

下面给你一个在你项目里最稳的实现方案（按效果从强到弱）。

结论先讲
✅ 最推荐的形式（强约束）

Manim API 规则（可版本化的文档/文件）：manim_rules.md / manim_api_allowlist.json

静态校验工具节点：import check + AST 扫描 + signature check

失败就走“修复节点”（你已有），但修复 prompt 里强制引用规则文件

⚠️ 长期记忆能做什么？

存“你们的风格模板/常用 Scene skeleton/常见 bug 修复 pattern”

不适合存“Manim API 规则”当真理来源（版本更新会让记忆变旧）

为什么“规则”要做成文件，而不是记忆

可审计：你可以 review、diff、版本控制（git）

可更新：Manim 升级只需要更新一份规则

可注入：每次生成时把规则作为 system context / reference 给模型

可被工具消费：校验器能读 allowlist 做 AST 检查

记忆做不到这些。

你可以用的三种“规则形态”（建议组合用）
形态 A：Markdown 规则手册（给 LLM 看）

manim_rules.md 内容结构建议：

Allowed imports（统一 from manim import * 或指定子集）

禁止用的函数/类（例如你们经常幻觉出来的）

常用模式（Axes/NumberPlane/ValueTracker/always_redraw）

你们的工程约束（输出路径、Scene class naming、分辨率等）

“如果你不确定 API，宁可用更原始的写法”（fallback patterns）

优点：最容易落地；直接塞进 prompt。

形态 B：Allowlist / schema（给工具和 LLM 都能用）

manim_api_allowlist.json（示例概念）：

{
  "classes": ["Scene", "Mobject", "VGroup", "Axes", "NumberPlane", "MathTex", "Tex", "Dot", "Line"],
  "functions": ["FadeIn", "FadeOut", "Create", "Write", "Transform", "ReplacementTransform"],
  "methods": {
    "Mobject": ["move_to", "shift", "scale", "rotate", "set_color", "set_opacity", "next_to", "to_edge"]
  }
}

用途：

prompt 里告诉 LLM “只能用这些”

代码生成后用 AST 扫描：发现不在 allowlist 的调用 → 判失败 → 走修复

优点：可自动化、可强制。

形态 C：自动校验节点（你最需要的“硬门槛”）

在 code_gen 后、scene_fix 前加一个节点，例如 api_check：

它做三件事：

python -m py_compile scene.py（语法）

AST 扫描 Call(Name/Attribute)：找未知函数/方法

（可选更强）在 venv 里 import manim，用 inspect.signature 验证关键调用签名（对少数高风险 API）

输出：

api_ok: True/False

violations: [...]（具体哪个文件哪一行哪一个符号）

然后 LangGraph 路由：

ok → render

fail → fix（把 violations 当作修复证据）

这一步比“记忆”强 100 倍，因为它是可执行的。

在你现有 LangGraph 里怎么放（最小改动）

你现在是：
code_gen -> scene_fix -> render

建议变成：
code_gen -> api_check -> scene_fix -> render

并且 scene_fix 里的 prompt 增加两条硬约束：

“不得引入 allowlist 外的符号”

“如果需要功能但不在 allowlist，用已允许的替代写法”

Prompt 层面的关键技巧（减少幻觉）

即使有校验，也要减少无谓返工：

要求“只用 Manim CE 官方 API”并指定版本（你项目依赖哪个版本就写死）

要求“不要发明 helper 函数名”，除非在同文件明确定义

要求返回“完整可运行文件”，包含 import、Scene 类名

输出前自检清单（LLM 逐条确认）：

“All called functions are from allowlist or defined in file”

“Scene class name matches step id”

“No missing imports”
2.输出结构和kokoro的强制设定
3.layout设定 通过skill，通过system prompt？
4.少样本的finetune还是规则学习？