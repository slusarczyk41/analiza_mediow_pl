### Analiza stronniczości mediów internetowych w Polsce

Wykorzystując prosty mechanizm tworzenia wektorów znaczeniowych (word2bec) ze słów w tekście, popularnej
oraz dosyć prostej techniki NLP, porównać kontekst oraz sentyment wybranych słów kluczy, odnoszących się do polityki, w różnych domach mediowych.

Założenie jest takie, że **część z nich jest w jakiś sposób stronnicza (czy to pod względem lewicy, prawicy,  
lub unia/rosja)**, będę się więc starać udowodnić że tak nie jest, jak na statystyka przystało.
Wynik powinien być taki, że wektory wytrenowane na różnych zestawach danych (pochodzących z różnych gazet
internetowych) powinny wyjść dosyć podobne (przynajmniej pod względem tego, czy nacechowany jest
on pozytywnie czy negatywnie).

Porównam również słowa niezwiązane z polityką aby sprawdzić, czy to
porównanie ma w ogóle sens (nie ma go jeżeli dla neutralnych słów te wektory bardzo często się różnią).

### Struktura internetowych mediów w Polsce:

- [DE] Axel Springer SE/Ringier Holding AG > Axel Springer Media AG > Ringier Axel Springer PL: **Newsweek, Onet, Fakt**
- [PL] Agora SA: **Wyborcza, Gazeta**
- [PL] Hajdarowicz Grzegorz > KCI SA > Gremi media SA > Presspublica SA: **Rzeczpospolita, Życie Warszawy, Przekrój, Uwarzam Rze**
- [US] Discovery > TVN Group: **Tvn24**


- [LEWICA] Nie, fakty i mity, Gazeta wyborcza, Newsweek, Przekrój, Przegląd, Polityka
- [PRAWICA] Uważam rze, Do rzeczy, W sieci, Gazeta polska, Nasz dziennik, Gość niedzielny, Rzeczypospolita

Do dodania: Na temat, Wprost, Do rzeczy, Krytyka Polityczna, Radio maryja

### Klasteryzacja poglądów:

- Lewica/Prawica
- UE/Rosja/US
- PO/PIS

### Słowa klucze:

pis, po, duda, morawiecki, szydło, kaczyński, kwaśniewski, lewica, prawica,
lgbt, unia, eu, rosja, stany, premier, prezydent, opozycja, rząd, sejm, polska,
putin, trump

### Potrzebne dane:
- tytuł
- streszczenie
- treść artkułu
- podpisy pod zdjęciami
- (popularne) komentarze


### Plan działania:
1. Dla każdego medium:
- wyszykuję lub znajduję po tagach artykuły na temat zawierający słowo kluczowe.
- wstępnie obrabiam tekst, znajduję konkretne wystąpienia słów kluczy oraz ich najbliższe otoczenie
- z uzyskanych danych tworzę wektory znaczeniowe za pomocą word2vec lub glove
Dzięki czemu posiadam wektory dla każdego słowa-klucz unikalne dla każdej gazety internetowej
2. Dodatkowo,
- dla każdego medium stworzę wektory dla najpopularniejszych oraz neutralnych słów
- oraz porównam je pomiędzy gazetami,
aby dowiedziec się jak duża jest różnica pomiędzy nimi
- jeżeli jest ona niewiekla, to fakt korzystania z róznych zbiorów danych nie wpływa na wygląd wektora
- jeżeli jest ona duża, to sam już fakt korzystania z różnych zbiorów danych treningowych sprawia że są one różne
(i stąd różnice dla słów kluczowych mogą być sztuczne, niespowodowane różnicami w poglądach)
3. Łącze dane z:
- http://dsmodels.nlp.ipipan.waw.pl/ (wektory dla najczęstszych wyrazów języka polskiego)
- http://plwordnet.pwr.wroc.pl//wordnet/download-wordnet?key=1iflsj&file=4.0 (nacechowanie emocjonalne słów)
- <coś jeszcze z emocjami lub analizą sentymentu>
Dzięki temu mam przestrzeń, z której wybieram tylko te słowa dla których mam dane dotyczące sentymentu
4. Do tej przestrzeni dodaję słowa (wektory) wytrenowane na danych pochodzących z gazet, i
- wykorzystuję PCA aby narysować wykres w dwóch wymiarach i stwierdzić wizualnie czy danemu słowu
bliżej jest do grona słów o pozytywnym czy negatywnych znaczeniu
- wykorzystuję K-means ++ lub SVM aby kategoryzować dane słowa mechanicznie
5. Mogę również
- naszykować wzorce, które szukam w tekście, np "duda jest <kilka dodatkowych słów>"  
- ze wszystkich znalezionych wycinków wybrać słowa opisujące słowa-klucz
- narysować chmurę wyrazów aby mieć ogólny obraz
- przeprowadzić typową analizę sentymentu dla wszystkich wyrazów, +1 jeżeli pozytywne -1 jeżeli słowo jest negatywne
- oraz porównać wyniki pomiędzy gazetami
6. Przeprowadzić bardzo podobną analizę jak wyżej,
- biorąc tylko tutyłu artykułów
- oraz przeprowadzając analizę sentymentu dla tytułu
7. Na koniec warto porównać wszystkie wykorzystane metody
