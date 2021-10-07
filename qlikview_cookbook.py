import datetime
import time
from dataclasses import dataclass
from typing import List

import pandas as pd

from program import (
    connect_and_store_metadata_to_db,
    flatten_nested_list,
    query_page_with_blog_posts,
)

URL = "https://qlikviewcookbook.com/"


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


def main():
    all_blog_posts: List = []

    soup = query_page_with_blog_posts(URL)
    last_page = get_last_pagenum_with_blog_posts(soup)
    # last_page = 3
    for page_num in range(1, last_page + 1):
        page_soup = query_page_with_blog_posts(URL + "?_page=" + str(page_num))
        all_blog_posts.append(get_blog_posts_from_soup(page_soup))
        time.sleep(2)

    flat_list = flatten_nested_list(all_blog_posts)
    df = pd.DataFrame(flat_list)
    connect_and_store_metadata_to_db(df, "qlikview_cookbook")


def get_last_pagenum_with_blog_posts(page_soup) -> int:
    page_footer = page_soup.find(
        "div", {"class": "text-left pt-cv-pagination-wrapper"}
    ).find_all("li", {"class": ""})

    last_page_num = 0

    for li_item in page_footer:
        text_from_hyperlink: str = li_item.find("a").text.strip()
        if text_from_hyperlink.isdigit() and int(text_from_hyperlink) > last_page_num:
            last_page_num = int(text_from_hyperlink)

    return last_page_num


def get_blog_posts_from_soup(page_soup) -> List[Blogpost]:
    all_blog_posts_on_page = []

    all_blog_posts = page_soup.find_all(
        "div", {"class": "col-md-12 col-sm-6 col-xs-12 pt-cv-content-item pt-cv-1-col"}
    )

    for blog_post in all_blog_posts:
        blog_post_title = blog_post.find("h4").find("a").text
        created_date = blog_post.find("span", {"class": "entry-date"}).text.strip()
        author = blog_post.find("span", {"class": "author"}).text.strip()
        url = blog_post.find("h4").find("a").get("href")

        all_blog_posts_on_page.append(
            Blogpost(
                author=author,
                title=blog_post_title,
                url=url,
                publish_date=datetime.datetime.strptime(
                    created_date, "%b %d, %Y"
                ).date(),
                source="qlikview_cookbook",
            )
        )

    return all_blog_posts_on_page


if __name__ == "__main__":
    main()
