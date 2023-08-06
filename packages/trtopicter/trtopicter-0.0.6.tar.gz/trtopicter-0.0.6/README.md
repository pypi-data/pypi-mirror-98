# TrTopicter 🇹🇷

[![Python](https://img.shields.io/pypi/pyversions/tensorflow.svg?style=plastic)](https://badge.fury.io/py/trtopicter)
[![PyPI](https://badge.fury.io/py/tensorflow.svg)](https://badge.fury.io/py/trtopicter)

TrTopicter is a ready-use fasttext machine learning model to detect the topic of given Turkish text. Language detection
is stacked before the model to avoid analyzing non-Turkish text that may potentially pave the way to erroneous
responses. The deployed model was trained with almost 30K Turkish annotated sentences/paragraphs, and an averaged F-1
measure of 94.37 % is achieved. Execution time for a given text that has over 300 characters is lower than 1 ms and
resource usage is only 6 MB.

## Install

Pypi installation is available. Tested on Windows 8 / 10, Ubuntu 18.04 / 20.04 and OSX Catalina 10.15.7

```sh
$ pip install trtopicter
```

## Supported Topics

**politics** - **economy** - **health** - **sport** - **technology** - **culture** - **religion** - **justice**

## Pre-processings

- Case-folding to lower case
- Punctuation, numbers and white space removal
- Stop words removal (
  credits: https://github.com/ahmetaa/zemberek-nlp/blob/master/experiment/src/main/resources/stop-words.tr.txt)

## Configuration

```JSON
{
  "LANGUAGE_IDENTIFICATION": {
    "limit": {
      "character": 500
    },
    "probability_threshold": 0.2
  },
  "DOMAIN_DETECTION": {
    "limit": {
      "character": 500
    },
    "probability_threshold": 0.5
  }
}
```

`character` : Number of characters threshold for detection, data type is integer

`probability_threshold`: Probablity threshold for detection, data type is float

## Usage

Create an object from TrTopicter class and easily pass a string to get_topic method.

```python
>>> from trtopicter install TrTopicter

>>> topicter = TrTopicter()

>>> print(topicter.get_topic("""
Epidemiyoloji:HIV infeksiyonu ile birlikte dünyada Tbc olgularında artış görülmüştür.
İnfeksiyon hastalıkları içerisinde morbidite ve mortalitesi en yüksek olandır. 
Kişide infeksiyona yatkınlıkbulaşmada önemlidir (genetik faktörler).
Mycobacteria tuberculosis aside dirençli bir bakteri olup Ehrlich-Ziehl-Neelsen boyama yöntemi ilemavi bir 
zemin üzerinde kırmızı çomaklar halinde görülür.Deri tüberkülozu:Deride M tuberculosis, M bovis ve 
bazı durumlarda Bacillus Calmette-Guerin (BCG) infeksiyona neden olur. Tbc yaygın görülmekle beraber etkenler ne 
çok virülandır ne de infeksiyözdür. M. tuberculosis infeksiyonunun ancak %5-10‟u hastalık yapar. 
M tuberculosis dokuda latent bir şekilde kalabilir, tedaviye yanıt vermez ve reaktivasyon gösterebilir"""))

{'label': 'health', 'probability': 1.0}

>>> print(topicter.get_topic("""
Salgından etkilenen altının gram fiyatı, güne yükselişle başlamasının ardından 473,8 liradan işlem görüyor. 
Aynı dakikalarda çeyrek altın 775 lira, Cumhuriyet altını da 3.163 liradan satılıyor.
Dün, altının ons fiyatı ve dolar kurundaki düşüşe paralel değer kaybeden gram altın, 
günü bir önceki kapanışın yüzde 7,7 altında 468 liradan tamamladı.
SALGIN ALTININ ONS FİYATINI ETKİLİYOR
Gram altın, yeni güne değer kazancıyla başlamasının ardından saat 10.55 itibarıyla önceki kapanışın 
yüzde 1,2 üzerinde 473,8 liradan işlem görüyor. Aynı dakikalarda çeyrek altın 775 lira, 
Cumhuriyet altını da 3.163 liradan satılıyor.
"""))

{'label': 'economy', 'probability': 1.0}

>>> print(instance.get_topic("""
Onlar yıllardır yeşil sahalarda sergiledikleri futbolla tuttuğumuz takımları galibiyete taşıyor,
Milli takımla bizleri temsil ediyor. Ancak dediğimiz gibi yıllardı. Yıllardır Süper Lig'de 
izlediğimiz futbolcuların gençlik zamanları ve şimdiki halleri arasındaki değişimleri sizi
çok şaşırtacak. A Milli Futbol Takımı'nın UEFA Uluslar B Ligi 3. Grup'ta 18 Kasım Çarşamba
günü Macaristan ile deplasmanda oynayacağı maçı Slovak hakem Ivan Kruzliak yönetecek.
Türkiye Futbol Federasyonunun internet sitesinde yer alan açıklamaya göre, 
başkent Budapeşte'deki Puşkaş Arena'da TSİ 22.45'te başlayacak karşılaşmada düdük çalacak 
Kruzliak'ın yardımcılıklarını Tomas Somolani ve Branislav Hancko yapacak.
Karşılaşmanın dördüncü hakemi ise Filip Glova olacak.
"""))

{'label': 'sport', 'probability': 1.0}
```

## To-do

- Increase number of topics
- Cython support

## Resources

* [Fasttext](https://arxiv.org/abs/1607.01759)
* [Topic Classification Survey](https://arxiv.org/abs/2004.03705)

