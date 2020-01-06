
ETLCDB Image Extractor
======================

Utility to extract image data from ETL Character Database, which contains 1.2 million Japanese character images (most of them are handwritten).


Overview
--------

[ETL Character Database (ETLCDB)](http://etlcdb.db.aist.go.jp/) is Japanese character datasets including both handwritten and machine-printed.
Characters consists of Japanese daily used characters such as hiragana, katakana, kanji, numerals, symbols and Latin alphabets.

Datasets is a little difficult to handle with because they have unique binary data format rather than a modern data format like JSON or XML.

This utility enables to extract all charcter images that link unicode code point.
Though ETLCDB contains 9 datasets (ETL-1 to ETL-9) and each of those has different data format,
this utility can handle with all of those datasets.

ETLCDB dataset is free to use but **allowed only for non-commercial use**. cf.) [Conditions of Use](http://etlcdb.db.aist.go.jp/obtaining-etl-character-database)


Usage
-----

1. Download the dataset.
   To download ETLCDB dataset, you must register form the official website and get the password for the download link.
2. git clone this repository
```
    git clone https://github.com/choo/etlcdb-image-extractor.git
```
3. Unzip donwloaded dataset file move it to `etl_data` directory. Dataset directoty will be located under `etl_data` like `etl_data/ETL1`.
4. Install required pip modules
```
    pip install -r requirements.txt
```
5. Run the command.
```
    python etl_extractor.py
```
   You can know options for execution using `--help` option

Note: tested only on Ubuntu16.04 + Python3.6 environment


Licence
-------

[MIT](https://github.com/tcnksm/tool/blob/master/LICENCE)


Memos
-----

  

### About each dataset

- Summarized descriptions about datasets is as follows (Details is in the officail web page).

|#  |hira|kata|kanji|symb|total |each     |sample  |year  |reso   |size    | format|info|
|--:|---:|---:|----:|---:|-----:|--------:|-------:|-----:|------:|-------:|------:|---|
|1  | 0  |51  |   0 |48  |  99  |approx.1400  |141319  |1973  |64x63  |101 MB  | M-type|自由手書き, num(10) + alpha(26) + symbol(12)|
|2  | ?  | ?  |   ? | ?  |2184  |approx.24  | 52796  |1973  |60x60  | 40 MB  |       |印刷漢字, 6 bits, CO-59 characters|
|3  | 0  | 0  |   0 |48  |  48  |    200  |  9600  |1974  |72x76  |  9 MB  | C-type|    |
|4  |51  | 0  |   0 | 0  |  51  |    120  |  6120  |1974  |72x76  |  5 MB  | C-type|    |
|5  | 0  |51  |   0 | 0  |  51  |approx.200  | 10608  |1975  |72x76  |  8 MB  | C-type|104 people|
|6  | 0  |46  |   0 |68  | 114  |   1383  |157662  |1976  |64x63  |159 MB  | M-type|    |
|7  |46  | 0  |   0 | 2  |  48  |    160  | 16800  |1977  |64x63  | 36 MB  | M-type|hira, dakuten, han-dakuten|
|8  |75  | 0  | 881 | 0  | 956  |    160  |152960  |1980  |128x127|135 MB  |       |JIS X 0208|
|9  |71  | 0  |2965 | 0  |3036  |    200  |607200  |1984  |128x127|561 MB  |       |JIS X 0208|


### Detailed Data format of each dataset

- ETL1, 6, 7
    - M-type data format
    - JIS X 0201 (hankaku hira, kata, latin, num, symbols)
    - all characters are half width

- ETL2
    - CO-59 (六社協定新聞社用文字コード)
    - 印刷漢字データベース
    - [Code Mapping Image](http://etlcdb.db.aist.go.jp/etlcdb/etln/etl2/e2code.jpg)
        - the same file is on the "charcode_data" directory
    - all characters including latin alphabet and numbers are full width

- ETL3, 4, 5
    - C-type data format
    - JIS X 0201
    - [format description of ETL4](http://etlcdb.db.aist.go.jp/specifications-of-etl4)
        - Note that on the table, 1 byte is refered to as 6 bits
    - all characters are half width

- ETL8 and 9
    - almost the same, but have different size of data padding just before the image data
  

### About JIS X 0201/0208

#### JIS X 0201

- mapping file was downloaded from [here](http://www.unicode.org/Public/MAPPINGS/OBSOLETE/EASTASIA/JIS/JIS0201.TXT)
- JIS X 0201 and Unicode mappings is on [this web page](http://charset.7jp.net/jis0201.html), but useful only for Japanese users.

#### JIS X 0208

- mapping file was downloaded from [here](http://unicode.org/Public/MAPPINGS/OBSOLETE/EASTASIA/JIS/JIS0208.TXT)
- JIS X 0208 (1990) and Unicode mappings is on [this web page](http://charset.7jp.net/jis0208.html), but useful only for Japanese users.
