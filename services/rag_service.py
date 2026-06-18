
import google.generativeai as genai

from config import Config

from services.vector_store_service import (
    load_vector_store
)

from services.markdown_service import (
    render_markdown
)


genai.configure(
    api_key=
    Config.GEMINI_API_KEY
)

MODEL = genai.GenerativeModel(
    "gemini-2.5-flash"
)


def ask_rag(
    question: str
):

    try:

        # ======================
        # LOAD VECTOR STORE
        # ======================

        vectorstore = (
            load_vector_store()
        )

        retriever = (
            vectorstore
            .as_retriever(
                search_kwargs={
                    "k": 5
                }
            )
        )

        documents = (
            retriever.invoke(
                question
            )
        )

        if not documents:

            return render_markdown(
                """
### No Relevant Information Found

The uploaded document does not contain information related to your question.
"""
            )

        # ======================
        # BUILD CONTEXT
        # ======================

        context = "\n\n".join(

            doc.page_content

            for doc in documents

        )

        # ======================
        # PROMPT
        # ======================


        prompt = f"""
        You are ChatGPT, an advanced AI assistant.

        You have access to an uploaded document.

        The document is additional context, not your only source of knowledge.

        Instructions:

        1. First determine whether the user's question is related to the uploaded document.

        2. If the question is related to the uploaded document:
        - Use the document as your primary source.
        - Quote or summarize the document accurately.
        - If the document is incomplete, you may supplement with general knowledge and clearly distinguish it.

        3. If the question is NOT related to the uploaded document:
        - Ignore the document.
        - Answer normally using your own knowledge.

        4. Never invent facts that supposedly come from the uploaded document.

        5. Respond naturally exactly like ChatGPT.

        6. For coding questions:
        - Explain briefly.
        - Write clean production-quality code.
        - Use Markdown.
        - Include examples when useful.

        7. For resumes:
        - Calculate an estimated ATS score.
        - Suggest improvements.
        - Rewrite sections when requested.
        - Highlight missing skills.

        8. For documents:
        - Summarize
        - Compare
        - Explain
        - Translate
        - Extract tables
        - Extract key points

        9. Use proper Markdown:
        - Headings
        - Bullet lists
        - Tables
        - Code blocks

        Uploaded Document:

        {context}

        User Question:

        {question}

        Answer:
        """



        # ======================
        # GEMINI
        # ======================

        response = (
            MODEL.generate_content(
                prompt
            )
        )

        if (
            not response
            or
            not response.text
        ):

            return render_markdown(
                """
### No Response Generated

Gemini did not return any answer.
"""
            )

        return render_markdown(
            response.text
        )

    except FileNotFoundError:

        return render_markdown(
            """
### No Document Indexed

Please upload a file first.
"""
        )

    except Exception as e:

        return render_markdown(
            f"""
### RAG Error

{str(e)}
"""
        )

