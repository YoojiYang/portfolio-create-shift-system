# シフトアサイン表自動作成ツール

## システム概要
従業員のポジションの割り当て、およびシフト表の作成を行うサービスです。
  
  
## 特徴
  
**自動シフト生成**: 条件に基づいて最適な従業員を各ポジションにアサインします。  
**スプレッドシートベース**: 微調整も簡単に行えます。  
**シンプル設計**:　５ステップで対象期間のアサイン表とシフト表を作成します。  
  
## 使用方法
  
STEP1: 各従業員の出勤可否情報を入力する。（①出勤可否連絡シート）  
STEP2: 各従業員のスキル情報を入力する。（②従業員マスタ[編集用]）  
STEP3: 対象期間を設定。（③実行ページ）  
STEP4: アサイン表の雛形を作成。（③実行ページ）  
STEP5: 従業員の割り当てを実行。（③実行ページ）  
  
## 技術スタック
  
| 項目 | 利用言語･フレームワーク |
| ---- | ---- |
| アサインアルゴリズム | Python |
| フロントエンド | HTML, CSS, JavaScript, BootStrap |
| spreadsheet操作 | GoogleAppScript |
| データベース | Googlespreadsheet |
| 実行環境 | Flask, PythonAnywhere |
