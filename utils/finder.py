"""Document extraction and contextual text search."""

from __future__ import annotations

import io
import re
from pathlib import Path

SUPPORTED_EXTENSIONS = {".txt", ".md", ".csv", ".log", ".json", ".pdf", ".docx"}


class SearchError(ValueError):
    """A document or query cannot be searched safely."""


def _decode_text(payload: bytes) -> str:
    for encoding in ("utf-8-sig", "utf-8", "cp1252", "latin-1"):
        try:
            return payload.decode(encoding)
        except UnicodeDecodeError:
            continue
    raise SearchError("This text encoding is not supported.")


def _extract_units(payload: bytes, extension: str) -> tuple[str, list[str]]:
    if extension in {".txt", ".md", ".csv", ".log", ".json"}:
        return "line", _decode_text(payload).splitlines()
    if extension == ".pdf":
        try:
            from pypdf import PdfReader
            reader = PdfReader(io.BytesIO(payload))
            return "page", [(page.extract_text() or "") for page in reader.pages]
        except Exception as exc:
            raise SearchError("The PDF could not be read. It may be encrypted or damaged.") from exc
    if extension == ".docx":
        try:
            from docx import Document
            document = Document(io.BytesIO(payload))
            return "paragraph", [paragraph.text for paragraph in document.paragraphs]
        except Exception as exc:
            raise SearchError("The DOCX document could not be read.") from exc
    raise SearchError("Unsupported format. Use TXT, MD, CSV, LOG, JSON, PDF, or DOCX.")


def _compact(text: str, match_start: int, match_end: int, radius: int = 115) -> str:
    clean = " ".join(text.split())
    if len(clean) <= radius * 2:
        return clean
    needle = " ".join(text[match_start:match_end].split())
    position = max(clean.casefold().find(needle.casefold()), 0)
    start = max(position - radius, 0)
    end = min(position + len(needle) + radius, len(clean))
    return ("…" if start else "") + clean[start:end] + ("…" if end < len(clean) else "")


def search_document(payload: bytes, filename: str, query: str, *, case_sensitive: bool = False,
                    whole_word: bool = False, limit: int = 50) -> dict:
    """Search a supported in-memory document and return contextual matches."""
    extension = Path(filename).suffix.lower()
    if extension not in SUPPORTED_EXTENSIONS:
        raise SearchError("Unsupported format. Use TXT, MD, CSV, LOG, JSON, PDF, or DOCX.")
    if not payload:
        raise SearchError("The selected document is empty.")

    unit, units = _extract_units(payload, extension)
    flags = 0 if case_sensitive else re.IGNORECASE
    escaped = re.escape(query)
    pattern = re.compile(rf"(?<!\w){escaped}(?!\w)" if whole_word else escaped, flags)
    matches, matched_units, occurrence_count = [], 0, 0
    for index, content in enumerate(units, start=1):
        found = list(pattern.finditer(content))
        if not found:
            continue
        matched_units += 1
        occurrence_count += len(found)
        if len(matches) < limit:
            first = found[0]
            matches.append({"number": index, "occurrences": len(found),
                            "preview": _compact(content, first.start(), first.end())})

    return {"filename": Path(filename).name, "query": query, "unit": unit,
            "scannedUnits": len(units), "matchedUnits": matched_units,
            "occurrences": occurrence_count, "results": matches,
            "truncated": matched_units > limit}
