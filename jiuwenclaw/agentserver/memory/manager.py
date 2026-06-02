"""MemoryManager — file-based persistent memory.

Memory is stored as Markdown files under the workspace memory directory::

    memory/
    ├── MEMORY.md           # Long-term memory (loaded every session)
    ├── USER.md             # User profile (learned over time)
    └── daily_memory/       # Daily memory files (YYYY-MM-DD.md)
"""

from __future__ import annotations

import logging
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

_logger = logging.getLogger(__name__)


class MemoryManager:
    """Reads and writes persistent memory from Markdown files."""

    def __init__(self, memory_dir: Path | None = None):
        self._memory_dir = memory_dir
        self._cache: dict[str, str] = {}  # filename → content

    @property
    def memory_dir(self) -> Path:
        if self._memory_dir:
            return self._memory_dir
        from jiuwenclaw.utils import get_agent_memory_dir
        return get_agent_memory_dir()

    def load(self) -> str:
        """Load all memory files and return combined context."""
        self._cache.clear()
        memory_dir = self.memory_dir
        memory_dir.mkdir(parents=True, exist_ok=True)

        parts: list[str] = []

        # Load MEMORY.md (long-term)
        long_term = memory_dir / "MEMORY.md"
        if long_term.exists():
            content = long_term.read_text(encoding="utf-8").strip()
            if content and not content.startswith("# This file stores"):
                self._cache["MEMORY.md"] = content
                parts.append(content)

        # Load USER.md (user profile)
        user_file = memory_dir / "USER.md"
        if user_file.exists():
            content = user_file.read_text(encoding="utf-8").strip()
            if content and not content.startswith("(Your profile"):
                self._cache["USER.md"] = content
                parts.append(content)

        # Load daily memory files
        daily_dir = memory_dir / "daily_memory"
        if daily_dir.exists():
            for f in sorted(daily_dir.glob("*.md"), reverse=True)[:10]:
                content = f.read_text(encoding="utf-8").strip()
                if content:
                    self._cache[f.name] = content
                    parts.append(f"[{f.stem}] {content}")

        _logger.info("Loaded %d memory files", len(self._cache))
        return "\n\n".join(parts)

    def get_context(self) -> str:
        """Return cached memory content, loading if needed."""
        if not self._cache:
            return self.load()
        return "\n\n".join(self._cache.values())

    def remember(self, fact: str) -> None:
        """Save a fact to today's daily memory file."""
        today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
        daily_dir = self.memory_dir / "daily_memory"
        daily_dir.mkdir(parents=True, exist_ok=True)

        daily_file = daily_dir / f"{today}.md"
        entry = f"- {fact}\n"
        with open(daily_file, "a", encoding="utf-8") as f:
            f.write(entry)

        self._cache[f"{today}.md"] = daily_file.read_text(encoding="utf-8").strip()
        _logger.info("Saved memory to %s", daily_file)

    def update_user(self, fact: str) -> None:
        """Append a fact to USER.md."""
        user_file = self.memory_dir / "USER.md"
        user_file.parent.mkdir(parents=True, exist_ok=True)

        entry = f"- {fact}\n"
        with open(user_file, "a", encoding="utf-8") as f:
            f.write(entry)

        self._cache["USER.md"] = user_file.read_text(encoding="utf-8").strip()
        _logger.info("Updated USER.md: %s", fact)

    def recall(self, query: str) -> str:
        """Search all loaded memory for a query. Simple substring match."""
        results: list[str] = []
        for filename, content in self._cache.items():
            if query.lower() in content.lower():
                results.append(f"[{filename}] {content[:300]}")
        if not results:
            return "No matching memory found."
        return "\n".join(results)
