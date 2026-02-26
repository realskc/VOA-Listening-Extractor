import requests
import re
from pathlib import Path


PROXIES = {
    "http": "http://127.0.0.1:7897",
    "https": "http://127.0.0.1:7897",
}


def sanitize_filename(filename):
    """
    清理文件名，移除不合法的字符
    """
    invalid_chars = r'[<>:"/\\|?*]'
    sanitized = re.sub(invalid_chars, '_', filename)
    sanitized = sanitized.rstrip('. ')
    return sanitized[:200]


def save_article(article_data):
    """
    保存文章内容到 data/ 下的子文件夹，并下载音频文件
    参数：
        article_data: dict -> {
            "title": str,
            "content": str,
            "audio_url": str
        }
    返回：
        str -> 保存文件夹路径
    """
    # 创建 data 文件夹
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    # 使用文章标题创建子文件夹，清理不合法字符
    folder_name = sanitize_filename(article_data["title"])
    article_folder = data_dir / folder_name
    article_folder.mkdir(exist_ok=True)
    
    # 保存文章标题
    title_file = article_folder / "title.txt"
    with open(title_file, "w", encoding="utf-8") as f:
        f.write(article_data["title"])
    
    # 保存文章内容
    content_file = article_folder / "content.txt"
    with open(content_file, "w", encoding="utf-8") as f:
        f.write(article_data["content"])
    
    # 下载音频文件
    if article_data.get("audio_url"):
        try:
            audio_path = download_audio(article_data["audio_url"], article_folder)
            print(f"音频已下载至: {audio_path}")
        except Exception as e:
            print(f"音频下载失败: {e}")
    
    print(f"文章已保存至: {article_folder}")
    return str(article_folder)


def download_audio(audio_url, save_folder):
    """
    下载音频文件到指定文件夹
    参数：
        audio_url: str -> 音频链接
        save_folder: Path/str -> 保存文件夹
    返回：
        str -> 音频文件的相对路径
    """
    try:
        response = requests.get(
            audio_url,
            proxies=PROXIES,
            timeout=30,
            stream=True
        )
        response.raise_for_status()
        
        # 从 URL 中提取文件名
        filename = audio_url.split("/")[-1].split("?")[0]
        if not filename.endswith(".mp3"):
            raise RuntimeError("音频链接不合法，未找到 .mp3 文件")
        
        save_path = Path(save_folder) / filename
        with open(save_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
        
        return str(save_path)
    
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"音频下载失败: {e}")
