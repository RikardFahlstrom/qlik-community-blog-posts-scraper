import datetime
from dataclasses import dataclass
from typing import List

import pandas as pd
import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine


@dataclass
class Blogpost:
    author: str
    title: str
    url: str
    publish_date: datetime.date
    source: str
    likes: int = 0
    views: int = 0
    scraped_date: datetime.date = datetime.date.today()


def query_page_with_blog_posts(url_to_scrape: str) -> BeautifulSoup:
    headers_dict = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0 Safari/537.36"}
    r = requests.get(url_to_scrape, headers=headers_dict)

    assert r.status_code == 200

    return BeautifulSoup(r.text, "html.parser")


def flatten_nested_list(t):
    return [item for sublist in t for item in sublist]


def connect_and_store_metadata_to_db(
    df_with_blog_post_data: pd.DataFrame,
    table_name: str,
    if_exist_solution: str = "replace",
):
    engine = create_engine("sqlite:///qlik_posts.db", echo=False)
    sqlite_connection = engine.connect()

    sqlite_table = table_name
    df_with_blog_post_data.to_sql(
        sqlite_table, sqlite_connection, if_exists=if_exist_solution, index=False
    )


def create_dataframe_from_blog_posts(
    structured_metadata: List[Blogpost]
) -> pd.DataFrame:
    return pd.DataFrame(structured_metadata)
