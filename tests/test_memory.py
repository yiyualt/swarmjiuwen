"""Tests for MemoryManager."""

import tempfile
from pathlib import Path

from jiuwenclaw.agentserver.memory.manager import MemoryManager


class TestMemoryManager:
    def test_empty_memory_returns_empty(self):
        with tempfile.TemporaryDirectory() as tmp:
            mgr = MemoryManager(Path(tmp))
            ctx = mgr.get_context()
            assert ctx == ""

    def test_loads_memory_md(self):
        with tempfile.TemporaryDirectory() as tmp:
            mem_dir = Path(tmp)
            mem_dir.mkdir(parents=True, exist_ok=True)
            (mem_dir / "MEMORY.md").write_text("User prefers Python.")
            (mem_dir / "USER.md").write_text("- Name: Alex")

            mgr = MemoryManager(mem_dir)
            ctx = mgr.get_context()

            assert "User prefers Python" in ctx
            assert "Name: Alex" in ctx

    def test_loads_daily_memory(self):
        with tempfile.TemporaryDirectory() as tmp:
            mem_dir = Path(tmp)
            daily = mem_dir / "daily_memory"
            daily.mkdir(parents=True)
            (daily / "2026-01-01.md").write_text("- Did a thing")

            mgr = MemoryManager(mem_dir)
            ctx = mgr.load()

            assert "Did a thing" in ctx

    def test_remember_saves_fact(self):
        with tempfile.TemporaryDirectory() as tmp:
            mem_dir = Path(tmp)
            daily = mem_dir / "daily_memory"
            daily.mkdir(parents=True)

            mgr = MemoryManager(mem_dir)
            mgr.remember("User's favorite color is blue")

            # Check file was created
            files = list(daily.glob("*.md"))
            assert len(files) == 1

            content = files[0].read_text()
            assert "favorite color is blue" in content

    def test_recall_finds_query(self):
        with tempfile.TemporaryDirectory() as tmp:
            mem_dir = Path(tmp)
            mem_dir.mkdir(parents=True, exist_ok=True)
            (mem_dir / "MEMORY.md").write_text("User prefers Python. Likes coffee.")

            mgr = MemoryManager(mem_dir)
            mgr.load()

            result = mgr.recall("Python")
            assert "Python" in result

            result = mgr.recall("nonexistent")
            assert "No matching memory" in result

    def test_update_user(self):
        with tempfile.TemporaryDirectory() as tmp:
            mem_dir = Path(tmp)
            mem_dir.mkdir(parents=True, exist_ok=True)

            mgr = MemoryManager(mem_dir)
            mgr.update_user("Name: Alex")

            user_file = mem_dir / "USER.md"
            assert user_file.exists()
            assert "Name: Alex" in user_file.read_text()

    def test_cached_context_avoids_reload(self):
        with tempfile.TemporaryDirectory() as tmp:
            mem_dir = Path(tmp)
            mem_dir.mkdir(parents=True, exist_ok=True)
            (mem_dir / "MEMORY.md").write_text("Fact A")

            mgr = MemoryManager(mem_dir)
            ctx1 = mgr.get_context()

            # Change file on disk
            (mem_dir / "MEMORY.md").write_text("Fact B")

            # Should still return cached
            ctx2 = mgr.get_context()
            assert "Fact A" in ctx2
            assert "Fact B" not in ctx2

            # After reload
            ctx3 = mgr.load()
            assert "Fact B" in ctx3
