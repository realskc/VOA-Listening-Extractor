### 爬取 VOC Learning English 听力材料并处理

#### 流程

1. 主程序为 main.py
2. main.py 调用 crawler.py 爬取列表中的若干文章，并将这些文章直接输出（无GUI），由用户选择所需的文章
3. main.py 调用 crawler.py，爬取该文章的文本与录音
4. main.py 调用 storage.py，将该爬到的内容保存至data/下文章名称的同名子文件夹中
5. main.py 调用 extractor.py，将文章发送给大语言模型 API，并得到生词列表
6. main.py 调用 storage.py，将生词列表存储至文章对应的文件夹中

#### 文件架构

voa_listening_extractor/
    main.py
    core/
        crawler.py
        extractor.py
        storage.py
    data/
        (auto downloaded)
    requirements.txt
