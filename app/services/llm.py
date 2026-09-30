from app.services.rag import rag_engine


def answer_question(question: str, component: str = None):

    question_lower = question.lower()

    # --------------------------------------------------
    # Determine component
    # --------------------------------------------------

    if component:
        selected_component = component

    elif any(word in question_lower for word in [
        "mcb",
        "miniature circuit breaker",
        "circuit breaker"
    ]):
        selected_component = "MCB"

    elif "contactor" in question_lower:
        selected_component = "Contactor"

    elif "relay" in question_lower:
        selected_component = "Relay"

    else:
        selected_component = None

    # --------------------------------------------------
    # Retrieve component
    # --------------------------------------------------

    if selected_component:

        results = rag_engine.search(
            selected_component,
            top_k=3
        )

    else:

        results = rag_engine.search(
            question,
            top_k=3
        )

    if not results:
        return "I could not find relevant engineering information."

    # --------------------------------------------------
    # Choose the best matching component
    # --------------------------------------------------

    document = results[0]

    # --------------------------------------------------
    # Question-aware answer
    # --------------------------------------------------

    if any(word in question_lower for word in [
        "maintain",
        "maintenance",
        "service",
        "inspect",
        "inspection"
    ]):

        return (
            f"{document['component']} maintenance:\n\n"
            f"{document['maintenance']}"
        )

    elif any(word in question_lower for word in [
        "safe",
        "safety",
        "danger",
        "precaution"
    ]):

        return (
            f"Safety guidance for {document['component']}:\n\n"
            f"{document['safety']}"
        )

    elif any(word in question_lower for word in [
        "trip",
        "tripping",
        "fault",
        "problem",
        "issue",
        "not working"
    ]):

        return (
            f"Recommended action for {document['component']}:\n\n"
            f"{document['action']}"
        )

    elif any(word in question_lower for word in [
        "what is",
        "what does",
        "function",
        "purpose",
        "used for"
    ]):

        return (
            f"{document['component']}:\n\n"
            f"{document['description']}"
        )

    else:

        return (
            f"{document['component']}\n\n"
            f"{document['description']}\n\n"
            f"Safety:\n"
            f"{document['safety']}\n\n"
            f"Maintenance:\n"
            f"{document['maintenance']}\n\n"
            f"Recommended action:\n"
            f"{document['action']}"
        )