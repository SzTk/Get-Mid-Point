Get-Mid-Point
=============
離れた地点に住んでいる複数の人が集まるのに
最も都合が良い場所を探す。
・移動時間に差が無いほうがよい。
・費用に差が無いほうが良い。
・とりあえず電車で移動する場合を考える。

＝＝＝以下は開発者向け＝＝＝＝＝
setup.pyの使い方

setup.pyとは
http://docs.python.jp/2/distutils/setupscript.html

setup.pyを使って開発していきましょう。

$ python setup.py develop

を実行することで、自分のpython環境にインストールされます。

※環境を汚したくない時はvirtualenv内で上記コマンドを実行すること。（自分はそうやっている
）
とりあえず自分の環境ではsetup.pyしてtestコードがが走ることは確認しました。
