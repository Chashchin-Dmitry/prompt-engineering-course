# System Prompt Engineering: How to Shape Generative AI for Real Business Needs

**Source:** https://medium.com/@dmitry-baraishuk/system-prompt-engineering-how-to-shape-generative-ai-for-real-business-needs-3c22652dc17b
**Author:** 
**Published:** None
**Scraped:** 2026-02-20

---

System Prompt Engineering: How to Shape Generative AI for Real Business Needs
Dmitry Baraishuk
8 min read
·
Aug 21, 2025

This article contains ideas on customizing prompts for gen AI applications and the golden rules of prompt engineering. The enterprise generative AI market is growing. Companies need “picks and shovels” to adapt LLMs to their proprietary data. To assist businesses, software experts examine their niche terminology and workflows and apply prompt engineering to tailor AI behavior to each customer’s requirements.

Press enter or click to view image in full size

Belitsoft is a software development company that offers outsourced services of LLM training. To tailor our customers’ LLMs, we leverage their internal data (policies, documents, workflows) to tailor their LLMs while taking good care of data security. We employ different prompt engineering techniques (few-shot prompting, chain-of-thought, etc.) to align the responses with appropriate use cases. As a result, the LLM interprets complex queries with high contextual accuracy.

Large enterprises seek full-spectrum customization and need LLMs that are trained on their internal knowledge datasets, branding, advanced functionality, etc. These companies can choose to develop a gen AI model from scratch. However, this option requires massive investment. Another way is to either use ready-made models or customize existing ones by training them with proprietary data.

According to market researchers, the global prompt engineering market is projected to grow from USD 280.08 million in 2024 to USD 2,515.79 billion by 2032, with a CAGR of 31.6% during the forecast period.

Why Prompts Are Your Secret Weapon

Interactions between a human and a machine are currently happening with natural language (NL). That is why it is important to formulate prompts that direct artificial intelligence (AI) in its effort to generate relevant and reliable responses. The skill of prompt engineering includes formulating correct requests and anticipating how the AI will interpret and execute commands. Competent prompt engineers build prompts with linguistic precision and the knowledge of how algorithms perform their functions.

No matter what framework you use (LlamaIndex, LangChain, or your own code), the retrieval-augmented generation (RAG) system needs clear, well-structured prompts for every LLM interaction. A RAG-based application behaves as a simple user does while interacting with an LLM through the chat. For every task, such as indexing, retrieval of the information, metadata extraction, or response generation, the RAG system produces prompts. The context is added to those prompts and sent to the LLM.

Ready-made systems like LlamaIndex provide templates, storage, injection, and inspection tools. However, it is necessary to understand and fine-tune them. For instance, in LlamaIndex, every kind of interaction with an LLM uses a default prompt as a template. For example, the TitleExtractor extracts metadata into the RAG workflow. Prompt libraries allow you to speed up the process of creating content and provide a more predictable result since all requests have already been pre-checked. However, the models are regularly updated and it is useful to test the existing prompts on new versions.

Customizing Prompts

The RAG workflow programmatically creates prompts. When LlamaIndex or any other framework is used, it builds prompts based on the company’s documents. The documents are divided into nodes, indexed, and selected with retrievers.

Prompt customization is sometimes necessary or desirable. Developers do it, as it helps to achieve better interaction between the RAG components and the LLM, which leads to improved accuracy, and effectiveness of the app. Prompt customization is used in the following situations:

To integrate domain-specific knowledge and terms
To adjust prompts to a certain writing style or tone
To modify prompts to prioritize certain types of information or outputs
To use different prompt structures in order to optimize performance or quality

The LlamaIndex framework offers the following advanced prompting techniques:

Partial formatting means that you format a prompt partially, leaving some variables to be filled in later. It is convenient for multi-step processes when the required data is not available at once.
Prompt template variable mappings let you reuse existing templates instead of rewriting them.
Prompt function mappings allow for dynamic injection of certain values that depend on some specific conditions.
The Golden Rules of Prompt Engineering

The following golden rules include the prompt’s characteristics, differences of LLMs, and methods of creating prompts. By following these recommendations, you can develop effective and reliable RAG applications using LlamaIndex or other frameworks.

Accuracy

The prompt is precise and does not allow for ambiguity. You will receive a relevant response only if you clearly state what you need.

Directiveness

The directiveness of the prompt impacts the response. The prompt can be either open-ended or specific. The first type implies some space for creativity. The second needs a particular answer. As it was mentioned earlier, prompts combine the static part with dynamically retrieved content. Prompts should contain verbs like “summarize”, “analyze”, or “explain”, because those are clear instructions that make AI understand what is needed.

Context quality

An effective RAG system depends on the proprietary knowledge base. Prompt engineers remove data duplicates, inconsistencies, and grammar mistakes from the database, as they affect the retrieval process and the response generation.

Context quantity

A prompt should be brief and detailed at the same time. It means it should give the context in the amount sufficient to understand the request and specific requirements. Providing a RAG system with more details can give a broader understanding of the task, but it also can confuse the system with a lengthy prompt. Long and unstructured prompts may lead to hallucinations or irrelevant answers. Structured and relevant long prompts can improve accuracy.

Cognitive load is the amount of resources that the LLM needs to examine, understand, and respond to. With RAG systems, cognitive load is the amount and difficulty of the prompt context.

Get Dmitry Baraishuk’s stories in your inbox

Join Medium for free to get updates from this writer.

Apart from the context quality and quantity, context ordering is also critical. If you provide a long context, make sure you place the key information at the beginning or at the end. It helps LLMs to extract the main problem from the context and generate a relevant output.

Required output format

You need to specify the output in format, size, or language.

Inference costs

It is important to make cost estimations and consider token usage. Tools like LongLLMLinguaPostprocessor help to compress prompts. Prompt compression techniques can also improve the quality of the final response by removing unnecessary data from the context.

System latency

The system latency is related to the quality of the prompts. When there is a long and overly detailed request, the system requires more time to process it. Long processing times decrease user satisfaction levels. Prompt engineers regularly evaluate the performance of the prompts and optimize them depending on the results. It is a continuous process because the rules are changing rapidly.

Selecting the Right LLM

Not all LLMs are equal. The wrong LLM is able to neglect the effort devoted to crafting prompts. The following characteristics are useful while choosing the model:

Model architecture defines which tasks the model is suited for. Encoder-only models (BERT) categorize texts and predict relations between sentences. Encoder-decoder models (BART) not only understand the input but also generate new texts. They can translate, summarize, and provide responses. Decoder-only models (GPT, LlaMa, Claude, Mistral) predict the next words in a sequence and can perform creative tasks. They write different texts and answer questions. Mixture-of-experts (MoE) models (Mixtral 8x7B) can cope with complex math, multilingual tasks, and code generation.
Model size determines computational costs and the model’s capabilities. The more parameters the LLM has, the more resources it needs, and the higher operational expenses are.
Inference speed is how fast the system processes input and generates output. Model pruning, quantization, and special hardware can improve the LLM speed.

Besides the above-mentioned characteristics, LLMs can be divided according to different tasks or domains, demonstrating better performance in certain scenarios.

Chat models are used for building AI chatbots and virtual assistants.
Instruct models are found in educational tools and productivity applications, where users are interested in a detailed explanation rather than a natural conversation.
Codex models are integrated into development environments and coding automation tools. They help with coding tasks, debugging codes, explaining code snippets, and even generating programs based on a description.
Summarization models transform long texts into short summaries. They are used in news aggregation services, content creation, and research.
Translation models suit global communication platforms, educational platforms for language learners, and localization tools.
Question-answering models are underneath intelligent search engines and interactive knowledge bases.
Methods for Creating Prompts

The following advanced techniques are used for complex and multi-step RAG applications. They structure the input to better guide the model’s internal reasoning.

Few-shot prompting, or k-shot prompting, means showing a couple of examples of the task. Those examples demonstrate the model of what kind of response is expected from it. It helps to optimize the system to the tasks specific to a certain niche.
Chain-of-Thought (CoT) prompting is breaking the problem into several steps. Instead of asking the system to provide the final result, prompts encourage the model to explain the process step-by-step. For example: “Children have five apples. John has eaten two apples, and Mary has eaten one apple. How many apples are left? Explain the solution step-by-step”. The system shows each calculation one by one as a school student does. The process of answer generation becomes transparent and reliable with this method.
Self-consistency method improves the performance of the CoT prompting. It generates several reasoning paths and selects the answer that appears in most or all cases. For example, the task about apples mentioned earlier can be solved in three ways:
5–2–1 = 2 apples left
5 — (2 + 1) = 2 apples left
5–1–2 = 2 apples left

The answer is 2 in all approaches, so 2 is the final result. This method of prompting is used to solve logic puzzles, math problems, and real-world reasoning (“Should I buy the shares of this company?”).

Tree of Thoughts (ToT) prompting is based on the CoT, but it goes further, generates several ways of dealing with each step, and evaluates the results of each step. It may turn back if the result is incorrect and examine another solution. Therefore, each solution is like a new branch of a tree.
Prompt chaining is giving short prompts in a sequence. The output of the first prompt becomes the input of the second. It makes the process of dealing with complicated tasks simpler.
API-Based and Tool-Augmented Prompting

The following methods are used when the model interacts with external systems, tools, or APIs to retrieve or process data.

Function Calling is calling an external function according to the described scheme (via the OpenAl API, etc.). The model provides structured outputs (e.g., JSON) after calling integrated APIs. For example, in response to “Weather forecast in Paris?” the model calls getWeather(“Paris”) and generates the answer.
Tool Use allows the model to dynamically choose tools (search engines, calculators, APIs, etc.) while generating the answer. For example, to provide the latest news on a certain topic, it uses a connected search tool. Models retrieve live data and verify facts.
ReAct (Reason + Act) combines natural language reasoning and tool execution. Users provide prompts such as “I need to find out the dollar exchange rate. First tell me what you’re going to do, and then do it.” The model gives a step-by-step plan, performs actions (tool calls), observes the results, and continues its logic. ReAct serves as the foundation for AI agents and retrieval-augmented decision-making.

Originally published here

---
*Auto-collected for Prompt Engineering Course*
