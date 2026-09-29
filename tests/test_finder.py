from utils.finder import SearchError, search_document


def test_text_search_returns_context_and_counts():
    result = search_document(b"Signal one\nno match\nsignal signal", "log.txt", "signal")
    assert result["occurrences"] == 3
    assert result["matchedUnits"] == 2
    assert [item["number"] for item in result["results"]] == [1, 3]


def test_whole_word_excludes_partial_matches():
    result = search_document(b"orbit orbital orbit", "log.txt", "orbit", whole_word=True)
    assert result["occurrences"] == 2


def test_unsupported_document_is_rejected():
    try:
        search_document(b"content", "archive.zip", "content")
    except SearchError as error:
        assert "Unsupported format" in str(error)
    else:
        raise AssertionError("Unsupported extension was accepted")
