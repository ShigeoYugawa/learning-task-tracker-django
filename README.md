# Learning Task Tracker (Django版)

このリポジトリは、**学習タスク管理アプリのPoC（概念実証）としてDjangoで開発したテンプレートベースのWebアプリケーション**です。

現在はDjangoでの学習を再開しており、基礎の理解を深めながら機能拡張を進めています。

---

## 🧭 Django版の位置づけ

- DjangoのMVC構成やCRUD処理の理解を深めることを目的に構築した学習用PoCです。  
- ユーザー登録や認証などの機能は未実装ですが、今後フォーム処理や認証機能の実装も進める予定です。  
- 将来的にはFastAPI版などモダンなAPI分離構成への展開も視野に入れていますが、まずはDjango版で基礎固めを優先しています。

---

## ✅ 現在の実装済み機能

- 学習タスクの一覧表示、登録、編集、削除（CRUD）  
- Djangoテンプレートを用いた基本的な画面表示  
- SQLiteによるシンプルなデータ永続化

---

## 🛠 今後の開発予定（Django版）

- Djangoフォーム（ModelForm）を使った入力処理の強化  
- ユーザー登録・ログイン認証機能の実装  
- テストコードの整備とCI/CDパイプラインの構築  
- 必要に応じてREST API化やフロントエンド分離構成の検討  

---

## 📚 開発環境

- Python 3.12.3  
- Django 5.2.4  
- SQLite（開発用DB）  

---

## 📝 補足・所感

本プロジェクトは、長年のC# × Unityでの開発経験を活かし、PythonとDjangoでのWebアプリケーション開発を再学習するためのPoCです。

Djangoでの開発を通じてWebの基本を固め、将来的にはFastAPIやフロントエンド技術も取り入れて拡張していきます。

---

## 📎 関連プロジェクト

- 🚀 [learning-task-tracker-fastapi](https://github.com/ShigeoYugawa/learning-task-tracker-fastapi) — API分離構成を目指すFastAPI版
