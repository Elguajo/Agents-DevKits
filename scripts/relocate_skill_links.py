#!/usr/bin/env python3
"""Keep copied skills' external Markdown references attached to their source."""

from pathlib import Path
import argparse
import re
from urllib.parse import unquote, urlsplit


MARKDOWN_LINK = re.compile(r"(\[[^\]\n]*\]\()(<[^>\n]+>|[^\s)\n]+)(\))")


def relocate_links(source: Path, destination: Path) -> None:
    source = source.resolve()
    if destination.is_symlink() or source == destination.resolve():
        raise ValueError("Refusing to rewrite links through the source or a symbolic link")
    for source_file in source.rglob("*.md"):
        target_file = destination / source_file.relative_to(source)
        content = source_file.read_bytes().decode("utf-8")

        def replace(match: re.Match[str]) -> str:
            link = match[2].removeprefix("<").removesuffix(">")
            parsed = urlsplit(link)
            if parsed.scheme or parsed.netloc or not parsed.path or parsed.path.startswith("/"):
                return match[0]
            reference = (source_file.parent / unquote(parsed.path)).resolve()
            if reference.is_relative_to(source) or not reference.exists():
                return match[0]
            # Absolute paths work for both native Windows and POSIX readers.
            # Angle brackets preserve spaces in checkout paths.
            absolute = reference.as_posix()
            if parsed.fragment:
                absolute += f"#{parsed.fragment}"
            return f"{match[1]}<{absolute}>{match[3]}"

        updated = MARKDOWN_LINK.sub(replace, content)
        if updated != content:
            target_file.write_bytes(updated.encode("utf-8"))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    relocate_links(args.source, args.destination)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
