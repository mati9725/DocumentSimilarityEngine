# DocumentSimilarityEngine

![](https://cdn-media-1.freecodecamp.org/images/1*q3qYevXqQOjJf6Pwdlx8Mw.png =300x)

TF- częstotliwość występowania słowa w danym dokumencie

IDF- współczynnik używany do obliczenia wagi rzadkich słów we wszystkich dokumentach. Słowa, które rzadko wystękują mają wysoki IDF. Faworyzacja słów, które występują w niewielu dokumentach –  większa siła dyskryminacyjna.

TF-IDF połączenie powyższych wskaźników.

Do obliczania powyższej macierzy można wykorzystać bibliotekę sklearn do Pythona. 

![](https://upload.wikimedia.org/wikipedia/en/f/fa/MLR-search-engine-example.png =300x)


## Full text search in Azure Cognitive Search

https://docs.microsoft.com/en-us/azure/search/search-lucene-query-architecture?fbclid=IwAR166H8Ym1SgOgK9mmvPHRCXMUpqmQxeD88H3pvXfIOHFKG7uZT-oWisxAw

## Python & Web scraping

1. Łączenie się ze stroną internetową - wykorzystanie biblioteki request.
2. Scrapowanie – użycie parsera BeautifulSoup.
3. Pakiet Wikipedia API 
4. Pobranie dumpa wikipedii

## Obróbka danych

* Usunięcie zbędnych znaków interpunkcyjnych, liczb, oraz często występujących słów jak np. "i", "lub", "oraz".
* Wygenerowanie macierzy

## Działanie

* Obliczenie odległości kosinusowej pomiędzy zapytaniem, a dokumentem
	- Konwersja zapytania na reprezentację wektorową
	- Obliczanie odległości od próbki do elementów z bazy
	- Wybranie dokumentów z najlepszym wynikiem

## Przygotowanie modelu

* Wybranie cech modelu do uczenia np. długość dokumentu, współczynniki TF-IDF...
* 



