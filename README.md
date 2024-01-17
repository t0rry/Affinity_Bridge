<h1>AffnityBridge Addon V0.6.0 </h1>

![export](https://github.com/t0rry/Affinity_Bridge/assets/78343605/2ee80440-f5a9-401a-8057-0c9a0b8b58a7)
<h2>どういうアドオン？</h2>
BlenderとAffinityPhotoV2を強力に連携するために作成されました。</br>
現在はAffinityPhotoV2以外のソフトとの連携ができるようにアップデートを行っています。

<h2>機能</h2>
<h3>RenderLayer、ViewerNodeを直接エディタソフトで起動</h3>
Blender標準の「外部エディタで編集」はRenderLayer、ViewerNodeに対応していないため、対応。</br>
また、強力なエクスポーターによりPNG／JPEG／OpenEXR／OpenEXR(MultiLayer)に対応。</br>

exeファイルを指定することでAffinityPhotov2以外のエディタでも同様の機能が実行できます。</br>

<h3>読込み済みの画像を外部エディタソフトで起動</h3>
当然、Blenderに読み込まれた画像を外部エディタソフトで起動することができます。</br>

<h3>画像のリロード</h3>
エディタ側で保存した画像をリロードします。</br>
外部エディタソフトを用いたテクスチャペイントにとても便利です。</br>

<h3>選択ノードをOpenEXR(MultiLayer)で出力してくれるアウトプットノードを自動生成</h3>
コンポジットノードで選択されたノードをOpenEXR（MultiLayer）で出力するアウトプットノードを自動生成します。</br>
個人向けのカスタマイズされたグループノードで要素を出力するときなどに便利です。

<h3>シーンのレンダーレイヤをOpenEXR(MultiLayer)で出力してくれるアウトプットノードを自動生成</h3>
シーンのレンダーレイヤーの有効なパスを出力するアウトプットノードを自動生成します。</br>
レンダーレイヤーごと生成するため、ノード構成が複雑になってしまったシーンで純粋なパスだけを出力したいときに便利です。
