# 学習タスク管理アプリ（PoC）

このリポジトリは、Djangoフレームワークを使った学習用Webアプリケーションの**概念実証（Proof of Concept）**です。  
教材、授業、学習進捗などを管理する機能のプロトタイプ実装を目的としています。

---

## 目的

- Djangoの基本機能（Model、View、Template、ORMなど）を理解する  
- Webアプリ開発の全体的な流れを学習する  
- 今後の拡張やリファクタリングを見据えた「土台」を構築する  

---

## 注意点

- 本プロジェクトはPoCのため、アーキテクチャ設計（MVPなど）やユニットテストは未導入です。  
- コードは最小構成かつ学習優先で記述しています。  
- 今後、設計改善、テスト導入、パフォーマンス最適化を計画しています。  

---

## 環境構築手順（WSL + venv）

このアプリケーションは、**Windows 上での WSL（Ubuntu）環境 + VSCode + Django**による開発を前提としています。

### 0. WSL の有効化と Ubuntu のインストール（初回のみ）

#### 1. PowerShell（管理者）で以下を実行：

```powershell
wsl --install
```

#### 2. 自動的に Ubuntu がインストールされ、PCの再起動が求められます。

#### 3. 再起動後、初回の Ubuntu 起動時に ユーザー名とパスワードを設定します。

#### 4. インストール確認：

```powershell
wsl --list --verbose
```

### 1. VSCode に WSL 拡張機能をインストール

#### 1. VSCode を起動

#### 2. 拡張機能パネルで下記項目を検索し、インストール

| 拡張機能名                  | 用途             |
| ---------------------- | -------------- |
| Remote - Development   | WSL接続やSSH開発に必要 |
| Python                 | Django開発に必須    |
| Japanese Language Pack | 日本語UI（任意）      |

### 2. WSL に接続し、プロジェクトディレクトリを作成

#### 1. VSCode 左下の緑の「><」アイコンをクリック

#### 2. 「ディストリビューションを使用してWSLに接続...」]

#### 3. WSLのターミナルで以下を実行：

```bash
wsl
mkdir -p ~/projects/learning-task-tracker
cd ~/projects/learning-task-tracker
```

### 3. Python 仮想環境を作成・有効化

```bash
sudo apt update
sudo apt install python3-venv -y

python3 -m venv .venv
source .venv/bin/activate
```

### 4. Djangoのインストールと初期化

```bash
pip install django
python -m django --version
django-admin startproject learning_task_tracker .
```

### 5. 動作確認

```bash
python manage.py runserver
# http://127.0.0.1:8000 にアクセスしてホーム画面（home.html）を確認
```
### 6. GitHub リポジトリとの連携

```bash
# GitHubのユーザー名とメールアドレスを設定（初回のみ必要）
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Git 初期化とリモート設定
git init
git remote add origin https://github.com/YOUR_USERNAME/learning-task-tracker.git

# 初回コミットとプッシュ
git add .
git commit -m "Initial Django project setup"
git push -u origin main

```

### 7. VSCode の Python インタプリタ選択
画面右下に表示される Python バージョンをクリックし、.venv/bin/python を選択してください。表示されない場合は、コマンドパレット（Ctrl+Shift+P）で Python: Select Interpreter を実行します。


---

## 今後の予定

- 学習タスク管理に関わる基本的なCRUD操作を通じて、Djangoのモデル間の関連付けを理解し実装する  
- ユーザーインターフェースの充実と使いやすさの向上を目指す  
- 学習進捗の管理や教材・授業の紐付けなど、実務に近い機能の追加を予定  
- 逐次、テスト導入や設計改善、パフォーマンス最適化にも取り組む  

---

## 本プロジェクトの価値について

本プロジェクトは単なるCRUD操作の実装にとどまらず、  
- データモデルの設計と関係性の理解  
- 実際に動くWebアプリケーションの構築経験  
- 今後の機能拡張やリファクタリングを見据えた土台作り  

を目的としています。  
学習段階としては基礎の積み重ねが重要であり、これが将来的により高度な業務アプリケーション開発への糧となることを目指しています。

---

## 実装済みの主な機能

- トップページ（ホーム）表示
- 教材（Material）一覧／詳細表示
- 授業（Lesson）詳細表示
- 画面テンプレートにBootstrap導入

