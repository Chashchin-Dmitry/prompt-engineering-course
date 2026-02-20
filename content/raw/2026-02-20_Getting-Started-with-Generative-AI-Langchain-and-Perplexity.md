# Getting Started with Generative AI: Langchain and Perplexity in Action

**Source:** https://jolumabu.medium.com/getting-started-with-generative-ai-langchain-and-perplexity-in-action-6f205f6673bf
**Author:** Tech, IT Arch. & Soft Dev.
**Published:** None
**Scraped:** 2026-02-20

---

Getting Started with Generative AI: Langchain and Perplexity in Action
Generative AI Is Reshaping Daily Life
Tech, IT Arch. & Soft Dev.
6 min read
·
Aug 31, 2025
--
Press enter or click to view image in full size
Photo by
Igor Omilaev
on
Unsplash
Introduction
Generative AI is revolutionising several aspects of our daily and professional lives.
It allows us to access and interact with information in new ways, or use it as part of our daily work, as an assistant that helps boost our productivity.
The adoption of these tools in internet search, as opposed to traditional browsers and search engines, is already a reality. Some platforms are now directly powered by this technology, enriching conventional search experiences.
In software development, guided tools are helping both professionals and enthusiasts accelerate prototyping and testing. Software engineers enhance productivity and allow a shift toward more advanced tasks within the field. Still, it’s important to acknowledge the risks of using these technologies without the proper knowledge and experience
This approach streamlines experimentation, promotes best practices, and makes your generative AI workflows more maintainable.
Key Tools: LangChain and Perplexity
From an AI-driven development perspective, frameworks like
LangChain
empower both enthusiasts and professionals to implement their own generative AI use cases.
In this article (and chapter), you will learn how to:
Set up your development environment
Run intelligent queries
Leverage generative AI’s capabilities
Perplexity
is an AI-powered search engine with an open API. You can integrate its capabilities in two ways:
Directly calling their REST APIs for maximum control
Using frameworks like LangChain, which abstract away the complexity of REST calls. But with the additional limitations of framework implementation
Tip: Direct API integration ensures compatibility without intermediaries, while LangChain simplifies the process by handling HTTP requests and response parsing under the hood. Langchain itself is a development framework built around LLMs (Large Language Models).
LangChain
is a development framework built around LLMs (Large Language Models), designed to simplify integration and experimentation.
Integrate LLM using LangChain
In this section, we’ll focus on the LangChain framework. We’ll use
ChatPerplexity
along with the
invoke
method in its simplest form. To get started, you’ll need:
An
API key
from Perplexity
A supported
model
(e.g.,
"sonar"
), in that case from perplexity
A
temperature
setting (which controls response creativity)
A
prompt
to send to the model
Here’s the basic implementation:
from langchain.chat_models import ChatPerplexity
model = ChatPerplexity(
api_key="your_api_key",
model="sonar",
temperature=0.2
)
response = model.invoke("What is the capital of Spain?")
print(response)
Tip:
Lower temperature values (e.g., 0.2) produce more focused and deterministic answers, while higher values (e.g., 0.8) allow for more creative and varied responses
The Model’s Response
When you inspect the returned
AIMessage
, you’ll see a structure typical of a large language model message, with additional fields to meet Perplexity’s needs:
content
: The AI-generated answer, returned in Markdown. This lets you display and format the response more cleanly in notebooks or web UIs.
additional_kwargs:
Contains extra elements, such as
citations
, which list the trusted sources underpinning each statement. By linking every claim to a reference, you ensure traceability and support research-grade transparency.
metadata
Encapsulates model‐ and execution-related details:
model_name
: the exact model used
id
: a unique identifier for this response
usage_metadata
: token counts (input, output, total), invaluable for cost analysis, performance tuning, and tracking compute resources
Give context to the LLM
A clear message structure is key to guiding the model’s behavior. You establish this by defining:.
SystemMessage
Sets the model’s role and high-level instructions (e.g. “You are a helpful assistant that cites reliable sources”).
HumanMessage
Carries the user’s prompt or question.
By layering SystemMessages and HumanMessages, you create a focused conversational context. This approach delivers more coherent, purpose-driven answers and elevates response quality across your applications.
from langchain_perplexity import ChatPerplexity
from langchain.schema import SystemMessage, HumanMessage
model = ChatPerplexity(api_key=api_key,
model="sonar",
temperature=0.9)
system_msg = SystemMessage(content=
'''You are a helpful assistant. That are expert in Electonic and embbeded System.''')
user_msg = HumanMessage(content='''What is a esp32 microcontroller?''')
messages = [system_msg, user_msg]
model.invoke(messages)
Prompt reuse
An important capability to keep in mind is the reuse and curation of prompts you’ve already crafted. LangChain provides the PromptTemplate class, which lets you define a prompt template as a structured data object and embed placeholder variables that will be substituted at runtime.
By centralizing your prompts in templates, you ensure consistency across your application, reduce duplication, and make it easier to update or refine prompts in one place rather than hunting through your codebase. For example
from langchain_core.prompts import ChatPromptTemplate
from langchain_perplexity import ChatPerplexity
template = ChatPromptTemplate.from_messages([
("system", "Respond to the following question using ONLY the text below and don't use any other information. If you don't know the answer, just say that you don't know."),
("human", "context: {context}\nquestion: {question}")
])
prompt = template.invoke({
"context": """The ESP32 is a family of low-cost, energy-efficient microcontrollers
developed by Espressif Systems. It is designed for embedded applications,
especially in the Internet of Things (IoT) space, and integrates both Wi-Fi and
Bluetooth connectivity in a single chip, making it highly suitable
for wireless data communication.Key Features of the ESP32 Microcontroller:-
- **Processor:** It typically features a Tensilica Xtensa LX6 microprocessor available in dual-core or single-core versions.
Newer models also include variants with the Xtensa LX7 dual-core processor or a single-core RISC-V microprocessor, the
latter being open-source and well-supported by compilers.
- **Wireless Connectivity:** Integrated Wi-Fi and Bluetooth (both classic and BLE), enabling devices
to connect to the internet or form networks without additional hardware.
- **Power Efficiency:** The ESP32 is designed to be low-power, supporting various sleep modes such as deep sleep to minimize
energy consumption, which is critical for battery-powered and portable devices.
**Integrated Components:** The chip includes built-in antenna switches, RF balun, power amplifiers, low-noise receivers, filters,
and power management modules for efficient wireless performance without the need for many external components.
**GPIO and Peripheral Support:** It provides multiple General
Purpose Input/Output pins (up to 34 in original models, and more in newer ones), along with interfaces like SPI, I2C, UART, ADC, PWM, and more, allowing it to control sensors, motors, LEDs, and other components.
**Variants and Subfamilies:** There are multiple models and series of ESP32 microcontrollers tailored to different use cases, including the original ESP32, ESP32-S series (with improvements in processor and security), ESP32-C series, and ESP32-H series. These variations offer different core architectures, clock speeds, connectivity options, and peripheral counts[2][4].\n\n### Typical Applications:\n\nThe ESP32 is widely used in IoT devices, wearable technology, smart home automation, mobile devices, and embedded systems. Its combination of wireless connectivity, processing power, and energy efficiency make it a popular choice among hobbyists and commercial developers alike[2][4][5].\n\nIn summary, the ESP32 is a versatile, powerful, and affordable microcontroller that integrates Wi-Fi and Bluetooth connectivity, designed primarily for IoT and embedded applications
requiring wireless communication with low power consumption""",
"question": "Is capable to use MQTT ? "
})
model = ChatPerplexity(api_key=api_key,
model="sonar",
temperature=0.9)
model.invoke(prompt)
This approach streamlines experimentation, promotes best practices, and makes your generative AI workflows more maintainable.
Response normalization
Although the response is already normalized by default, you can structure a language model’s output into a user-defined format. This is useful, for example, when you need to store the data according to a database schema.
This code uses S
tructured_Output
and
Pydantic
. Here is a breakdown of what it does:
class answerWithJustificaction(BaseModel):
answer: str
justification: str
Where :
answer
: Un campo de tipo
str
que contendrá la respuesta principal del modelo.
justification
: Un campo de tipo
str
que contendrá la justificación o explicación de la respuesta.
and after of this applies:
structuredLLM = llm.with_structured_output(answerWithJustificaction)
Conclusion
Generative AI is proving to be a transformative force across search, content creation, and software development. By combining Langchain’s abstractions with Perplexity’s powerful API, you can rapidly prototype intelligent applications, experiment with LLM behaviors, and maintain clean, reproducible workflows. tools like
PromptTemplate
ensure your prompts remain consistent and easy to manage.
Key takeaways:
Establishing a clear message structure (SystemMessage + HumanMessage) dramatically improves response coherence.
Fine-tuning parameters such as
temperature
lets you balance precision and creativity.
Centralizing prompts into templates reduces duplication and accelerates iteration.
Inspecting
AIMessage
fields (content, citations, metadata) enhances transparency and research rigor.
Stay tuned for more deep dives that will help you build robust, responsible, and cutting-edge generative AI solutions.

---
*Auto-collected for Prompt Engineering Course*
