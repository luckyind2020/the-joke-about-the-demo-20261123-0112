#!/usr/bin/env python3
"""The Demo Joke — a one-line joke about working beside AI coding agents.

The program keeps a small book of original one-liners and deterministically
picks one for today, then writes it to /output/entry.txt.

Deterministic by design: the pick depends only on the calendar date, so the
same run on the same day always produces the same joke, and no network or
randomness is involved.
"""

from __future__ import annotations

import datetime
import pathlib
import sys

OUTPUT_PATH = pathlib.Path("/output/entry.txt")
MIN_LENGTH = 1
MAX_LENGTH = 280


class JokeBook:
    """A tiny book of original one-liners about demos and AI coding agents."""

    def __init__(self) -> None:
        self._lines = [
            (
                "I don't pair-program with an AI agent — I watch it write "
                "500 lines in 30 seconds, then spend the whole demo "
                "explaining why none of them were the lines I asked for."
            ),
            (
                "My AI coding agent fixed the bug before I finished "
                "describing it, then confidently introduced three new ones "
                "during the live demo, like a magician who only knows the "
                "disappearing trick."
            ),
            (
                "Working beside an AI coding agent is great: the demo is "
                "always ready on time — it's just that 'ready' turns out "
                "to have been a figure of speech."
            ),
        ]

    def __len__(self) -> int:
        return len(self._lines)

    def pick(self, day: datetime.date) -> str:
        """Deterministically pick one line for the given day.

        A simple day-based rotation: the index is derived from the
        day-of-year, so the choice is stable within a day and rotates
        across days without any randomness.
        """
        if not self._lines:
            raise ValueError("joke book is empty")
        index = (day.timetuple().tm_yday * 7) % len(self._lines)
        return self._lines[index]

    def validate(self, line: str) -> str:
        """Return the line if it meets the entry rules, else raise."""
        text = line.strip()
        if not text:
            raise ValueError("joke must not be only whitespace")
        if "\n" in text or "\r" in text:
            raise ValueError("joke must be a single line")
        if not MIN_LENGTH <= len(text) <= MAX_LENGTH:
            raise ValueError(
                f"joke must be {MIN_LENGTH}-{MAX_LENGTH} characters, "
                f"got {len(text)}"
            )
        return text


def main(argv: list[str] | None = None) -> int:
    today = datetime.date.today()
    book = JokeBook()
    joke = book.validate(book.pick(today))

    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_PATH.write_text(joke + "\n", encoding="utf-8")

    # Round-trip check: what is on disk must be exactly the joke we chose,
    # and the whole file (trailing newline included) must stay in bounds.
    on_disk = OUTPUT_PATH.read_text(encoding="utf-8")
    if on_disk.strip() != joke:
        raise RuntimeError("round-trip check failed: file differs from joke")
    if not MIN_LENGTH <= len(on_disk) <= MAX_LENGTH + 1:
        raise ValueError(
            f"written file must be {MIN_LENGTH}-{MAX_LENGTH + 1} "
            f"characters, got {len(on_disk)}"
        )

    print(f"Wrote {len(joke)} characters to {OUTPUT_PATH}")
    print(joke)
    return 0


if __name__ == "__main__":
    sys.exit(main())
