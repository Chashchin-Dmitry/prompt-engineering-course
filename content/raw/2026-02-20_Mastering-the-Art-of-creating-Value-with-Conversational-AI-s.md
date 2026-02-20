# Mastering the Art of creating Value with Conversational AI systems Prompt Engineering for Business

**Source:** https://medium.com/@dialoglk/mastering-the-art-of-creating-value-with-conversational-ai-systems-prompt-engineering-for-business-f310af652b97
**Author:** 
**Published:** None
**Scraped:** 2026-02-20

---

Mastering the Art of creating Value with Conversational AI systems
Prompt Engineering for Business
Dialog Axiata
8 min read
·
Sep 15, 2023

Press enter or click to view image in full size

Author Shehan Perera: Shehan is a dedicated Data Science Lead with over 6 years of experience in the Data Science and Analytics fields. His expertise and skills extend across Generative AI, Deep Learning, Statistics, Python, SQL, and more. Currently, Shehan is a Senior Data Scientist at Dialog Axiata PLC. His responsibilities include leading Axiata Experiments and the R&D track, collaborating with telecommunications companies across the Axiata group to drive Generative AI initiatives and research and development tasks.

Generative AI has the potential to revolutionize the global economy, adding trillions of dollars in value. McKinsey estimates it could add $2.6 to $4.4 trillion annually across 63 use cases, which is more than the GDP of the United Kingdom. With the ability to automate complex tasks, understand natural language, and potentially automate 60% to 70% of tasks, generative AI envisions a workforce evolution by 2030–2060. To stay competitive in the market, organizations must embrace generative AI and master the art of communicating with conversational AI systems. As models like OpenAI’s GPT series and Google’s Bard become more prevalent, understanding how to interact with them effectively becomes crucial. In this article, we’re diving deep into the realm of prompt engineering, unraveling its significance, techniques, and real-world applications with captivating examples on how it can be used in your organization to create value, in a way that safeguards data privacy and security while maximizing the benefits of language models.

What is Prompt Engineering?

Prompt engineering is the art and science of crafting input instructions, or “prompts,” that yield desired responses from AI models. It’s the process of formulating queries or commands that elicit accurate and contextually relevant outputs.

Think of prompts as the guiding questions you pose to AI systems, instructing them to perform specific tasks, generate creative content, answer questions, or even engage in meaningful conversations.

Figure 1: An AI generated crayon drawing of several cute colorful monsters with ice cream cone bodies on dark blue paper
Why is Prompt Engineering Important?

By mastering prompt engineering, you can:

Enhance Precision: Craft prompts to produce specific information or outputs, reducing the need for post-processing or filtering.

Optimize Efficiency: Well-constructed prompts lead to quicker, more accurate results, saving time and resources in refining outputs.

Cost Efficiency: In cloud-based model deployments, you’re often charged per token (words/characters). Efficient prompts can reduce unnecessary verbiage and costs.

Safety and Bias Mitigation: Carefully crafted prompts can reduce the chances of a model producing harmful or biased outputs.

Improve Creativity: Prompt engineering can coax AI models into generating imaginative and creative content that aligns with your goals.

The following are AI generated images of an astronaut riding a horse and a stern owl dressed as a librarian. There were created using DALLE-2.

Mastering the Art of Prompt Engineering: Techniques and Tips

a) Be Clear and Specific: Be precise and specific in your prompts. Use delimiters to make the prompt clear and more organized (See example 2). Ask for a structured output such as HTML, JSON whenever possible (See example 7). Clearly state the task or information you’re seeking. For instance, compare:

Generic: “Write about dogs.”
Engineered: “Craft a 300-word piece on the evolution of dog breeds over the last century.”

b) Avoid Entering Personal or Confidential Information: Ensuring the highest level of data safety and security is a primary concern. Before engaging with Language Model Models (LLMs), it is essential to carefully review data privacy policies. Many LLMs rely on input data to enhance their models, underscoring the importance of refraining from inputting confidential information. Organizations can effectively safeguard data by opting for solutions like Azure OpenAI service, enabling the deployment of proprietary LLMs within dedicated virtual private clouds (VPCs) for enhanced data protection.

c) Contextual Cues: Provide context within your prompt. This helps the AI model understand the task better. For instance:

Generic: “Summarize this article.”
Engineered: “Generate a concise summary (150 words) of the attached article about renewable energy breakthroughs.”

d) Give the model time to think: This is important for problems which need several steps to solve. Clearly guide the model with the steps to complete a specific task. Also, instruct the model to work on its own solution before rushing into conclusions.

e) Examples Speak Volumes: When seeking creative content, offer examples to guide the AI’s style and tone. For instance:

Generic: “Write a poem about nature.”
Engineered: “Compose a lyrical poem (10–12 lines) inspired by the tranquility of a forest, using vivid imagery and a reflective tone.”

f) Iterative Prompt Development: Don’t hesitate to iterate and experiment with different prompts. Analyze why your result is not the desired output, refine the idea and the prompt, and then repeat the process.

g) Avoid Biases: Ensure that your prompts don’t inadvertently introduce or amplify biases. For instance:

Biased: “Why is junk food bad?”
Neutral: “Discuss the nutritional value and health implications of junk food.”
Real-World Applications of Prompt Engineering for your Company

Let’s explore some real-world scenarios where prompt engineering can be a game-changer in your organization:

1. Content Creation: Tailor AI-generated articles, emails, stories, or marketing copy to suit specific themes, styles, or target audiences.

Example 1: Writing an email to customers notifying a maintenance

Could you provide a sample email to notify our corporate clients about a scheduled maintenance downtime, including the date, time, expected duration, and alternative means of communication during the downtime?

Example 2: Writing microcopy for a brand ‘ABC’ in its tone of voice

I will provide you with phrase delimited by triple backticks, and your job is to rephrase them in the tone of voice of the brand “ABC”. “ABC” is a brand that caters to digital consumers in Sri Lanka. It is known for being personable and friendly, spontaneous and high-energy, modern and high-tech, and fun. The tone of voice for “ABC” should be more of a twin to the consumer. It should be playful, engaging, and always up for a good time.

Your first phrase is: ```This voucher has been collected successfully, and added to the ABC Wallet```

Keep the response lesser than 25 words.

Example 3: Making the text accessible to a non-technical audience

Could you assist me in rephrasing this technical description to make it more accessible to a non-technical audience?

Description: “Our new 5G-enabled router leverages advanced millimeter-wave technology to provide ultra-high-speed internet connectivity, enabling lightning-fast downloads and lag-free streaming. “

Example 4: Generating FAQs for a product within seconds

Generate FAQs for the following product delimited by <>

<Name: The GigaMax Plan

Price: $79.99 per month

Get Dialog Axiata’s stories in your inbox

Join Medium for free to get updates from this writer.

Data: Unlimited data

Features:

Includes 50GB of mobile hotspot data

Free international roaming in Mexico and Canada

Free streaming of music and video

No contracts or hidden fees>

Example 5: Grammar Corrections in an Email

Can you please review the following email and perform any grammar corrections if there are any? “Dear team members, I wants to reminds you about the upcoming meeting on 20th of March, 10 AM. Its important that everybody attends the meeting as we needs to discuss about the new project. Also, please brings any relevant documents or information that you have. Its crucial for the success of the project. Thank you for your cooperation and I looks forward to seeing you all at the meeting.“

2. Data Analysis, Transformation and Insights Extraction: Extract relevant insights from datasets by framing queries that prompt detailed, insightful responses.

Example 6: Data Transformation: Conversion from JSON to XML

Transform the below JSON to XML format.

“data_json ={ “resturant employees” :[

{“name”:”Shyam”, “email”:”shyamjaiswal@gmail.com”},

{“name”:”Bob”, “email”:”bob32@gmail.com”},

{“name”:”Jai”, “email”:”jai87@gmail.com”}

]}”

Example 7: Extracting relevant insights from a CV to fast-track recruitment

Extract Name, Address, Email Address, Telephone number, Experience from following text delimited by triple backticks.

```John W. Smith 2002 Front Range Way Fort Collins, CO 80525 jwsmith@colostate.edu Career Summary Four years’ experience in early childhood development with a diverse background in the care of special needs children and adults. ```

Give the response in JSON format.

3. Generating code: Prompt engineering can be used to generate code, such as Python scripts or Java programs.

Example 8: Generate code for the Frontend and Backend of a Chatbot

I need to create a Chatbot using Flask as the backend. Frontend should be in html, css, javascript

For backend, generate flask code to do the following.

- Receive frontend request in json form

- Process the user message comes in request (through a python code)

- Return the response message in json form

For frontend,

- Take the user message from a UI

- Convert it to json

- Send request to flask backend

- Display backend response in the UI

Give file structure of both backend and frontend.

Then give content of each file separately.

4. Academic Aid: Seek AI assistance for academic tasks like generating explanations for complex concepts or formulating hypotheses.

Example 9: Question of languages to build a scalable frontend application

What are the best programming languages that most suitable for a scalable frontend application?

5. Problem Solving: Seek AI assistance for coding challenges or mathematical problem-solving by phrasing prompts that guide the model step by step.

Example 10: Mathematical problem related to analyzing website traffic data

The analytics team is analyzing website traffic data. They recorded 1,000 visits last week, with an average session duration of 2.5 minutes. What was the total time spent by visitors on the website?

6. Generating images: Prompt engineering can be used to generate images, such as paintings, photographs, or even cartoons.

Example 11: AI generated image for a Sales campaign

Teddy bears shopping for groceries, pencil and watercolor drawing

Press enter or click to view image in full size
Figure 4 :Teddy Bears Shopping

Conclusion

Generative AI has big potential for businesses which compels enterprises to embrace it to stay competitive in the market. As AI infiltrates daily life and workplaces, learning prompt engineering is crucial to make the most out of Generative AI. Following privacy rules, avoiding sensitive data, and using secure platforms like Azure OpenAI help adopt this tech smartly. Yet, vigilance against biases and AI model outputs is essential. Balancing innovation and responsibility unlock prompt engineering’s true enterprise potential, enriching capabilities with AI to create significant value while upholding ethics and security.

References

McKinsey & Company. “The economic potential of generative AI: The next productivity frontier,” McKinsey Digital, [Online]. Available: https://www.mckinsey.com/capabilities/mckinsey-digital/our-insights/the-economic-potential-of-generative-ai-the-next-productivity-frontier#introduction [Accessed: August 20, 2023].

OpenAI, “DALL·E 2,” [Online]. Available: https://openai.com/dall-e-2. [Accessed: Aug. 20, 2023].

---
*Auto-collected for Prompt Engineering Course*
