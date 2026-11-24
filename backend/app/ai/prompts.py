from langchain_core.prompts import PromptTemplate

# Prompt for classifying user developer intent
QUERY_CLASSIFIER_PROMPT = PromptTemplate(
    input_variables=["query"],
    template="""You are a code assistant classifier.
Classify the following query into one of the categories:
- 'explanation' (e.g. how does X work, what is this function)
- 'debug' (e.g. why is this error happening, find bug in Y)
- 'review' (e.g. review this file, security check, performance check)
- 'general' (e.g. general codebase questions, architecture overview)

Query: {query}
Respond ONLY with one word: explanation, debug, review, or general."""
)

# Prompt for query rewriter when initial retrieval lacked relevant context
QUERY_REWRITER_PROMPT = PromptTemplate(
    input_variables=["query", "context_notes"],
    template="""You are an expert software developer and search query optimizer.
The user asked: "{query}"
The previous retrieval did not yield sufficient context: {context_notes}

Rewrite this query into 2-3 specific technical keywords, class/function identifiers, or conceptual terms to search a code repository vector index effectively.
Output only the optimized query."""
)

# Context relevance evaluation
CONTEXT_EVALUATOR_PROMPT = PromptTemplate(
    input_variables=["query", "retrieved_code"],
    template="""Evaluate whether the retrieved code snippets are relevant and sufficient to answer the developer's question.

Query: {query}

Retrieved Code:
{retrieved_code}

Respond with:
RELEVANT: [YES/NO]
REASON: [Brief reason]"""
)

# Response generation grounded strictly in retrieved code
RESPONSE_GENERATOR_PROMPT = PromptTemplate(
    input_variables=["query", "query_type", "context"],
    template="""You are GITI, an AI-powered GitHub Codebase Assistant.
Your task is to answer the developer's query accurately, based strictly on the provided codebase context.

Guidelines:
1. Ground your answer in the retrieved source code evidence.
2. Explicitly cite file paths and line numbers (e.g., `src/auth.py:24-45`).
3. If the retrieved context is insufficient or evidence is not found, clearly state that rather than hallucinating code details.
4. Keep the response crisp, structured, and developer-friendly.

Query Type: {query_type}
Developer Query: {query}

Codebase Context:
{context}

Answer:"""
)

# Source verification prompt
SOURCE_VERIFIER_PROMPT = PromptTemplate(
    input_variables=["answer", "evidence_files"],
    template="""Verify that the citations and code references in this answer exist in the provided retrieved evidence files list.
Evidence files present: {evidence_files}

Draft Answer:
{answer}

If the answer references non-existent files or fabricated lines, adjust or annotate it.
Provide the verified answer:"""
)
