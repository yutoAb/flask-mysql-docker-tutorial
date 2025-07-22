from flask import Flask, render_template, request, redirect  # Flaskアプリケーションに必要なモジュールをインポート
import mysql.connector  # MySQLデータベースに接続するためのモジュール
import os

app = Flask(__name__)  # Flaskアプリケーションのインスタンスを作成

def get_db_connection():
    # MySQLデータベースへの接続を確立する関数
    return mysql.connector.connect(
        unix_socket=os.environ['DB_SOCKET'],
        user=os.environ['DB_USER'],
        password=os.environ['DB_PASS'],
        database=os.environ['DB_NAME'],
    )

@app.route('/')
def home():
    # ホームページを表示するルート
    connection = get_db_connection()  # データベース接続を取得
    cursor = connection.cursor()  # クエリを実行するためのカーソルを取得
    cursor.execute("SELECT message FROM greetings")  # greetingsテーブルからmessage列を取得
    messages = cursor.fetchall()  # 取得したメッセージをすべてリストで取得
    cursor.close()  # カーソルを閉じる
    connection.close()  # データベース接続を閉じる
    return render_template('index.html', messages=messages)  # messagesをテンプレートに渡してHTMLをレンダリング

@app.route('/add', methods=['POST'])
def add_message():
    # メッセージを追加する処理を行うルート（POSTリクエストを処理）
    message = request.form['message']  # フォームから送信されたメッセージを取得
    connection = get_db_connection()  # データベース接続を取得
    cursor = connection.cursor()  # クエリを実行するためのカーソルを取得
    cursor.execute("INSERT INTO greetings (message) VALUES (%s)", (message,))  # メッセージをgreetingsテーブルに挿入
    connection.commit()  # データベースに変更を反映
    cursor.close()  # カーソルを閉じる
    connection.close()  # データベース接続を閉じる
    return redirect('/')  # メッセージ追加後、ホームページにリダイレクト

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
