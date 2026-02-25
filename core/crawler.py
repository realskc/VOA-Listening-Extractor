import requests
from bs4 import BeautifulSoup

PROXIES = {
    "http": "http://127.0.0.1:7897",
    "https": "http://127.0.0.1:7897",
}


def fetch_article_list(base_url):
    """
    获取文章列表
    返回：
        List[dict] -> [{"title": str, "url": str}]
    """
    try:
        response = requests.get(
            base_url,
            proxies=PROXIES,
            timeout=10,
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"请求失败，请检查代理是否开启: {e}")

    soup = BeautifulSoup(response.text, "html.parser")

    article_list = []

    items = soup.select("ul#articleItems > li > div > a")
    if not items:
        raise RuntimeError("未找到文章列表，请检查页面结构是否发生变化")

    for a in items:
        title = a.get("title")
        title = title.strip() if title else "No Title"
        url = a.get("href")

        if url and not url.startswith("http"):
            url = "https://learningenglish.voanews.com" + url

        article_list.append({
            "title": title,
            "url": url
        })

    return article_list

def fetch_article(url):
    """
    获取文章和录音
    url 类似 https://learningenglish.voanews.com/a/how-daylight-savings-time-affects-health/8001173.html
    返回：
        dict -> {
            "title": str,
            "content": str,
            "audio_url": str
        }
    """
    try:
        response = requests.get(
            url,
            proxies=PROXIES,
            timeout=10,
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"请求失败，请检查网络或代理配置: {e}")

    soup = BeautifulSoup(response.text, "html.parser")

    # 获取文章标题
    title_elem = soup.select_one("h1")
    title = title_elem.get_text(strip=True) if title_elem else "No Title"

    # 获取文章内容
    content_elem = soup.select_one("div.wsw")
    if not content_elem:
        raise RuntimeError("未找到文章内容，页面结构可能已变化")
    paragraphs = content_elem.find_all("p", recursive=False)
    text_list = [p.get_text(strip=True) for p in paragraphs if p.get_text(strip=True)]
    content = "\n\n".join(text_list)
    if not content:
        raise RuntimeError("未能提取文章内容")

    # 获取音频链接 - VOA 网站使用 a[href*='.mp3']，且必须要 title="128 kbps | MP3"
    audio_url = None
    audio_elem = soup.select_one("a[href*='.mp3'][title='128 kbps | MP3']")
    if audio_elem:
        audio_url = audio_elem.get("href")

    return {
        "title": title,
        "content": content,
        "audio_url": audio_url
    }

if __name__ == "__main__":
    base_url = "https://learningenglish.voanews.com/z/955"
    articles = fetch_article_list(base_url)

    for idx, article in enumerate(articles):
        print(f"{idx + 1}. {article['title']}")
        print(f"   {article['url']}")