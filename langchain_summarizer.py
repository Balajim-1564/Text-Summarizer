from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI

# Configure the OpenAI model; OPENAI_API_KEY must be set in the environment.
llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
)

# Keep the summarization instructions reusable with text and length placeholders.
prompt = PromptTemplate.from_template(
    """
You are an expert text summarizer.

Summarize the following text in a {length} format.

Instructions:
1. Identify the important points.
2. Avoid unnecessary details.
3. Keep the summary easy to understand.

Text:
{text}

Summary:
"""
)

# Convert the model's response into plain text.
parser = StrOutputParser()

# Run the prompt, model, and parser in sequence.
summarizer_chain = prompt | llm | parser


def summarize_text(text, length):
    # Supply values for the prompt's {text} and {length} placeholders.
    return summarizer_chain.invoke(
        {
            "text": text,
            "length": length,
        }
    )
