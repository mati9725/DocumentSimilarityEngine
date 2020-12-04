# Document Similarity Engine

## Cel projektu

Celem projektu będzie przygotowanie, przetestowanie oraz wdrożenie w pełni funkcjonalnego serwisu, którego zadaniem będzie rekomendacja artykułów Wikipedii w oparciu o jej podobieństwo do zadanego wyszukiwania. W tym celu wykorzystane zostaną dwa główne komponenty: Azure Functions oraz Azure Storage.

## Zdobycie danych

1. Łączenie się ze stroną internetową - wykorzystanie biblioteki request
2. Scrapowanie – użycie parsera BeautifulSoup - można dostać bana 
3. Pakiet Wikipedia API 
4. Pobranie dumpa Wikipedii

## Przygotowanie danych

1. Oczyszczenie danych - (lower, strip, tokenizacja, stop words, itd)

2. Przedstawienie dokumentu w formie wektora:

   - **TF-IDF**

     ![](https://cdn-media-1.freecodecamp.org/images/1*q3qYevXqQOjJf6Pwdlx8Mw.png)

     TF - częstotliwość występowania słowa w danym dokumencie

     IDF- współczynnik używany do obliczenia wagi rzadkich słów we wszystkich dokumentach. Słowa, które rzadko wystękują mają wysoki IDF. Faworyzacja słów, które występują w niewielu dokumentach –  większa siła dyskryminacyjna.

     TF  - IDF połączenie powyższych wskaźników.

     Do obliczania powyższej macierzy można wykorzystać bibliotekę sklearn do Pythona. 

   - **doc2vec**

     Bardziej zaawansowane narzędzie do reprezentacji dokumentu w formie wektora.

## Search Engine

- Proste porównanie poprzez odległość cosinusową pomiędzy wektorami
- Model ML, którego zadaniem będzie przygotowanie rankingu - Learning to rank
- Gotowy Search Engine

## Gotowe rozwiązania

- [Full text search in Azure Cognitive Search](https://docs.microsoft.com/en-us/azure/search/search-lucene-query-architecture?fbclid=IwAR1xzNhtWgpP-fEdo57_DFJIpccRtPVvYN_R1yZ966uLzYQs6gdibyzJJRI)

  

## Pytania 

- Czy repozytorium ma/może być publiczne?

- Czy możemy kontaktować się w trakcie wykonywania projektu, gdyby pojawiły się niejasności lub problemy w realizacji projektu? Jeśli tak, to w jakiej formie (MS Teams, wiadomość mailowa, spotkania na Teams)?

  
