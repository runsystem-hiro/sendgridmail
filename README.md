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

## ♥️ 注意事項

- SendGrid Essentials プランでは **1 秒あたり 1 通程度** に制限をかけています（`time.sleep(1.2)`）
- `mail_template.txt` の 2 行目が空行でない場合はエラーになります
- テスト送信を行う際は、宛先 CSV とログファイルを適切に管理してください

---

## 📜 ライセンス

© hiro MIT License
