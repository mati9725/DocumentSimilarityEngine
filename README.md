# Document Similarity Engine

## Członkowie zespołu:

- Wojciech Szczęsny - [github](https://github.com/supermari0oo) [Linkedin](https://www.linkedin.com/in/wojciech-szczesny-info/)
- Mateusz Wieczorek - [github](https://github.com/mati9725) [Linkedin](https://www.linkedin.com/in/mateusz-wieczorek-pw/)

- Bartłomiej Zgórzyński - [github](https://github.com/zgorzynb) [Linkedin](https://www.linkedin.com/in/zgorzynb/)

## Cel projektu

Celem projektu będzie przygotowanie, przetestowanie oraz wdrożenie w pełni funkcjonalnego serwisu, którego zadaniem będzie rekomendacja artykułów Wikipedii w oparciu o jej podobieństwo do zadanego wyszukiwania. W tym celu wykorzystany zostanie główny komponent: Azure Fuctions.

## Zdobycie danych

Pierwszym krokiem projektu było zdobycie danych, które następnie wykorzystane zostaną do zasilenia naszego modelu. Podczas przeglądu rozwiązań udało nam się wybrać 3 możliwe drogi do osiągnięcia tego celu:

1. Łączenie się ze stroną internetową z wykorzystaniem biblioteki request, a następnie scrapowanie zawartości w wykorzystaniem parsera BeautifulSoup
2. Komunikacja z Wikipedią poprzez udostępnione API
3. Pobranie zrzutu (dumpa) Wikipedii 

Po rozmowie z Product Ownerem zdecydowaliśmy się na pierwsze podejście. Budowa oraz funkcjonowanie scrapera zostanie omówione poniżej.

## Scraper

Przygotowany scraper bazuje na wykorzystaniu bibliotek request oraz BeautifulSoup. Pierwsza z nich pozwala na uzyskanie zawartości strony internetowej o zadanym linku. Kolejna, pozwala na parsowanie zawartości strony i wydobycie tylko interesującej nas zawartości. 

Proces wydobywania danych rozpoczęliśmy od jednego, wybranego artykułu i linku do niego. Następnie z wybranego artykuły pobrane zostały tytuł artykułu oraz abstract (to co jest powyżej spisu treści) oraz wszystkie linki, będące odwołaniami do kolejnych stron Wikipedi. Uzyskane dane zapisywane były do bazy danych MS SQL SERVER, która została stworzona jako zasób w Microsoft Azure. Warto zaznaczyć, że przygotowane przez nas rozwiązanie jest zgodne z polityką Wikipedii. Algorytm skanuje plik robots.txt i nie wysyła zapytań do stron zablokowanych. Dodatkowo ograniczyliśmy częstość zapytań do 1 requesta na sekundę. 

Ponadto algorytm pozwala na uruchomienie scrapera na kilku maszynach jednocześnie!

 ## Wstępne przygotowanie danych

Dane zostały pobrane z bazy danych w formacie CSV. Pierwszym krokiem do stworzenia rozwiązania bazującego na algorytmach uczenia maszynowego jest odpowiednie przygotowanie danych. W tym wypadku również zostało to przeprowadzone. Poniżej przedstawię listę kolejnych przekształceń, które zostały przeprowadzone  na naszych danych:

- usunięcie oznaczeń odnośników np.  [15]
- usunięcie znaków nie-alfanumerycznych
- transformacja tekstu na małe litery
- usunięcie punktacji
- usunięcie wielokrotnych spacji
- usunięcie "stopwords" (słów, które często występują a nie niosą ze sobą informacji)
- tokenizacja 

Z tak przygotowanymi danymi możemy przejść do budowania modelu.

## Wybór modelu

Porównywanie danych tekstowych jest zagadnieniem trudnym i w większości przypadków wymaga transformacji tekstu do postaci liczbowej. Podczas przeglądu rozwiązań znaleźliśmy kilka, które pozwoliłyby na to przekształcenie:

1. TF-IDF
2. Bag of words
3. doc2vec model

Po konsultacjach z Product Ownerem zdecydowaliśmy się na wybór 3 algorytmu. Jest to algorytm bazujący na swoim poprzedniku word2vec, wzbogacony o dodatkową macierz. Doc2vec należy do rodziny rozwiązań uczenia nienadzorowanego. Sposób jego uczenia polega na predykcji kolejnych słów w paragrafie, a opiera się ono o algorytm Stochastic Gradient Decent (SGD), z kolei gradient wyznaczany jest przy pomocy propagacji wstecznej.

Tekst, który został przedstawiony w formie wektora o określonej długości może zostać porównany z innym wektorem poprzez odległość kosinusową. Im mniejsza ta wartość będzie, tym teksty są do siebie bardziej zbliżone.

## Szkolenie modelu

Szkolenie modelu przeprowadzone zostało lokalnie, na jednym z naszych komputerów. Do stworzenia modelu wykorzystany został język Python oraz biblioteka gensim. Plik treningowy dostępny jest [tutaj](https://github.com/mati9725/DocumentSimilarityEngine/blob/main/Model/train.py).

Dobór parametrów modelu przeprowadzony został poprzez wyszukiwanie najlepszej kombinacji parametrów z podanych list (grid search). Jako parametr określający jakość poszczególnych modeli, wykorzystana została skuteczność. Wyznaczana była ona dla całego zbioru treningowego i sprawdzała, czy wynikiem działania modelu dla zadanego tekstu będzie poprawny artykuł.

## Wykorzystanie rozwiązań Microsoft Azure



## Ocena dojrzałości rozwiązania



## Przykładowe zapytania

**Przykład 1** 

"Machine learning (ML) is the study of computer algorithms that improve automatically through experience.[1]
 It is seen as a part of artificial intelligence. Machine learning algorithms build a model based on sample data,
 known as "training data", in order to make predictions or decisions without being explicitly programmed to do so.[2]
 Machine learning algorithms are used in a wide variety of applications, such as email filtering and computer vision,
 where it is difficult or unfeasible to develop conventional algorithms to perform the needed tasks."

 **Otrzymane wyniki:**

1. 80.3% https://en.wikipedia.org/wiki/machine_learning
2. 67.4% https://en.wikipedia.org/wiki/visual_learning

3. 67.2% https://en.wikipedia.org/wiki/patient

Zgodnie z oczekiwaniami algorytm zwrócił na pierwszym miejscu artykuł, z którego pochodzi powyższy fragment. Można, by się spodziewać, że kolejne artykuły również będą związane z tematyką uczenia maszynowego lub sztucznej inteligencji, ale nie są. Niestety 3 link kompletnie nie pasuje to podanej frazy. Natomiast link otrzymany w drugim wyniku jest bardzo ciekawy. Zwrócony został styl uczenia się, w którym uczący musi zobaczyć informacje, aby je zrozumieć, co jest zgodne z ideą uczenia maszynowego. 

**Przykład 2** 

 Link wejściowy: https://en.wikipedia.org/wiki/Microsoft_Windows

  **Otrzymane wyniki:**

1. 63.6% https://en.wikipedia.org/wiki/operating_system
2. 61.9% https://en.wikipedia.org/wiki/linux
3. 53.7% https://en.wikipedia.org/wiki/java_(software_platform)

W drugim przypadku po podaniu linku do artykułu wikipedii wszystkie wyniki są blisko związane z tematyką w artykule wejściowym.

## Reprodukcja rozwiązania

Pierwszym krokiem reprodukcji rozwiązania będzie pobranie repozytorium.

W celu rozpoczęcia procesu scrapowania danych należy:



W celu rozpoczęcia nauki modelu należy:

- Pobrać dane z bazy w formacie CSV
- Zainstalowanie zależności zawartych w pliku requirements.txt
  - pip install -r requirements.txt
- Uruchomić plik train.py w celu uruchomienia treningu
- Skrypt test.py pozwala na testowanie rozwiązania zdalnie

W celu utworzenia rozwiązania w chmurze należy:



## Pozostałe artefakty

**Film demonstrujący działanie rozwiązania**

Pod tym [linkiem]() znajduje się krótki film demonstrujący działanie naszego rozwiązania.

**Diagram architektury**

![TEKST](https://github.com/mati9725/DocumentSimilarityEngine/blob/main/images/Architektura.PNG)

**Stos technologiczny**

- Python
- request
- BeatifulSoup
- gensim
- pandas
- HTML
- JQuery i Bootstrap

**Podział zadań**

- Scraping i deploy modelu - Wojciech Szczęsny, Mateusz Wieczorek
- Budowa i trening modelu - Bartłomiej Zgórzyński




## Ocena dojrzałości rozwiązania

* Rozwiązanie działa! 
* Jest skończone!
* Technologie są zaawansowane.
* Użyto serwisów Paas.

Oczywiście projekt jest jedynie prototypem rozwiązania, ale spełnia wszystkiego wymagania. Do jego uczenia wykorzystano jedynie 13.000 artykułów. Użycie zdecydowanie większej liczby artykułów znacząco poprawiłoby jakoś otrzymanego modelu. Oczywiście należałoby jeszcze poprawić wygląd naszej usługi, tak żeby była bardziej przyjazna dla użytkownika. Niestety żaden z członków naszego zespołu nie rozwija się w tych technologiach.


## Dlaczego użycia Azure Machine Learning to gorszy pomysł od Azure Functions? 

Podczas realizacji projektu udało nam się zrealizować projekt również za pomocą innych serwisów niż Azure Functions. 
Taką samą funkcjonalność uzyskaliśmy dzięki wrzuceniu lokalnie nauczonemu modelu do serwisu Azure Machine Learning. 
Ostatecznie porzuciliśmy ten kierunek z powodu wyższości Azure Functions nad Azure Machine Learnings:

* Koszty - przy użyciu serwisu Machine Learning ponosimy opłaty za korzystanie z tego serwisu
* Architektura - jeżeli mamy duży system, gdzie mamy tysiąc modeli Azure Machine Learning jest bardzo trudny do zarządzania, bo musimy wrzucić wiele modeli. Jeżeli chcielibyśmy mieć live predykcje dla tych wszystkich modeli, to musielibyśmy mieć tysiąc
oddzielnych serwisów. W przypadku Azure Function, jeżeli model jest położony na storage to możemy wczytywać dowolny model używając tylko jednego mikro serwisu, jako naszego end-pointu.
