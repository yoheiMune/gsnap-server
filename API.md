# GSnap API仕様
ここではGSnapサーバーのAPI仕様を記載します.

## 共通
* APIルート：http://gsnap.yoheim.tech
* 実装ファイル：[app.py](./appy.py)
  * 本仕様書で不明点がある場合には、お手数ですが上記の実装内容をご確認ください.
* リクエストヘッダ：
  * Content-Type : application/json
* ログイン必須
  * ログイン（/api/login）以外は、APIトークンが必要です。
  * クエリパラメータに `?api_token=token1` のように付与してください。
  * APIトークンは、ログインAPIのレスポンスから取得できます。  

## ログイン
* メソッド：POST
* パス：/api/login
* パラメータ：
  * login_id : ログインID
  * password : パスワード
* レスポンスのステータスコード: 200
* レスポンス例：
    ```json
    {
        "api_token": "token1",
        "avatar_url": "/static/images/icons/1.png",
        "id": 1,
        "login_id": "test1",
        "name": "うさぎ"
    }
    ```

## タイムライン取得
* メソッド：GET
* パス：/api/posts
* パラメータ：なし
* レスポンスのステータスコード: 200
* レスポンス例：
    ```json
    [
        {
            "body": "本文だよー本文だよー13",
            "id": 13,
            "image_url": "/static/images/photos/13.jpg",
            "liked": false,
            "num_of_comments": 0,
            "num_of_likes": 0,
            "posted_at": 1535639728000,
            "user": {
                "api_token": "token5",
                "avatar_url": "/static/images/icons/5.png",
                "id": 5,
                "login_id": "test5",
                "name": "ぱんだ"
            },
            "user_id": 5
        }
    ]
    ```

## 投稿
* メソッド：POST
* パス：/api/posts
* リクエストヘッダ：
  * Content-Type: multipart/formdata
* パラメータ：
  * body : 本文
  * file : 画像ファイル
* レスポンスのステータスコード: 201
* レスポンス例：
    ```json
    {
        "body": "body",
        "id": 14,
        "image_url": "/static/images/photos/u_XDCqJnyrHK.png",
        "posted_at": 1535645898000,
        "user_id": 1
    }
    ```

## いいね追加
* メソッド：POST
* パス：/api/posts/{post_id}/likes
* パラメータ：なし
* レスポンスのステータスコード: 201
* レスポンス例：
    ```json
    {
        "post_id": 1,
        "user_id": 1
    }
    ```

## いいね削除
* メソッド：DELETE
* パス：/api/posts/{post_id}/likes
* パラメータ：なし
* レスポンスのステータスコード: 200
* レスポンス例：
    ```json
    {
        "message": "Deleted."
    }
    ```

## コメント追加
* メソッド：POST
* パス：/api/posts/{post_id}/comments
* パラメータ：
  * comment : コメント内容
* レスポンスのステータスコード: 201
* レスポンス例：
    ```json
    {
        "comment": "コメント内容",
        "id": 3,
        "post_id": 1,
        "user_id": 1
    }
    ```

## コメント削除
* メソッド：DELETE
* パス：/api/comments/{comment_id}
* パラメータ：なし
* レスポンスのステータスコード: 200
* レスポンス例：
    ```json
    {
        "message": "Deleted."
    }
    ```
