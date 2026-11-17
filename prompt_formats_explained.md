# Python f-strings and LangChain PromptTemplate

Both formats let you place changing values inside a prompt, but they fill
those values at different times and produce different kinds of objects.

## 1. Python f-string

```python
purpose = "announce a team meeting"
tone = "friendly"
recipient = "the project team"

email_prompt = f"""
You are an expert email writer.
Generate an email.
Purpose: {purpose}
Tone: {tone}
Recipient: {recipient}
Return:
Subject: Body:
"""
```

The `f` before the opening triple quote tells Python to evaluate expressions
inside braces immediately. When this assignment runs, Python replaces
`{purpose}`, `{tone}`, and `{recipient}` with their current values.

Afterward, `email_prompt` is an ordinary Python `str` containing the completed
text. The variables must already exist when the f-string is evaluated. If one
does not exist, Python raises a `NameError`.

An f-string does not call an AI model. It only constructs text. You can then
pass that text to code that makes a model request.

## 2. LangChain `PromptTemplate`

```python
from langchain_core.prompts import PromptTemplate

summary_prompt = PromptTemplate.from_template(
    """
You are an expert text summarizer.
Summarize the following text in a {length} format.

Text:
{text}

Summary:
"""
)
```

Here, `{length}` and `{text}` remain placeholders when `summary_prompt` is
created. `PromptTemplate.from_template()` creates a LangChain template object
and identifies those placeholders as inputs.

The values are supplied later:

```python
formatted_prompt = summary_prompt.format(
    text="The source text to summarize.",
    length="short",
)
```

`formatted_prompt` is now the completed prompt text. Formatting the template
does not itself call the AI model.

In a LangChain chain, the prompt can be connected to a model and an output
parser:

```python
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

# Requires OPENAI_API_KEY to be set in the environment.
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

chain = summary_prompt | llm | StrOutputParser()

summary = chain.invoke({
    "text": "The source text to summarize.",
    "length": "short",
})
```

When `invoke()` runs, LangChain fills the template, sends the resulting prompt
to `llm`, and passes the model response to `StrOutputParser`. This chain call
does make a model request.

## Main differences

| | Python f-string | LangChain `PromptTemplate` |
|---|---|---|
| Result | A regular string | A reusable LangChain template object |
| When values are inserted | When Python executes the f-string | When the template is formatted or the chain is invoked |
| Values come from | Python variables in scope | Values passed to `.format()` or `.invoke()` |
| LangChain chain integration | Must be adapted before composing as a chain | Can be composed directly with `\|` |
| Calls an AI model by itself | No | No; a chain's `.invoke()` with a model does |

## Which one to use

Use an f-string when you want to build a prompt string immediately in ordinary
Python code. Use `PromptTemplate` when you want a reusable prompt whose inputs
will be supplied later, especially when composing a LangChain pipeline.

If both snippets assign to a variable named `prompt`, the second assignment
replaces the first value. Use distinct names, such as `email_prompt` and
`summary_prompt`, when keeping both examples in the same file.
