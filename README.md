# Learning Task Tracker (Django版)

このリポジトリは、**学習タスク管理アプリのPoC（概念実証）として、Djangoで開発したテンプレートベースのWebアプリケーション**です。

現在は、よりモダンで拡張性の高い構成を目指し、FastAPIをベースとした実装（[learning-task-tracker-fastapi](https://github.com/ShigeoYugawa/learning-task-tracker-fastapi)）に開発の主軸を移しています。

---

## 🧭 このDjango版の位置づけ

- Webアプリ開発の基礎理解と、Python + Django の復習・実践のために構築した学習用PoCです。
- 認証やフォームの活用といった機能は未実装ですが、**DjangoのMVC構成とCRUDの基本実装**に焦点を当てています。
- このリポジトリは、**FastAPI版へ移行する前段階の学習成果**として、記録的に残しています。

---

## ✅ 実装済の機能（PoC範囲）

- 学習タスクの一覧表示・登録・編集・削除（CRUD）
- Djangoテンプレートによる基本的なUI構成
- SQLiteを用いたシンプルなデータ永続化

---

## 🛠 未実装・今後の補完はFastAPI版で対応予定

- ユーザー登録・ログイン認証
- Djangoフォーム（ModelForm）の活用
- フロントエンド分離構成（SPA対応）
- RESTful API化
- CI/CD・テスト自動化

これらはすべて、[learning-task-tracker-fastapi](https://github.com/ShigeoYugawa/learning-task-tracker-fastapi) にて順次対応・設計中です。

---

## 📚 開発環境

- Python 3.12.3
- Django 5.2.4
- SQLite（開発用DB）

---

## 📝 補足と所感

本プロジェクトは、C# × Unity による長期的な個人開発経験をベースに、**Webアプリケーション領域へと実践を広げる第一歩**として開発しました。

FastAPIを本業軸としながらも、DjangoによるWeb構築の土台理解は、今後の設計にも大きな土台となっています。

---

## 📎 関連プロジェクト

- 🚀 [learning-task-tracker-fastapi](https://github.com/あなたのFastAPIリポジトリURL) — 本格的なAPI分離構成を目指すFastAPI版
