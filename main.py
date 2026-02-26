import core.crawler as crawler
import core.storage as storage

if __name__ == "__main__":
    base_url = "https://learningenglish.voanews.com/z/955"
    articles = crawler.fetch_article_list(base_url)

    for idx, article in enumerate(articles):
        print(f"{idx + 1}. {article['title']}")
    print("Select an article number, or 'q' to quit:")
    while True:
        choice = input("> ")
        if choice.lower() == 'q':
            print("Exiting.")
            break
        if not choice.isdigit() or not (1 <= int(choice) <= len(articles)):
            print("Invalid choice. Please enter a valid article number or 'q' to quit.")
            continue
        selected_article = articles[int(choice) - 1]
        break

    try:
        article_data = crawler.fetch_article(selected_article["url"])
        print("\n" + "="*60)
        print(f"标题: {article_data['title']}")
        print("="*60)
        print(f"\n内容:\n{article_data['content']}\n")
        if article_data['audio_url']:
            print(f"录音链接: {article_data['audio_url']}")
        else:
            print("未找到录音链接")
        print("="*60)
        
        # 保存文章到本地
        article_folder = storage.save_article(article_data)
        print(f"\n文章已保存至: {article_folder}")
    except RuntimeError as e:
        print(f"错误: {e}")