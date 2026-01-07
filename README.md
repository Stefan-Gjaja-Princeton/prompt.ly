# Welcome!

# This is prompt.ly: Prompt better, think better.

prompt.ly works just like a standard chatbot, but it provides tailored feedback on prompt depth and conceptual understanding too. It also makes its response terser if it detects poor prompt quality.

## Setup and Run Instructions

**The Easy Way**

Just go to https://promptly-frontend-dcbp.onrender.com/ - all the work is done for you! Bang.

**The Harder Way**

1. From the root of the directory, run: `bash pip install -r requirements.txt `
2. Run: `bash npm install`
3. In one terminal window, run: `bash ./start_backend.sh `
4. In another terminal window, run: `bash ./start_frontend.sh `
5. If your browser does not automatically open, navigate to http://localhost:3000

## Usage Examples

This product is designed for academic and business audiences.

**Academic**

Schools at all levels are under immense pressure with the surge of generative AI to both prepare students for an AI-first environment in the workplace and ensure that students are properly learning. prompt.ly allows students to make the most of Gen AI's powerful output while also keeping them honest to make sure they properly consdier the material they are asking about before seeking answers. Questions like "how do I answer this math problem?" will be answered with a response like "what do you think is an appropriate approach? Let's work together," and questions like "Summarize Moby Dick" will be answered with a response like "what aspects in particular? Are there particular themes or characters that you'd like to focus on?"

**Business**

Businesses are also confronted with a dual-pronged challenge with GenAI - how can they allow their workers to make the most of AI's efficiency gains while maintaining important skills in senior employees and building necessary skills in junior employees? prompt.ly once again answers this question by providing deep critical thinkers with the answers they are looking for and steering less sophisticated prompters to think about how they can be more effective in their prompting.

## Proof of Efficacy

I ran a study to determine if this tool is effective. The format of the study replicated some of the methods from the May 2025 MIT Study that found that heavy LLM use is associated with cognitive decline. In the study, participants were asked to complete two timed SAT-style essays with some form of assistance. In the first essay, their assistance was one of the following: nothing, an LLM of the participant's choice, or prompt.ly. In the second, all participants had to write unassisted. Responses were independently evaluated for quality and reflection questions were asked to determine recall and ownership of the work from the original authors. Here are the results from the abstract of my paper: Results indicate that while conventional
LLM assistance produced the strongest essays under time constraints, prompt.ly users demonstrated more ownership over their work and the strongest absolute performance when subsequently writing unassisted (as well as +6% performance from session 1 to 2 compared to -9% in LLM group).

## Use of AI Disclosure

As I explained in genai_usage_disclosure.md, I marked in the code at the top of files where I used Cursor, which was the only GenAI tool I used in coding this project. As my writeup describes, I allowed participants in my psychological study's LLM group to use an LLM of their choice. I will also add that the directory structure was also recommended by Cursor - couldn't put that in a specific area in the code. The code is explained through in line comments.

## Testing information

You can find the testing information (how to test and what the tests cover) in how_to_test.md.
