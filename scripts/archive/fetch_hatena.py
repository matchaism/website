from typing import Optional, List, Dict
import logging
import requests
import argparse
from requests.exceptions import Timeout, ConnectionError, HTTPError, RequestException
from bs4 import BeautifulSoup
import os
from pathlib import Path
from article import Article, ArticleList
import config

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


def extract_url_from_hatena_page(soup: BeautifulSoup) -> Optional[str]:
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


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    logger.info("----- Started -----")

    parser = argparse.ArgumentParser()
    parser.add_argument("urls", type=str, nargs="+", help="Hatena article URLs")
    args = parser.parse_args()

    output_dir: Path = Path(config.ARTICLE_LIST_DIRECTORY_PATH["hatena"])
    output_dir.mkdir(parents=True, exist_ok=True)

    article_list_arg = ArticleList()

    for url in args.urls:
        response_text = get_hatena_page(url)
        soup = parse_html(response_text)

        article_list_arg.append(
            Article(
                **{
                    "title": extract_title_from_hatena_page(soup),
                    "url": extract_url_from_hatena_page(soup),
                    "thumbnail_url": extract_thumbnail_url_from_hatena_page(soup),
                    "published_date": extract_published_date_from_hatena_page(soup),
                    "site_name": "hatena",
                }
            )
        )

    for year in config.YEAR:
        output_path: Path = Path(output_dir / f"hatena_{year}.json")

        article_list_saved = ArticleList(
            output_path if os.path.isfile(output_path) else None
        )

        article_list_by_year = article_list_arg.get_by_year(year)

        article_list_by_year.concat(article_list_saved)
        article_list_by_year.remove_duplicate_url()
        article_list_by_year.sort_by_published_date()

        logger.info(f"Save {output_path}")
        article_list_by_year.save_as_json(output_path)

    logger.info("----- Finished -----")


if __name__ == "__main__":
    main()
