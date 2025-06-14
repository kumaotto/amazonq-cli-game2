# AWS IAM Security Adventure

AWS IAMを主人公にしたアクションゲームです。IAM関連のセキュリティリスクを避けながらセキュアなクラウド環境（ゴール）を目指します。

## ゲーム概要

- **主人公**: AWS IAM（青い盾のアイコン）
- **敵**: AWS IAM関連のセキュリティリスク（具体的な脅威名が表示される色付きボックス）
- **目標**: セキュリティリスクに当たらずにゴール（緑のセキュアクラウド）に到達する

## 新機能

### ステージ選択
5つの異なるIAMセキュリティステージから選択可能：
1. **IAM基本設定** - 基本的なIAM設定ミス
2. **アクセス管理** - アクセス制御の脅威
3. **認証情報漏洩** - 認証情報の不適切な管理
4. **ポリシー設定ミス** - IAMポリシーの設定不備
5. **高度なIAM攻撃** - 巧妙なIAM攻撃手法

### 難易度選択
4つの難易度レベル：
- **簡単** - 初心者向け（敵の速度が遅く、出現頻度も低い）
- **普通** - 標準的な難易度
- **難しい** - 上級者向け（敵の速度が速く、出現頻度が高い）
- **エキスパート** - 最高難易度

### AWS IAM関連セキュリティリスク表示
各ステージで異なる具体的なIAMセキュリティ脅威が日本語で表示されます：

**ステージ 1 - IAM基本設定:**
- ルートアカウント使用
- 弱いパスワード
- MFA未設定
- 過度な権限付与

**ステージ 2 - アクセス管理:**
- 権限昇格攻撃
- クロスアカウント侵害
- 一時認証情報漏洩
- 未使用ユーザー放置

**ステージ 3 - 認証情報漏洩:**
- アクセスキー漏洩
- シークレット平文保存
- 認証情報ハードコード
- ローテーション未実施

**ステージ 4 - ポリシー設定ミス:**
- ワイルドカード乱用
- リソース制限なし
- 条件設定不備
- 継承権限過多

**ステージ 5 - 高度なIAM攻撃:**
- AssumeRole悪用
- フェデレーション攻撃
- サービスロール乗っ取り
- IAMロール連鎖攻撃

## 操作方法

### メニュー画面
- **↑ ↓**: メニュー項目選択
- **ENTER**: 決定
- **ESC**: 終了

### ステージ選択画面
- **← →**: ステージ選択
- **ENTER**: 決定
- **ESC**: メニューに戻る

### 難易度選択画面
- **↑ ↓**: 難易度選択
- **ENTER**: ゲーム開始
- **ESC**: ステージ選択に戻る

### ゲーム中
- **移動**: 矢印キーまたはWASDキー
- **ESC**: メニューに戻る

### ゲームオーバー画面
- **R**: リスタート
- **ESC**: メニューに戻る

## ゲーム機能

- IAMセキュリティリスクを避けるたびにスコア獲得
- 時間が経つにつれて難易度が上昇
- ステージごとに異なる背景色とIAMセキュリティリスク
- 難易度に応じた敵の速度と出現頻度の調整
- ゴール到達で勝利
- セキュリティリスクに接触でゲームオーバー
- 日本語フォント対応で文字化けなし

## セットアップ

1. 必要なライブラリをインストール:
```bash
pip install -r requirements.txt
```

2. ゲームを実行:
```bash
python iam_security_game.py
```

## 技術的な特徴

- **日本語フォント自動検出**: macOS、Windows、Linuxで適切な日本語フォントを自動選択
- **マルチプラットフォーム対応**: 各OSの標準フォントに対応
- **文字化け防止**: 日本語テキストが正しく表示されます

## AWS IAMセキュリティの学習

このゲームは、AWS IAM（Identity and Access Management）で実際に発生する可能性のあるセキュリティリスクを体験できる教育的なゲームです。

### 各ステージで学べるIAMセキュリティ概念

**ステージ 1 - IAM基本設定:**
- ルートアカウントの適切な管理
- 強力なパスワードポリシーの重要性
- 多要素認証（MFA）の必要性
- 最小権限の原則

**ステージ 2 - アクセス管理:**
- 権限昇格攻撃の防止
- クロスアカウントアクセスの制御
- 一時認証情報の適切な管理
- 定期的なユーザーアクセス監査

**ステージ 3 - 認証情報漏洩:**
- アクセスキーの安全な管理
- AWS Secrets Managerの活用
- 認証情報のハードコード回避
- 定期的な認証情報ローテーション

**ステージ 4 - ポリシー設定ミス:**
- IAMポリシーのベストプラクティス
- ワイルドカード（*）の適切な使用
- リソースベースの制限
- 条件付きアクセス制御

**ステージ 5 - 高度なIAM攻撃:**
- AssumeRoleの安全な実装
- フェデレーションの適切な設定
- サービスロールの保護
- ロール連鎖の制限

現実のAWS環境でも、これらのセキュリティリスクを理解し、適切なIAM設定を行うことで、クラウドインフラストラクチャを保護することができます。
