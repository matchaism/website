from typing import Optional, List, Dict
import logging
import requests
import argparse
from requests.exceptions import Timeout, ConnectionError, HTTPError, RequestException
from bs4 import BeautifulSoup
from collections import defaultdict
import json
from pathlib import Path


logger = logging.getLogger(__name__)


def get_hatena_page(url: str, timeout: int = 30) -> str:
    try:
        response = requests.get(url, timeout=timeout)
        logger.info(f"GET {url}")

        response.raise_for_status()
        return response.text

    except Timeout:
        logger.exception("リクエストがタイムアウトしました")
        raise

    except ConnectionError:
        logger.exception("サーバに接続できませんでした")
        raise

    except HTTPError as e:
        status = e.response.status_code if e.response else "unknown"
        logger.exception(f"HTTPエラーが発生しました: {status}")
        raise

    except RequestException as e:
        logger.exception(f"リクエストに失敗しました: {e}")
        raise


def parse_html(html_doc: str) -> BeautifulSoup:
    return BeautifulSoup(html_doc, "html.parser")


def extract_title_from_hatena_page(soup: BeautifulSoup) -> Optional[str]:
    tag = soup.find("meta", property="og:title")
    if tag and "content" in tag.attrs:
        return tag["content"][:-11]
    return None


def extract_article_url_from_hatena_page(soup: BeautifulSoup) -> Optional[str]:
    tag = soup.find("meta", property="og:url")
    if tag and "content" in tag.attrs:
        return tag["content"]
    return None


def extract_thumbnail_url_from_hatena_page(soup: BeautifulSoup) -> Optional[str]:
    tag = soup.find("meta", property="og:image")
    if tag and "content" in tag.attrs:
        return tag["content"]
    return None


def extract_published_date_from_hatena_page(soup: BeautifulSoup) -> Optional[str]:
    date_div = soup.select_one("div.date.entry-date.first")
    if not date_div:
        return None

    tag_year = date_div.select_one("span.date-year")
    tag_month = date_div.select_one("span.date-month")
    tag_day = date_div.select_one("span.date-day")

    if tag_year and tag_month and tag_day:
        return f"{tag_year.text}/{tag_month.text}/{tag_day.text}"

    return None


def validate_article_info(
    article_info_list: List[Dict[str, Optional[str]]],
) -> List[Dict[str, str]]:
    validated: List[Dict[str, str]] = []

    for article_info in article_info_list:
        if all(
            article_info.get(key)
            for key in [
                "title",
                "article_url",
                "thumbnail_url",
                "published_date",
            ]
        ):
            validated.append(article_info)  # type: ignore[arg-type]
        else:
            logger.warning(f"値が不正な article_info を除外しました: {article_info}")

    return validated


def sort_article_info_list(
    article_info_list: List[Dict[str, str]],
    reverse: bool = True,
) -> List[Dict[str, str]]:
    return sorted(
        article_info_list,
        key=lambda x: x["published_date"],
        reverse=reverse,
    )


def separate_article_info_list_by_published_year(
    article_info_list: List[Dict[str, str]],
) -> Dict[str, List[Dict[str, str]]]:
    separated: Dict[str, List[Dict[str, str]]] = defaultdict(list)

    for article_info in article_info_list:
        year = article_info["published_date"].split("/")[0]
        separated[year].append(article_info)

    return separated


def save_article_info_list_as_json(
    article_info_list: List[Dict[str, str]],
    path: Path,
) -> None:
    with path.open(mode="w", encoding="utf-8") as json_file:
        json.dump(article_info_list, json_file, ensure_ascii=False, indent=2)


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    logger.info("----- Started -----")

    parser = argparse.ArgumentParser()
    parser.add_argument("url", type=str, nargs="+", help="Hatena article URLs")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path("data/archive"),
        help="JSON output directory (default: data/archive)",
    )
    args = parser.parse_args()

    output_dir: Path = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    article_info_list: List[Dict[str, Optional[str]]] = []

    for url in args.url:
        response_text = get_hatena_page(url)
        soup = parse_html(response_text)

        article_info_list.append(
            {
                "title": extract_title_from_hatena_page(soup),
                "article_url": extract_article_url_from_hatena_page(soup),
                "thumbnail_url": extract_thumbnail_url_from_hatena_page(soup),
                "published_date": extract_published_date_from_hatena_page(soup),
            }
        )

    validated = validate_article_info(article_info_list)
    sorted_list = sort_article_info_list(validated)
    separated = separate_article_info_list_by_published_year(sorted_list)

    for year, articles in separated.items():
        save_article_info_list_as_json(
            articles,
            output_dir / f"{year}.json",
        )

    logger.info("----- Finished -----")


if __name__ == "__main__":
    main()
