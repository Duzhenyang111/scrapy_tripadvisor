# TripAdvisor Scraper

一个使用Scrapy框架开发的TripAdvisor酒吧数据爬虫项目。

## 功能特点

- 自动爬取TripAdvisor网站上的酒吧信息
- 提取酒吧名称和详情页URL
- 内置403状态码检测和错误处理
- 数据以CSV格式保存

## 环境要求

- Python 3.x
- Scrapy框架

## 安装说明

1. 克隆项目到本地
2. 安装依赖包：
```bash
pip install scrapy
```

## 使用方法

1. 进入项目目录
2. 运行爬虫：
```bash
scrapy crawl job
```

## 数据输出

爬取的数据将保存为CSV格式，包含以下字段：
- name: 酒吧名称
- url: 详情页链接

## 注意事项

- 请遵守目标网站的robots.txt规则
- 建议设置适当的爬取延迟，避免对目标网站造成压力
- 如遇到403错误，请检查User-Agent设置或考虑使用代理IP
