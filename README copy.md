# SendGrid Plain Text Mail Distributor

このリポジトリは、**SendGrid API** を使用して、**プレーンテキスト形式のメールを一斉配信**する Python スクリプトです。  
メールテンプレートから件名・本文を構築し、CSV の宛先リストに対して順次送信します。

## ✅ 特長

- プレーンテキスト形式による軽量メール送信
- 宛先ごとに `{first_name}` `{last_name}` `{company}` `{full_name}` を差し込み可能
- 再送防止機能（送信済みリストから重複除外）
- `.env` による安全なキー管理
- ログファイルによる送信成功・失敗記録

---

## 📁 ディレクトリ構成

```
.
├── send_mail.py            # メインスクリプト
├── library-send_mail.py    # ライブラリ版メインスクリプト
├── mail_template.txt       # 件名・本文テンプレート
├── recipients.csv          # 宛先リスト
├── .env                    # APIキーと送信元情報
├── sent_log.csv            # 送信済みログ
├── error_log.csv           # エラーログ
├── README.md               # このファイル
└── .gitignore              # Git 除外設定
```

---

## 🔐 `.env` 設定

`.env` ファイルには以下を記述してください：

```env
SENDGRID_API_KEY=xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
FROM_EMAIL=yourname@example.com
FROM_NAME=送信者名
```

---

## 📨 mail_template.txt 仕様

テンプレートは以下の形式に従ってください：

```
【件名（1行目）】

（2行目は空行）

{company}
{full_name} 様

本文...
```

- `{first_name}` `{last_name}` `{company}` `{full_name}` を使用可能
- `{full_name}` は名前の有無に応じて自動で調整されます（例：田中 様／田中 一郎 様）

---

## 📋 recipients.csv 仕様

CSV の 1 行目（ヘッダー）は以下：

```
email,first_name,last_name,company
```

例：

```
tanaka@example.com,陽翔,田中,株式会社ランシステム
suzuki@example.com,陽葵,鈴木,株式会社ランシステム
```

---

## 🧪 実行方法

```bash
python send_mail.py
```

送信成功時は `✔`、失敗・例外時は `✘` で表示され、ログにも記録されます。

---

## 🔁 スクリプトのバリエーション

本リポジトリには、2 種類のスクリプトが同梱されています。**利用シーンや保守方針に応じて選択してください。**

| スクリプト名           | 特徴                                                                             |
| ---------------------- | -------------------------------------------------------------------------------- |
| `send_mail.py`         | `requests` による API 直叩き。軽量・汎用的だが記述がやや冗長                     |
| `library-send_mail.py` | SendGrid 公式ライブラリ（`sendgrid-python`）を使用。保守性が高く拡張しやすい構造 |

---

## ✅ `library-send_mail.py` を使うメリット

1. **SendGrid 公式サポート方式**：構文や仕様変更に強く、将来の API 更新にも対応しやすい
2. **構造が明快で読みやすい**：`Mail`, `Email`, `To` などのクラスで構築されており、型補完も効く
3. **HTML メール・添付ファイル・一括 BCC などの拡張も簡単**（将来の要件にも対応可能）
4. **エラー処理がわかりやすい**：例外・レスポンスのハンドリングがシンプル

---

## 📦 ライブラリのインストール（必須）

`library-send_mail.py` を使用するには、以下のライブラリが必要です：

```bash
pip install sendgrid
```

## 📟 ライブラリ版の実行方法

```bash
python library-send_mail.py
```

---

## 📌 どちらを使うべきか？

| 目的・背景                                  | 推奨スクリプト         |
| ------------------------------------------- | ---------------------- |
| とりあえず送る・軽量に済ませたい            | `send_mail.py`         |
| 将来の保守や拡張性も考慮したい              | `library-send_mail.py` |
| HTML メールや添付、BCC 送信などが視野にある | `library-send_mail.py` |
| 外部 API と汎用的に組み合わせたい           | `send_mail.py`         |

---

## ♥️ 注意事項

- SendGrid Essentials プランでは **1 秒あたり 1 通程度** に制限をかけています（`time.sleep(1.2)`）
- `mail_template.txt` の 2 行目が空行でない場合はエラーになります
- テスト送信を行う際は、宛先 CSV とログファイルを適切に管理してください

---

## 📜 ライセンス

© hiro MIT License
