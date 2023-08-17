from pathlib import Path
import re
import json
from PIL import Image

import feedparser
import streamlit as st


def fetch_title(url: str) -> str:
    feed = feedparser.parse(url)
    title = feed.feed.title
    title = title.split()[0]
    return title


def remove_tag(text: str) -> str:
    return re.sub("<p>.*<\/p>", "", text)


def format(text: str) -> str:
    text = text.replace("\n", " ")
    return text[:200]


def create_news(url: str) -> None:
    feed = feedparser.parse(url)
    for entry in feed.entries:
        st.markdown(f"#### [{entry.title}]({entry.link})")
        summary = getattr(entry, "summary", None)
        if summary:
            summary = remove_tag(summary)
            summary = format(summary)
            st.caption(summary)


def main() -> None:
    header_image = Image.open("data/header.png")
    st.image(header_image)

    urls_path = Path("data", "urls.json")
    with open(urls_path) as file:
        urls = json.load(file)
    titles = [fetch_title(url) for url in urls]

    tabs = st.tabs(titles)
    for url, tab in zip(urls, tabs):
        with tab:
            create_news(url)


if __name__ == "__main__":
    main()

