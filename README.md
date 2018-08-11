# gsnap-server
GSnapのサーバーサイドです。

## Pythonのセットアップ
### Python3系のインストール
https://www.python.org/
### 依存関係をインストール
```
pip3 install -r requirements.txt
```


## データベースのセットアップ
### MySQL準備
MySQLを利用可能にインストールしてください.
### データベース作成
```
CREATE DATABASE gsnap CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```
### ユーザー作成
```
CREATE USER gsnap@localhost IDENTIFIED BY 'gsnap';
GRANT ALL PRIVILEGES ON gsnap.* TO 'gsnap'@'localhost';
```
### テーブル作成
```
$ FLASK_APP=app.py flask shell
>>> from models import db
>>> db.create_all()
```
### データ投入
`sql/database/seeds.sql`を投入.

## サーバー起動.
```
python app.py
```