from openai import OpenAI

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI



llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
)

prompt = PromptTemplate.from_template(
    """
You are an expert text summarizer.

Summarize the following text in a {summary_length} format and present it as {summary_format}.

Instructions:
1. Identify the important points.
2. Avoid unnecessary details.
3. Keep the summary easy to understand.
4. Follow the requested output format.

Text:
{source_text}

Summary:    
"""
)

parser = StrOutputParser()
summarizer_chain = prompt | llm | parser

client = OpenAI()

def summarize_text(source_text, summary_length, summary_format):
    response = client.chat.completions.create(
        model = "gpt-4o-mini",
        messages = [
        {
            "role": "system",
            "content": "You are an expert text summarizer."
        },
        {
            "role": "user",
            "content": (
                    f"Summarize the text in a {summary_length} format "
                    f"and present it as {summary_format}.\n\n"
                    f"Text:\n{source_text}"
                )
        }
        ]
    )

    return response.choices[0].message.content

# def summarize_text(source_text, summary_length, summary_format="paragraph"):
#     return summarizer_chain.invoke(
#         {
#             "source_text": source_text,
#             "summary_length": summary_length,
#             "summary_format": summary_format,
#         }
#     )
