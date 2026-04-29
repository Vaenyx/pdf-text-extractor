#!/usr/bin/env python3

import pdfplumber
import argparse
import re
import json
import sys


class Pdf:
    def __init__(self, filepath: str):
        self.__path = filepath

    @staticmethod
    def _replace_phrases(content: str, phrase_map: dict[str, str]) -> str:
        if not phrase_map:
            return content

        sorted_keys = sorted(phrase_map.keys(), key=len, reverse=True)
        replace_pattern: re.Pattern = re.compile(
            rf"\b({'|'.join(map(re.escape, sorted_keys))})\b"
        )

        parsed_content: str = replace_pattern.sub(
            lambda m: phrase_map[m.group(0)], content
        )
        return parsed_content

    def _extract_content(self, start_page: int | None, end_page: int | None) -> str:
        start_page = start_page or 1
        end_page = max(start_page, end_page) if end_page else None

        with pdfplumber.open(self.__path) as pdf:
            content: str = "\n\n".join(
                page.extract_text() or ""
                for page in pdf.pages[start_page - 1 : end_page]
            )
            return content

    def get_content(
        self, start_page: int | None, end_page: int | None, replace_map: dict[str, str]
    ) -> str:
        text_content: str = self._extract_content(
            start_page=start_page, end_page=end_page
        )
        parsed_content: str = self._replace_phrases(
            content=text_content, phrase_map=replace_map
        )
        return parsed_content


def get_args() -> tuple[str, str | None, int | None, int | None, dict]:
    parser = argparse.ArgumentParser(description="PDF Text Extractor")

    parser.add_argument("filepath", help="PDF file path")
    parser.add_argument("-o", "--out", help="Output file path")
    parser.add_argument("-s", "--start", type=int, help="Start page")
    parser.add_argument("-e", "--end", type=int, help="End page")
    parser.add_argument(
        "-r",
        "--replace",
        default="{}",
        type=json.loads,
        help=r"Replace phrases as JSON (e.g. '{\"dog\":\"cat\"}')",
    )

    args = parser.parse_args()
    return args.filepath, args.out, args.start, args.end, dict(args.replace)


def main() -> None:
    filepath, out, start, end, replace = get_args()
    pdf = Pdf(filepath=filepath)
    content = pdf.get_content(start_page=start, end_page=end, replace_map=replace)

    if not out:
        print(content)
        sys.exit(0)
    with open(out, "w") as out_file:
        out_file.write(content)


if __name__ == "__main__":
    main()
