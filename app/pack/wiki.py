import wikipedia


def wiki_summary(search_term: str) -> str:
    search_term = format_as_title(search_term)
    searches = wikipedia.search(search_term)
    if search_term in searches:
        return wikipedia.summary(search_term, auto_suggest=False)
    else:
        response = f"No wikipedia entry for {search_term}."
        return response


def format_as_title(search_term: str) -> str:
    title_words = []
    search_term = search_term.replace("_", " ")
    searched_words = search_term.split()
    for word in searched_words:
        if word == searched_words[0] or (
            not word.startswith("(")
            and word.lower() not in ["of", "and", "if", "on", "a"]
        ):
            word = word.capitalize()
        else:
            word = word.lower()
        title_words.append(word)

    return " ".join(title_words)
