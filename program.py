import datetime
import time
from dataclasses import dataclass
from typing import List

import pandas as pd
import requests
from bs4 import BeautifulSoup
from sqlalchemy import create_engine
from tqdm import trange

URL = "https://community.qlik.com/t5/Blogs/ct-p/qlik-community-blogs/page/"


@dataclass
class Blogpost:
    author: str
    likes: int
    views: int
    url: str
    publish_date: datetime.date
    scraped_date: datetime.date = datetime.date.today()


def main():

    all_blog_posts: List = []

    soup_last_pagenum = query_page_with_blog_posts(URL + "1")
    last_page_num: int = extract_last_pagenum_with_blog_posts(soup_last_pagenum)

    # last_page_num = 2  # Use to manually override number of pages that get scraped, useful while developing

    for page_num in trange(1, last_page_num + 1):
        scrape_url = URL + str(page_num)

        soup = query_page_with_blog_posts(scrape_url)
        all_blog_posts.append(extract_blog_post_metadata(soup))
        time.sleep(2)

    flat_list = flatten_nested_list(all_blog_posts)
    df = create_dataframe_from_blog_posts(flat_list)

    connect_and_store_metadata_to_db(df, "qlik_community")


def query_page_with_blog_posts(url_to_scrape: str) -> BeautifulSoup:
    r = requests.get(url_to_scrape)

    assert r.status_code == 200

    return BeautifulSoup(r.text, "html.parser")


def extract_last_pagenum_with_blog_posts(
    beautifulsoup_object_for_page: BeautifulSoup
) -> int:
    ul_tags = beautifulsoup_object_for_page.find_all(
        "ul", {"class": "lia-paging-full-pages"}
    )
    first_match = ul_tags[0]
    li_tags = first_match.find_all("li")
    last_page: int = int(li_tags[-1].find("a").text.strip())

    return last_page


def extract_blog_post_metadata(
    beautifulsoup_object_for_page: BeautifulSoup
) -> List[Blogpost]:
    all_posts_on_page: List = []

    for ultag in beautifulsoup_object_for_page.find_all(
        "ul", {"class": "discussion-list-container"}
    ):
        for litag in ultag.find_all("li", {"class": "blog-category scroll-class"}):
            all_a_tags = litag.find_all("a")

            for a_tag in all_a_tags:
                img_element = a_tag.find_all("img")

                if img_element:
                    author = img_element[0].get("title")

            num_views = int(litag.find_all("label", {"class": "views"})[0].text.strip())
            num_likes = int(
                litag.find_all("span", {"class": "kudo-class"})[0].text.strip()
            )
            url = "https://community.qlik.com" + str(
                litag.find("h3").find("a").get("href")
            )
            created_date = (
                litag.find_all("div", {"class": "login-date-container"})[0]
                .find_all("label")[-1]
                .text.strip()
                .split("/")[0]
            )

            all_posts_on_page.append(
                Blogpost(
                    author=author,
                    likes=num_likes,
                    views=num_views,
                    url=url,
                    publish_date=datetime.datetime.strptime(
                        created_date.strip(), "%Y-%m-%d"
                    ).date(),
                )
            )

    return all_posts_on_page


def create_dataframe_from_blog_posts(
    structured_metadata: List[Blogpost]
) -> pd.DataFrame:
    return pd.DataFrame(structured_metadata)


def connect_and_store_metadata_to_db(
    df_with_blog_post_data: pd.DataFrame, table_name: str
):
    engine = create_engine("sqlite:///qlik_posts.db", echo=False)
    sqlite_connection = engine.connect()

    sqlite_table = table_name
    df_with_blog_post_data.to_sql(
        sqlite_table, sqlite_connection, if_exists="replace", index=False
    )


def flatten_nested_list(t):
    return [item for sublist in t for item in sublist]


if __name__ == "__main__":
    main()
