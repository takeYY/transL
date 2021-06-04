# selenium_in_docker

selenium を docker 上で動かす  
英語論文を自動翻訳するプログラム

## ソース

- 記事  
  https://qiita.com/ryoheiszk/items/93b2d52eec370c09a22e
- コード  
  https://github.com/ryoheiszk/python-selenium-on-docker

## コード関係

### 起動方法

```bash
./build.sh
```

もしくは

```bash
docker-compose build --no-cache
docker-compose up -d
docker-compose exec app bash
```

### 使い方

1. text/english.txt に以下のような形式で文章を貼り付ける  
   (text/english.txt)

```
## Abstract

Here is the text of the abstract.
The auto_n program will automatically format the text
even if it contains line breaks
in the middle of the text.

## 1. Introduction

Here is the text
of the introduction.

## 2. Chapter Title

This is the test.

### 2-1. Chapter Sub Title

This is the sub test.
```

2. 改行文字などを整形するプログラム（auto_n）を実行する

```bash
python3 source/auto_n.py
```

3. text/result.txt の自動整形ファイルを目視で確認する（改行が不適切な場合は手動で編集）  
   (text/result.txt)

```
## Abstract

Here is the text of the abstract.
The auto_n program will automatically format the text even if it contains line breaks in the middle of the text.


## 1. Introduction

Here is the text of the introduction.


## 2. Chapter Title

This is the test.


### 2-1. Chapter Sub Title

This is the sub test.


```

4. Selenium で text/result.txt にある本文を一行づつ翻訳

```bash
python3 source/translate.py
```

(text/translate.txt)

```
## Abstract
1. Here is the text of the abstract.
	- ==抄録の本文です。==
2. The auto_n program will automatically format the text even if it contains line breaks in the middle of the text.
	- ==auto_nプログラムは、テキストの途中に改行が含まれていても、自動的にフォーマットします。==

## 1. Introduction
1. Here is the text of the introduction.
	- ==ここでは、その紹介文をご紹介します。==

## 2. Chapter Title
1. This is the test.
	- ==これがテストです。==

### 2-1. Chapter Sub Title
1. This is the sub test.
	- ==これがサブテストです。==


```

HackMD で見ることを推奨
