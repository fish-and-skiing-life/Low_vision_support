# Low vision service - 弱視者向け情報収集支援アプリ

[![デモ動画](http://img.youtube.com/vi/TZeCFKSYbf8/0.jpg)](http://www.youtube.com/watch?v=TZeCFKSYbf8 "")


## Key features
### 音声読み上げ/音声操作
テキストの読み上げ機能，音声操作機能を実装しています．
テキスト読み上げと音声認識には Web Speech API を使用しています．

### 記事要約
ニュース記事の要約を提示します．

要約アルゴリズムはグラフベースの抽出型要約手法である[LexRank](https://www.aaai.org/Papers/JAIR/Vol22/JAIR-2214.pdf)を使用しています．
LexRankはNodeに文，Edge/Weightに文間類似度を使用した手法です．
本アプリでは，文間類似度の計算に[BERT](https://arxiv.org/abs/1810.04805)の特徴量を利用しています．
BERTモデルは東北大学 乾・鈴木研究室が公開している[学習済みモデル](https://github.com/cl-tohoku/bert-japanese)を使用しています．

### 単語トレンドの可視化
文章中のトレンドワードを拡大表示します．

単語トレンドの可視化の際には以下の処理を行っています．

まず，教師なしキーフレーズ抽出手法の[PositionRank](https://www.aclweb.org/anthology/P17-1102/)を使用して記事中からキーフレーズを抽出します．
次に，各キーフレーズの Google Trend Score の時系列データを取得します．
なお，生の Google Trend Score では日常的に検索される単語(e.g. 天気)のスコアが高くなりやすいという問題があるため，取得した Google Trend Score の時系列データに対して移動平均収束拡散法を適用し，スコアの変動量を求めます．これが最終的なトレンドスコアとなります．
このトレンドスコアが高いフレーズのフォントサイズを大きくすることで，トレンドの可視化を行っています．

![Low-vision_tech 002](https://user-images.githubusercontent.com/11304099/94304388-7626d100-ffaa-11ea-8c35-ce3000844594.png)

### 記事レコメンド
トレンドを考慮した記事レコメンドを行います．

レコメンドの際には以下の処理を行っています．

まず，記事中からキーフレーズを抽出した後，[GiNZA](https://github.com/megagonlabs/ginza)および[chiVe](https://github.com/WorksApplications/chiVe)(v1.1 mc5)を使用してキーフレーズをベクトル化します．
次に，各キーフレーズベクトルに対して，それぞれのキーフレーズのトレンドスコアを重みとして与えます．
これらの重み付けされたキーフレーズベクトルの平均が記事ベクトルとなります．
最後に，データベースに保存されている記事ベクトルとの間でcosine類似度を計算し，類似している記事上位5件を提示します．

![Low-vision_tech 003](https://user-images.githubusercontent.com/11304099/94304473-93f43600-ffaa-11ea-9770-ef4cc9de9b4e.png)

### 単語の意味検索
調べたい単語に関するWikipedia記事の概要を提示します．

Wikipedia記事の検索には[Wikipedia2Vec](https://wikipedia2vec.github.io/wikipedia2vec/)を使用し，入力された単語と最も類似している記事タイトルを取得しています．
これにより，Wikipedia記事のタイトルと完全に一致しない単語であっても，調べたい単語に該当する，あるいは類似する記事をサジェストすることが可能となっています．

![Low-vision_tech 004](https://user-images.githubusercontent.com/11304099/94305381-044f8700-ffac-11ea-9d4c-a9e0fea23496.png)


## Quick start
Docker，Docker-composeを使用．
```sh
# build and run app
docker-compose build
docker-compose up
```

`http://<YOUR LOCALHOST>:8080/` へアクセス．


## Data base
Tables
- Article
- Named entity
- Trend
- Wiki

### Article
記事の本文などのデータを格納する．

| Field   | Type         | Null | Key | Default | Extra          | 
| ------- | ------------ | ---- | --- | ------- | -------------- | 
| id      | int(11)      | NO   | PRI | NULL    | auto_increment | 
| url     | varchar(256) | NO   |     | NULL    |                | 
| title   | varchar(256) | NO   |     | NULL    |                | 
| content | longtext     | NO   |     | NULL    |                | 
| vector  | longtext     | YES  |     | NULL    |                | 

### Named entity
記事中のキーワードを格納する．

| Field  | Type         | Null | Key | Default | Extra          | 
| ------ | ------------ | ---- | --- | ------- | -------------- | 
| id     | int(11)      | NO   | PRI | NULL    | auto_increment | 
| url    | varchar(256) | NO   |     | NULL    |                | 
| word   | longtext     | NO   |     | NULL    |                | 
| vector | longtext     | YES  |     | NULL    |                | 

### Trend
キーワードのTrend scoreを格納する．

| Field | Type         | Null | Key | Default | Extra          | 
| ----- | ------------ | ---- | --- | ------- | -------------- | 
| id    | int(11)      | NO   | PRI | NULL    | auto_increment | 
| word  | varchar(256) | NO   |     | NULL    |                | 
| score | int(11)      | NO   |     | NULL    |                | 

### Wiki
Wikipediaの概要部分を格納する．データは[CirrusSearchダンプデータ](https://dumps.wikimedia.org/other/cirrussearch/current/)を使用．

| Field | Type         | Null | Key | Default | Extra          | 
| ----- | ------------ | ---- | --- | ------- | -------------- | 
| id    | int(11)      | NO   | PRI | NULL    | auto_increment | 
| title | varchar(256) | NO   |     | NULL    |                | 
| abst  | longtext     | NO   |     | NULL    |                | 
