import setuptools

with open("README.md", "r",encoding='utf8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="Suluoya",
    version="1.7.9",
    author="Suluoya",
    author_email="1931960436@qq.com",
    maintainer='Suluoya',
    maintainer_email='1931960436@qq.com',
    description="Suluoya",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=['requests',
                    'pandas',
                    'beautifulsoup4',
                    #'translators == 4.7.9',
                    #'fuzzywuzzy == 0.18.0',#字符串模拟匹配
                    #'ngender == 0.1.1',#性别
                    #'MyQR == 2.3.1',#二维码
                    #'pyforest == 1.0.3',#自动导入库
                    #'wget == 3.2',#下载
                    'urllib3',#爬虫
                    #'you-get == 0.4.1488',#下载视频
                    #'goose3 == 3.1.6',#文章提取
                    #'pandas_profiling == 2.9.0',#报告
                    #'flashtext == 2.7',#关键词查找与替换
                    #'textblob == 0.15.3',#英文情感
                    #'snownlp == 0.12.3',#中文情感
                    #'progressbar == 2.5',#进度条
                    'tqdm',#进度条
                    #'pyttsx3',#语音
                    #'textract',#提取文档信息
                    #'newspaper3k',#提取新闻
                    'baostock',#股票数据
                    'parsel',#爬虫解析
                    #'pretty_errors',#打印错误
                    #'fake_useragent',#伪装
                    'lunar_python',#日期
                    #'pandasgui',#可视化界面
                    #'sweetviz'#数据分析
                    ]
)
