# Anthropic Claude Prompting Guide (Opus 4.6 Era)
_Source: Synthesized from public best practices, including Anthropic's official documentation._

Anthropic's Claude Opus 4.6 represents a significant advancement in AI models, designed for robust execution, complex reasoning, and agentic capabilities. To effectively harness its power, a new approach to prompt engineering is crucial. Here's a guide to prompting Opus 4.6, incorporating best practices and key insights:

### I. Core Principles for Effective Prompting

1.  **Be Clear and Direct:** Claude Opus 4.6 responds best to explicit, detailed instructions. Frame your prompts as if you're guiding a brilliant but new employee unfamiliar with your specific workflows. Avoid vague language and explicitly state what you want the model to do.

2.  **Provide Context and Motivation:** Explain the "why" behind your requests. Providing context helps Claude better understand your goals and deliver more targeted and relevant responses.

3.  **Assign Deliverables, Not Just Questions:** Instead of asking "How can I improve my website's SEO?", assign a role and a specific task, such as: "You are an SEO Engineer. Analyze the provided site audit report, identify the top 5 technical blockers ranked by impact, and generate a pull request for \`header.component.tsx\` that fixes the meta-tag hierarchy. Include before/after comparisons."

4.  **Use Positive Steering:** Claude Opus 4.6 responds significantly better to affirmative instructions ("do this") than prohibitions ("don't do that"). For example, instead of "Do not use bullet points," say "Compose your response in three concise paragraphs of prose."

5.  **Define \"Done\" Explicitly:** Clearly state when a task is complete to prevent the model from over-exploring or generating unnecessary information.

6.  **Give Claude Time to Think:** For complex tasks, encourage Claude to "Think step by step" or instruct it to "please think about it step-by-step within \`<thinking></thinking>\` tags" before producing the final answer. This can lead to more accurate results.

### II. Leveraging Opus 4.6's Advanced Features

1.  **Navigating the 1M Token Context Window:**
    *   **Structured Contextualization:** When providing large amounts of data (e.g., codebases, documentation), use XML tags to segment and label your information. For instance, wrap documentation in \`<documentation>\` tags and code in \`<codebase>\` tags for cleaner separation.
    *   **\"Bottom-Loading\" Technique:** Place your most critical instructions at the end of the prompt, immediately following large data blocks. The model pays the highest attention to these final instructions.
    *   **Skip Redundant Instructions:** There's no need to repeatedly ask Claude to \"read everything carefully\"; its architecture is optimized for high-context thoroughness.
    *   **Front-load Material:** The model can handle a large amount of information, so provide all necessary material upfront instead of drip-feeding context.

2.  **Controlling Reasoning Effort:**
    *   Opus 4.6 allows you to control the "Reasoning Effort," balancing performance with latency and cost.
    *   **Low Effort:** Ideal for straightforward tasks like formatting, brief summaries, or routine data conversion.
    *   **Adaptive Effort:** Opus 4.6 now adaptively decides how much reasoning to apply based on task complexity. Hard problems will receive more planning and revisited reasoning, while simple ones move faster.

3.  **Enhanced Agentic Capabilities & Tool Use:**
    *   Opus 4.6 is built for action and excels at planning, persistence, and agentic work.
    *   **Tool Use Sensitivity:** Avoid aggressive phrasing like \"You MUST call this tool.\" Instead, use calm, conditional language such as \"Use tools when appropriate and helpful\" to prevent over-triggering.

4.  **Coding Performance:**
    *   **Iterative Editing:** For files over 100 lines, ask Claude to generate an outline first, then progressively fill in sections to prevent context drift.
    *   **Test-Driven Prompts:** Provide expected outputs or failing test cases. Opus 4.6 is excellent at root cause analysis when given error logs and environment context.
    *   **Force Codebase Reading:** Include instructions like \"ALWAYS read and fully understand the relevant files before proposing any changes. Never speculate about file contents\" to prevent hallucinated edits.

5.  **Visual Understanding (Computer Use Features):**
    *   When using computer vision features, include screenshots or GUI state descriptions for improved visual understanding in UI automation.

### III. Advanced Prompting Techniques

1.  **Structured and Labeled Prompts:** Use XML tags to clearly separate different components of your prompt, such as instructions, context, and examples.

2.  **Few-Shot Prompting (Examples):** Provide 3-5 diverse examples of desired input-output pairs, especially for complex tasks, to guide Claude's format, tone, and structure. Place these examples early in the first user message, wrapped in \`<example>\` tags within \`<examples>\` tags.

3.  **Memory Injection:** Front-load a context block with your preferences (e.g., coding style, programming language) to establish defaults that carry through the conversation.

4.  **Reverse Prompting:** Instruct Claude to ask clarifying questions before it starts working on a task. This ensures it gathers all necessary information upfront.

5.  **Verification Loop:** Ask Claude to produce an output and then immediately critique its own work to identify and fix potential issues before presenting the final result.

6.  **Breaking Down Complex Tasks:** Divide complex tasks into smaller, sequential subtasks. You can use prompt chaining, where the output of one prompt feeds into the next.

### IV. Overriding Default Behaviors

*   **Prose Default:** By default, Opus 4.6 writes in natural, flowing paragraphs, avoiding excessive bolding or "walls of bullets." If you desire a specific structure (e.g., bullet points, headers), explicitly request it.
