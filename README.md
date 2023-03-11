ChatGPT-GUI
===============

[![MIT License](https://img.shields.io/github/license/Cubicpath/ChatGPT-GUI?style=flat-square)][license]
[![PyPI](https://img.shields.io/pypi/v/chatgpt-gui?label=PyPI&logo=pypi&style=flat-square)][homepage]
[![Python](https://img.shields.io/pypi/pyversions/chatgpt-gui?label=Python&logo=python&style=flat-square)][python]
[![CPython](https://img.shields.io/pypi/implementation/chatgpt-gui?label=Impl&logo=python&style=flat-square)][python]

------------------------------

ChatGPTの非公式GUIアプリケーションです。

------------------------------

**注：このプロジェクトはパブリックαであり、そのため多くの機能が未完成です。**

### その他のドキュメント:
- [変更履歴][changelog_github]
- [ライセンス][license_github]

### 目次
- [概要](#about)
     - [機能](#features)
- [使用法](#how-to-use)
     - [インストール](#installation)
     - [認証](#authentication)
          - [セッショントークンガイド](#session-token-guide)
          - [セッションデータ](#session-data)
     - [会話の保存／読み込み](#savingloading-conversations)
     - [テーマ](#themes)
          - [テーマファイルの構成](#theme-file-structure)


## 概要
---------------
ChatGPT-GUIは、[Qt for Python][PySide]を使って書かれたアプリケーションで、
[ChatGPT]をベースにしたAIアシスタントと簡単に対話ができるようになります。

このプロジェクトは、私の別のプロジェクトである[HaloInfiniteGetter](https://github.com/Cubicpath/HaloInfiniteGetter )からフォークしたものです。

このアプリケーションが気に入ったら、ぜひスターを付けてください :)
<a id="about"></a>
---------------

## 機能
---------------
- ~~[x] Email/Password Login to [ChatGPT] Without Browser~~
  - ~~(Captcha solving is untested but implemented)~~
- [x] プロキシ設定
  - 対応プロトコルは`HTTP`と`SOCKS5`です。
- [x] PATHにある実行可能なスクリプト (`chatgpt`)
- [x] デスクトップおよびスタートメニューのショートカット
- [x] セッション（トークン）保持
- [x] アクセストークンの自動更新機能
- [x] 複数の同時会話
- [x] 会話のセーブ＆ローディング
- [x] 複数行入力
- [x] Exception Reporter & Traceback Viewer（例外レポート＆トレースバックビューア）
- [x] テーマ
  - ビルトイン・テーマは: [Breeze Dark, Breeze Light, and Legacy]です
<a id="features"></a>
---------------

#### Todo:
- [ ] きれいな対話ビュー
- [ ] AIメッセージの再試行

<a id="how-to-use"></a>
使用方法
---------------


<a id="installation"></a>
### インストール:
- まず、[このリンク][python310]を使ってPython3.10をインストールします。
- コマンドプロンプトを（Win + R を同時に押して-- "cmd "と入力）開いて`pip install chatgpt-gui` と入力する
  - また、オプションで、最新のアンステーブルバージョンをインストールするには、`pip install git+https://github.com/Cubicpath/ChatGPT-GUI.git` と入力します。
- これで完了です !プログラムを起動するには、`chatgpt`と入力するだけです。
  - 一旦起動したら、`Tools`コンテキストメニューの`Create Desktop Shortcut`ツールを使って、デスクトップショートカットを作成できます。


<a id="authentication"></a>
### 認証:
~~[rawandahmad698]と[tls-client][python-tls-client]のおかげで、トークンやブラウザをいじらずに認証する方法があります。アプリ自体からサインインするだけです.~~

**現在、cloudflareを自動的にバイパスするためには、Google Chromeが必要です。**

現在、EmailとPasswordによるログインはできません。
それまでの間、セッショントークン認証を参考にしてください。


![サインイン](https://i.imgur.com/DabSYBhl.png)


<a id="session-token-guide"></a>
#### セッション・トークンガイド:
- ブラウザから[ChatGPT]にサインインしてください
- chat.openai.comのCookiesに移動します。
  - Firefoxの場合 -- F12 > 「ストレージ」タブに移動 > 「Cookies」で「https://chat.openai.com」を選択します。
- Cookieの値「__Secure-next-auth.session-token」をダブルクリックし、CTRL + Cでコピーしてください。
- 設定ウィンドウを開き、「セッショントークンの編集」ボタンで入力のロックを解除し、コピーした値を貼り付けます。
- セットボタンを押すと、これで認証されるはずです
-

<a id="session-data"></a>
#### セッション・データ:
セッションデータは、持続性のために隠しファイル（`~/.config/chatgpt_gui/.session.json`）に保存されます。
サインアウトしたり、セッショントークンをクリアすると、自動的にすべてのセッションデータが削除されます。

セッションデータを直接編集する必要がある場合は、以下のフォーマットに沿って編集してください：
```json
{
  "user": {
    "id": "ユーザーID（'user-'で始まる接頭語）",
    "name": "ユーザー名（通常はEメールと同じ）",
    "email": "セッションに紐付けられたメール",
    "image": "プロフィール画像へのリンク（通常はあなたの画像と同一）",
    "picture": "プロフィール画像へのリンク",
    "groups": [],
    "features": []
  },
  "cloudflare": {
    "bm": "クッキー __cf_bm の値",
    "clearance": "cf_clearanceクッキーの値",
    "expires": "cf_clearance を取得してから 1 時間後"
  },
  "expires": "refresh_auth()後に自動的に取得される",
  "token": "Secure-next-auth.session-tokenクッキーの値",
  "user_agent": "クライアント/認証者が使用するユーザーエージェント"
}
```

<a id="savingloading-conversations"></a>
### 会話の保存／読み込み
ChatGPTで選択中の会話は、任意のタブを右クリックして`Export Conversation To...`ボタンを押すことで保存できます。
これでファイルダイアログが開き、読み込んだときに表示される会話の名前を変更する事が出来ます。

デフォルトでは、すべての会話は `~/.cache/chatgpt_gui/` ディレクトリに保存されます。
しかし、エクスポートする時には、任意のフォルダを選択する事ができます。

**注：あるアカウントの会話は、他のアカウントからアクセスすることはできません。**

#### 会話フォーマットについて:
会話はメッセージの線形のリストとして保存され、各メッセージはその前のメッセージに対する応答となります。
すべてのUUIDが追跡されるため、インポート後もクライアントが会話を継続する事が出来ます。

以下のデータフォーマットで保存されます：
```json
{
  "id": "会話UUID",
  "messages": [
    {
      "id": "メッセージUUID",
      "role": "user",
      "content": {
        "content_type": "text",
        "parts": [
          "ChatGPTへのメッセージ"
        ]
      }
    },
    {
      "id": "メッセージUUID",
      "role": "assistant",
      "content": {
        "content_type": "text",
        "parts": [
          "ChatGPTからの回答"
        ]
      }
    }
  ]
}
```

<a id="themes"></a>

### テーマ:
テーマは、すでに存在する要素にスタイルを付ける方法です（CSSを考えてください）。
リソースとスタイルシートが同じフォルダレベルにあるディレクトリ内に格納されます。

<a id="theme-file-structure"></a>
#### テーマファイルの構造:
    ../
    │
    ├───[theme_id]/
    │       ├─── [icon1_name].svg
    │       ├─── [icon2_name].svg
    │       ├─── [icon3_name].svg
    │       └─── stylesheet.qss
    │

現在のビルトインテーマは次の通りです:
- `Breeze Dark`
- `Breeze Light`
- `Legacy (Default Qt)`

現在のそよ風のテーマは若干の修正を加えたバージョンですが、オリジナルのテーマは[BreezeStyleSheets]で見られます。

[BreezeStyleSheets]: https://github.com/Alexhuszagh/BreezeStyleSheets "BreezeStyleSheets"
[changelog_github]: https://github.com/Cubicpath/ChatGPT-GUI/blob/master/CHANGELOG.md "Changelog"
[ChatGPT]: https://https://chat.openai.com "ChatGPT"
[homepage]: https://pypi.org/project/chatgpt-gui/ "ChatGPT-GUI PyPI"
[license]: https://choosealicense.com/licenses/mit "MIT License"
[license_github]: https://github.com/Cubicpath/ChatGPT-GUI/blob/master/LICENSE "MIT License"
[PySide]: https://pypi.org/project/PySide6/ "PySide6"
[python]: https://www.python.org "Python"
[python310]: https://www.python.org/downloads/release/python-3100/ "Python 3.10"
[rawandahmad698]: https://github.com/rawandahmad698 "rawandahmad698"
[python-tls-client]: https://github.com/FlorianREGAZ/Python-Tls-Client "tls-client"
