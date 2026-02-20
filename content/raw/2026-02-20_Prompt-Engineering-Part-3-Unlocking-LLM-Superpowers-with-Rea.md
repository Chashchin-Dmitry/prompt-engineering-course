# Prompt Engineering Part 3: Unlocking LLM Superpowers with Reasoning Techniques

**Source:** https://medium.com/@akankshasinha247/prompt-engineering-part-3-unlocking-llm-superpowers-with-reasoning-techniques-9848cabc21f0
**Author:** Akanksha Sinha
**Published:** None
**Scraped:** 2026-02-20

---

Prompt Engineering Part 3: Unlocking LLM Superpowers with Reasoning Techniques
Akanksha Sinha
4 min read
·
May 21, 2025
--
Day 50 of #100DaysOfAI | Reasoning -Based Prompting
“Prompting isn’t trial and error — it’s design thinking for machines. Reasoning is how you teach LLMs to think.”
As LLMs become more deeply integrated into business and product workflows, mastering
how
to guide them becomes as important as knowing
what
to ask.
Today, we explore three foundational
reasoning techniques
that unlock new levels of clarity, accuracy, and intelligence from LLMs:
What Are They?
1. Chain-of-Thought (CoT) Prompting
Encourages the model to “think out loud” by walking through intermediate steps.
Best for:
Math, logic, and multi-step reasoning.
Think:
“Step 1: calculate X. Step 2: add Y to X. Step 3: Result.”
Origin:
Wei et al., 2022 (Google)
2. ReAct (Reason + Act) Prompting
Combines CoT reasoning with tool-like action((search, verify, calculate)) steps, allowing the LLM to simulate interactions (e.g., retrieval, search, tool use).
Best for:
Decision support, planning, or tasks needing evidence or verification.
Think:
“Thought: I need data on X → Action: Search → Thought: Based on that, I choose Y.”
Origin:
Yao et al., 2022 —
Link to paper
3. Tree-of-Thought (ToT) Prompting
Simulates multiple reasoning branches before reaching a decision — much like weighing trade-offs or options.
Best for:
Strategic analysis, evaluations, planning, or choices involving pros and cons.
Think:
“Option A: Pros & Cons. Option B: Pros & Cons. Now compare and decide.”
Origin:
Long et al., 2023 (DeepMind & Princeton) —
Link to paper
Real-World Experiments
Task 1: Chain-of-Thought (Math Reasoning)
Prompting for precision:
Prompt Template:
Press enter or click to view image in full size
Example
A bakery sold 120 muffins in the morning, 80 in the afternoon, and 150 in the evening.
How many muffins in total? Let’s think step by step.
Output:
Step-by-step breakdown →
350 muffins
📸 Screenshot 1: CoT reasoning output (Math Problem)
Press enter or click to view image in full size
Screenshot 1: CoT reasoning output (Math Problem, GPT 4o)
Task 2: ReAct (Business Decision-Making)
Prompting for guided action:
Prompt Template:
Press enter or click to view image in full size
Example
Your task is to identify whether a company should launch a new eco-friendly product.
At each step:
Thought: [Reasoning]
Action: [Choose next step]
Final Answer: [Decision with justification]
Output:
6-step reasoning-action process →
Launch recommended
(based on demand, capability, ROI)
📸 Screenshot 2: ReAct-style strategic decision-making
Press enter or click to view image in full size
Screenshot 2: ReAct-style strategic decision-making (GPT 4o)
Task 3: Tree-of-Thought (Strategic Product Planning)
Prompting for exploratory reasoning:
Prompt Template:
Press enter or click to view image in full size
Example
You’re planning a Q3 product launch.
Options:
(1) Early launch with limited features
(2) Delay for full feature set
(3) Beta release with feedback
Evaluate each using a Tree-of-Thought approach.
Output:
Three decision branches + subthoughts →
Best option: Beta release with feedback
📸 Screenshot 3: ToT-style output with comparative decision matrix
Press enter or click to view image in full size
Screenshot 3: ToT-style output with comparative decision matrix (GPT 4o Model)
Comparative Summary Table
Press enter or click to view image in full size
Comparing Prompt Reasoning Techniques
Key Takeaways
Chain-of-Thought
improves clarity in multi-step logic.
ReAct
adds tool-like thinking and verification.
Tree-of-Thought
helps in structured decision-making with pros/cons exploration.
Each is not just a prompting style — it’s a
thinking framework
for LLMs.
📚 Further Reading
Chain-of-Thought Prompting (Wei et al., 2022)
ReAct: Reason + Act Prompting (Yao et al., 2022)
Tree-of-Thought Prompting (Long et al., 2023)
Prompting Guide
OpenAI Cookbook
💬 Let’s Talk
Which of these reasoning techniques have you used in your workflows?

---
*Auto-collected for Prompt Engineering Course*
