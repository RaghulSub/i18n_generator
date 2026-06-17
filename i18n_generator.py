#!/usr/bin/env python3
import argparse
import json
import logging
from functools import partial
from multiprocessing import Pool
from pathlib import Path

from translate import translate

logger = logging.getLogger(__name__)


def translate_to_language(
    language: str,
    from_language: str,
    source_data: dict[str, str],
    output_dir: str,
) -> None:
    logger.info("Creating %s.json", language)
    translated = {}
    for key, sentence in source_data.items():
        result = translate(
            sentence=sentence,
            from_language=from_language,
            to_language=language,
        )
        translated[key] = result[0] if result else sentence

    content = json.dumps(translated, ensure_ascii=False)
    path = Path(output_dir) / f"{language}.json"
    path.write_text(content, encoding="utf-8")
    logger.info("%s.json created", language)


def translate_all(
    from_language: str,
    to_languages: list[str],
    source_file: str,
    output_dir: str = "i18n",
) -> None:
    source_data = json.loads(Path(source_file).read_text())
    Path(output_dir).mkdir(exist_ok=True)

    worker = partial(
        translate_to_language,
        from_language=from_language,
        source_data=source_data,
        output_dir=output_dir,
    )

    with Pool() as pool:
        pool.map(worker, to_languages)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate i18n translation files",
    )
    parser.add_argument(
        "--from",
        dest="from_language",
        default="en",
        help="Source language code (default: en)",
    )
    parser.add_argument(
        "--to",
        nargs="+",
        default=["de", "ta", "ja", "hi", "ko"],
        help="Target language codes (default: de ta ja hi ko)",
    )
    parser.add_argument(
        "--source",
        default="en.json",
        help="Source JSON file (default: en.json)",
    )
    parser.add_argument(
        "--output-dir",
        default="i18n",
        help="Output directory (default: i18n)",
    )
    return parser


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s: %(message)s",
    )
    parser = build_parser()
    args = parser.parse_args()
    translate_all(
        from_language=args.from_language,
        to_languages=args.to,
        source_file=args.source,
        output_dir=args.output_dir,
    )


if __name__ == "__main__":
    main()
