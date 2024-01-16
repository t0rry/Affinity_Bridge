# Affinity Bridge Addon v0.6.0
![image](https://user-images.githubusercontent.com/78343605/201816867-742ffd77-b2d7-4f97-888c-c3b78264012a.png)
## Note (English only)
**(English)**

So many things are written in Japanese.
(For example, processing completion messages, debug messages, and this readme)
I don't know if this project can help people.
If there is a lot of feedback and support, we may support English.

**(日本語)**

## どういうアドオン？
Blenderの画像エディタ・UVエディタで開いている画像をAffinityPhoto2で開きます。

テクスチャの編集をはじめ、レンダリングした画像のレタッチを使用することを想定して作成されています。

※Blenderの標準機能でも「画像エディタ・UVエディタ上で開いている画像を外部エディタ上で開く」機能はあります。

## 標準機能との違い
***「Render Result」、「Viewer Node」についてもAffinityPhoto2で開くことができます。***

標準機能ではこれをサポートしていません。Blenderの仕様で上記二つのデータについてパスを保持していないためです。

この仕様を回避するために保存がされていない（パスが存在しない）Blenderが保持する画像データについてはblendファイル直下に「AffinityBridge」フォルダを生成し、
あなたが指定した画像フォーマット・カラーフォーマットをもとに保存され、AffinityPhoto2に共有されます。

## 動作環境
**開発者の環境に依存しています**
このプロジェクトは私の個人プロジェクトだからです。

多くの需要があれば多くの環境に提供できるようにしたいと考えています。

* Windows
* Blender2.8以降
## 使い方
### インストール

1. zipファイルの状態でアドオンを読み込みます。
![image](https://user-images.githubusercontent.com/78343605/201817616-4927a7c1-0fe7-40a4-b172-b8ad4cd4485a.png)


1. 画像エディタのプロパティパネルにAffinityBridgeが追加されているはずです。

![image](https://user-images.githubusercontent.com/78343605/201817774-24833aa3-a84c-4a1e-aa01-93ee27ba6204.png)

### すでに読み込んだ画像をAffinityBridgeする

画像エディタ上で対象の画像ファイルを開いた状態でBridge AffinityPhotoを実行します。

![image](https://user-images.githubusercontent.com/78343605/201818375-6f2d6952-2cda-4e04-a93a-9555cb4a553c.png)

RenderResult、ViewerNode、保存されていない画像をAffinityBridgeする
***

設定項目
* データフォーマット
* カラーモード
* ファイル名（有効時のみ利用されます）

を設定したあとにBridge_AffinityPhoto2を実行します。

![image](https://user-images.githubusercontent.com/78343605/201818886-e997702c-4826-449f-b8b4-487f5443331d.png)

自動的にファイルが保存されると同時にBlenderにロードされます。

![image](https://user-images.githubusercontent.com/78343605/201819390-56773089-e64b-4baf-8578-5240aa2e8b94.png)

Bridge AffinityPhoto Informationで出力された画像のパスを確認できます。

![image](https://user-images.githubusercontent.com/78343605/201819520-bb2884fd-a65e-4043-8dd9-4c3be0d1e7cd.png)

### AffinityPhoto2で作業した画像をBlenderに反映させる

再読み込みを実行

![image](https://user-images.githubusercontent.com/78343605/201819991-4bc6c4ef-d5ca-4ad5-80d2-9f891b6d8e2d.png)
