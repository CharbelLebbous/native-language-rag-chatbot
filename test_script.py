# test_script.py

# ✅ Utilities for pretty console output
import pprint

# ✅ Your local modules: CohereClient for direct calls, query_index for the main pipeline
from cohere_client import CohereClient
from query_engine import query_index

# ✅ Initialize the Cohere client if you ever want to test its raw methods directly
cohere_client = CohereClient()

# ✅ Handy pretty printer for nice output formatting
pp = pprint.PrettyPrinter(indent=2)


def test_single_turn():
    """
    ✅ Test case 1:
    Simple single-turn question → verifies the system answers correctly
    without any chat history.
    """
    print("\n=== TEST: Single-turn ===")
    question = "Who is Charbel?"
    answer, sources = query_index(question, chat_history=[])
    print(f"Question: {question}")
    print(f"Answer: {answer}")
    print("Sources:")
    pp.pprint(sources)


def test_cross_doc():
    """
    ✅ Test case 2:
    Cross-document scenario → ask about one doc first, then another doc,
    while maintaining the chat history.
    """
    print("\n=== TEST: Cross-doc ===")
    q1 = "Who is Charbel?"
    q2 = "What is The Phoenix Alliance?"
    history = []

    # 🔹 First question
    answer1, sources1 = query_index(q1, chat_history=history)
    print(f"Q1: {q1}")
    print(f"A1: {answer1}")
    pp.pprint(sources1)

    # Add first Q&A to history
    history.append({"role": "user", "content": q1})
    history.append({"role": "assistant", "content": answer1})

    # 🔹 Second question about a different doc
    answer2, sources2 = query_index(q2, chat_history=history)
    print(f"Q2: {q2}")
    print(f"A2: {answer2}")
    pp.pprint(sources2)


def test_followup():
    """
    ✅ Test case 3:
    Follow-up scenario → ask a follow-up question that depends on the first answer,
    to check if the model handles conversation context correctly.
    """
    print("\n=== TEST: Followup ===")
    q1 = "Who is Charbel?"
    q2 = "What is his phone number?"
    history = []

    # 🔹 First question
    answer1, sources1 = query_index(q1, chat_history=history)
    print(f"Q1: {q1}")
    print(f"A1: {answer1}")
    pp.pprint(sources1)

    # Add to history
    history.append({"role": "user", "content": q1})
    history.append({"role": "assistant", "content": answer1})

    # 🔹 Follow-up question that relies on previous turn
    answer2, sources2 = query_index(q2, chat_history=history)
    print(f"Q2: {q2}")
    print(f"A2: {answer2}")
    pp.pprint(sources2)


# ✅ Run all tests when executed directly
if __name__ == "__main__":
    test_single_turn()
    test_cross_doc()
    test_followup()
