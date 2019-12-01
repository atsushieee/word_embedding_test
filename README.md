# Word Embedding space Explanation:

## Getting Started

* Environment Requirements: **python 3.7.2**

### Prerequisites
1. [Qiitaの投稿](https://qiita.com/atsushieee/items/7b64b605de7d1646bf41) を参考に、wikipediaの情報をダウンロードし、NLPのコーパス用に整形
1. ダウンロードしたフォルダ一式をdataフォルダ以下に格納

### Installing

``` bash
# install dependencies
$ pip install -r requirements.txt
```

## Running the tests
1. 以下のコマンドを入力し、API用のweb アプリケーションを起動し、前処理を実行
``` bash
$ cd app
$ python app.py preprocess
```

1. 以下のコマンドを入力し、skipgramモデルにより導出した、類似単語をコンソールに表示
``` bash
$ python app.py skipgram
```

## Note
- Qiitaに、処理の説明を記載
  1. [日本語版wikipediaのデータ取得と整形](https://qiita.com/atsushieee/items/7b64b605de7d1646bf41)
  1. [テキストデータをNLPのコーパスとして活用するための事前処理](https://qiita.com/atsushieee/items/d002a27b8f1e270e28c8)


## License
The class is licensed under the [MIT License](https://opensource.org/licenses/MIT):

## Author
- Atsushi Tabata [@atsushieee](https://github.com/atsushieee)
- Author Email  [atsushi.tabata1204@gmail.com](mailto:atsushi.tabata1204@gmail.com)
