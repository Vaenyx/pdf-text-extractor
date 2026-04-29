#!/usr/bin/env python3

from argparse import ArgumentParser
from pdfplumber import open as open_pdf
from typing import Literal


def extract_text_from_pdf(
    input_pdf: str,
    output_txt: str,
    start_page: int,
    end_page: int | Literal["all"],
    replace_phrases: dict[str, str],
) -> None:
    with open_pdf(input_pdf) as pdf:
        end_page_num = len(pdf.pages) if end_page == "all" else int(end_page)

        print(
            f"Started text extraction of pdf '{input_pdf}'\nExtracting pages {start_page} to {end_page_num}{" (last page)" if end_page == "all" else ""}:"
        )
        with open(output_txt, "w+", encoding="utf-8") as out:
            for page_num in range(start_page - 1, end_page_num):
                if page_num != start_page - 1:
                    out.write("\n")

                page = pdf.pages[page_num]
                text = page.extract_text()

                if not text:
                    continue

                for old, new in replace_phrases.items():
                    text = text.replace(old, new)

                out.write(text)
                print(
                    f"Extracted page {page_num+1}/{end_page_num} ({int((page_num+1-start_page)/(end_page_num-start_page)*100)}%)\r",
                    flush=True,
                )

    print("Extraction complete.")


def parse_replace_argument(rep: str) -> dict:
    """
    Format: "old1~new1;old2~new2"
    """
    if not rep:
        return {}

    return dict(
        pair.split("~", 1) for pair in rep.split(";", some_string) if "~" in pair
    )


if __name__ == "__main__":
    parser = ArgumentParser(description="PDF Text Extractor")
    parser.add_argument("-pdf", required=True, help="Path to PDF file")
    parser.add_argument("-out", required=True, help="Output text file path")
    parser.add_argument("-s", type=int, default=1, help="Start page (default=1)")
    parser.add_argument("-e", default="all", help="End page number or 'all'")
    parser.add_argument(
        "-re", help="Replace phrases: 'old1~new1;old2~new2'", default=None
    )

    args = parser.parse_args()

    replace_dict = parse_replace_argument(rep=args.re)

    extract_text_from_pdf(
        input_pdf=args.pdf,
        output_txt=args.out,
        start_page=args.s,
        end_page=args.e,
        replace_phrases=replace_dict,
    )
