from typing import Optional, List, Dict
import logging
import argparse
from pathlib import Path
from string import Template
from article import Article, ArticleList
import config


logger = logging.getLogger(__name__)


def generate_latest_archive_page(
    article_list: ArticleList,
    path: Path,
) -> str:
    archive_page_source = ""

    for article in article_list:
        with open(path, mode="r", encoding="utf-8") as f:
            t = Template(f.read() + "\n\n")
            archive_page_source += t.substitute(
                title=article.title,
                article_url=article.url,
                thumbnail_url=article.thumbnail_url,
                published_date=article.published_date,
                site_icon=config.SITE_ICON.get(article.site_name, ""),
            )

    archive_page_source = (
        '<div class="container-fluid my-4">\n\n' + archive_page_source + "</div>\n"
    )

    return archive_page_source


def save_archive_page(
    archive_page_source: str,
    path: Path,
) -> None:
    with open(path, mode="w") as f:
        f.write(archive_page_source)


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    logger.info("----- Started -----")

    parser = argparse.ArgumentParser()
    parser.add_argument("--sites", type=str, default=config.SITE, nargs="+")
    parser.add_argument("--years", type=str, default=config.YEAR, nargs="+")
    args = parser.parse_args()

    for year in args.years:
        article_list_by_year = ArticleList()

        for site_name in args.sites:
            article_list_path: Path = Path(
                Path(config.ARTICLE_LIST_DIRECTORY_PATH[site_name])
                / f"{site_name}_{year}.json"
            )
            article_list_by_year.concat(ArticleList(article_list_path))

        article_list_by_year.sort_by_published_date()

        archive_page_source = generate_latest_archive_page(
            article_list_by_year,
            Path(config.ARCHIVE_CARD_TEMPLATE_PATH),
        )

        output_path = Path(Path(config.ARCHIVE_PAGE_DIRECTORY_PATH) / f"{year}.html")
        logger.info(f"Save {output_path}")
        save_archive_page(archive_page_source, output_path)

    logger.info("----- Finished -----")


if __name__ == "__main__":
    main()
