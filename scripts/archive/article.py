from typing import Optional, List, Dict, Self
import json
from pathlib import Path


class Article:
    def __init__(
        self,
        title: str = None,
        url: str = None,
        thumbnail_url: str = None,
        published_date: str = None,
        site_name: str = None,
    ):
        self.title = title
        self.url = url
        self.thumbnail_url = thumbnail_url
        self.published_date = published_date
        self.site_name = site_name

    def get_dict(self) -> Dict[str, str]:
        return {
            "title": self.title,
            "url": self.url,
            "thumbnail_url": self.thumbnail_url,
            "published_date": self.published_date,
            "site_name": self.site_name,
        }


class ArticleList:
    def __init__(self, path: Path = None):
        self.article_list: list[Article] = []
        if path:
            self.load(path)

    def load(self, path: Path) -> None:
        with open(path, mode="r", encoding="utf-8") as json_file:
            article_dict_list = json.load(json_file)
            self.article_list = [
                Article(**article_dict) for article_dict in article_dict_list
            ]

    def save_as_json(self, path: Path) -> None:
        article_dict_list = [article.get_dict() for article in self.article_list]
        with open(path, mode="w", encoding="utf-8") as json_file:
            json.dump(article_dict_list, json_file, ensure_ascii=False, indent=2)

    def append(self, article: Article) -> None:
        self.article_list.append(article)

    def concat(self, article_list: Self) -> None:
        self.article_list.extend(article_list)

    def get_by_year(self, year: str) -> Self:
        matched_article_list = ArticleList()
        for article in self.article_list:
            if article.published_date.split("/")[0] != year:
                continue
            matched_article_list.append(article)
        return matched_article_list

    def sort_by_published_date(self, reverse: bool = True) -> None:
        self.article_list.sort(
            key=lambda article: article.published_date,
            reverse=reverse,
        )

    def remove_duplicate_url(self, remains_latest: bool = True) -> None:
        self.sort_by_published_date(not remains_latest)
        unique_items = {article.url: article for article in self.article_list}
        self.article_list = list(unique_items.values())

    def __iter__(self):
        return iter(self.article_list)
