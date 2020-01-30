## Analiza stronniczości mediów internetowych w Polsce

Wykorzystując prosty mechanizm tworzenia wektorów znaczeniowych (word2bec) ze słów w tekście, popularnej
oraz dosyć prostej techniki NLP, porównać kontekst oraz sentyment wybranych słów kluczy, odnoszących się do polityki, w różnych domach mediowych.

Założenie jest takie, że **część z nich jest w jakiś sposób stronnicza (czy to pod względem lewicy, prawicy,  
lub unia/rosja)**, będę się więc starać udowodnić że tak nie jest, jak na statystyka przystało.
Wynik powinien być taki, że wektory wytrenowane na różnych zestawach danych (pochodzących z różnych gazet
internetowych) powinny wyjść dosyć podobne (przynajmniej pod względem tego, czy nacechowany jest
on pozytywnie czy negatywnie).

Porównam również słowa niezwiązane z polityką aby sprawdzić, czy to
porównanie ma w ogóle sens (nie ma go jeżeli dla neutralnych słów te wektory bardzo często się różnią).

## Struktura internetowych mediów w Polsce:

###### Kraje:

- [DE] Axel Springer SE/Ringier Holding AG > Axel Springer Media AG > Ringier Axel Springer PL: **Newsweek, Onet, Fakt**
- [PL] Agora SA: **Wyborcza, Gazeta**
- [PL] Hajdarowicz Grzegorz > KCI SA > Gremi media SA > Presspublica SA: **Rzeczpospolita, Życie Warszawy, Przekrój, Uwarzam Rze**
- [US] Discovery > TVN Group: **Tvn24**

###### Poglądy:

- [LEWICA] Nie, fakty i mity, Gazeta wyborcza, Newsweek, Przekrój, Przegląd, Polityka
- [PRAWICA] Uważam rze, Do rzeczy, W sieci, Gazeta polska, Nasz dziennik, Gość niedzielny, Rzeczypospolita

Do dodania: Na temat, Wprost, Do rzeczy, Krytyka Polityczna, Radio maryja

### Walidacja podejścia:

1. 


### Słowa klucze:

sąd najwyższy,
imigranci,
ekologia,
emigracja,
pis,
platforma,
duda,
morawiecki,
szydło,
kaczyński,
kwaśniewski,
lewica,
prawica,
lgbt,
unia+europejska,
rosja,
stany,
premier,
prezydent,
opozycja,
rząd,
sejm,
polska,
putin,
trump,
ukraina,
media,
bank,
polska,
niemcy,
papież,
kościół,
korwin,
rydzyk,
feminizm,
leszek miller

### Potrzebne dane:
- tytuł
- streszczenie
- treść artkułu
- podpisy pod zdjęciami
- (popularne) komentarze


## Plan działania (wektory) wersja 2:
1. Dla każdego słowa-klucz wybieram słowa-odniesienia pozytywne oraz negatywne
2. Dla każdej gazety oddzielnie tworzę wektory, wyciągam z nich wektory do słów-kluczy
3. Dla wszystkich gazet tworzę wektory, wyciągam z nich wektory do słów-odniesień
4. Pobieram wektory wytrenowane na narodowym korpusie języka polskiego
5. Jeżeli słów-odniesień jest więcej niż jedno to wyliczam srodek
6. Dla każdego słowa klucz wyliczma odległość od słowa-odniesienia pozytywnego oraz słowa-odniesienia negatywnego
7. Z tych dwóch miar wyliczam jedną w zakresie (0, 1), która mówi mi czy dana gazeta wypowiada się na dany temat w pozytywny (1) lub negatywny (0) sposób

###### Wybór słów-odniesień
Problem jest taki, że mogę to zrobić wykorzystując dwa zbiory wektorów, i każda metoda ma swoje plusy i minusy:
1. Wytrenowanych na artykułach wszystkich gazet - ryzykuję wtedy, że wektory są obiążone w jakiś sposób, ale odnoszą się one do słów-kluczy w lepszy sposób. Np: jeżeli wybiorę jako słowo-odniesienia negatywne "komunizm" do słowa-klucz, to pomimo tego że obiektywnie słowo to ma zły wydźwięk (i dlatego tez nadaje się jako słowo odniesienia do partii politycznych lub ogólnie do rządu), to fakt że w niektórych gazetach jest on opisywany w pozytywnym kontekście rzutuje na wektor i umniejsza jego wartość jako punkt odniesienia.

2. Wytrenowanych na narodowym korpusie języka polskiego - wtedy mam większą pewność że wektory słów-odniesień są nieobciążone, ale ze względu na inne źródło danych (wikipedia lub słownik języka polskiego) mogą być one mniej odnośne (relevant), związane z tematem analizy.



<!-- ### Plan działania:
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
- jeżeli jest ona duża, to sam już fakt korzystania z różnych zbiorów danych treningowych sprawia że są one różne (i stąd różnice dla słów kluczowych mogą być sztuczne, niespowodowane różnicami w poglądach)

3. Łącze dane z:


Dzięki temu mam date, z której wybieram tylko te słowa dla których mam dane dotyczące sentymentu

4. Do tych danych dodaję słowa (wektory) wytrenowane na danych pochodzących z gazet, i

- wykorzystuję PCA aby narysować wykres w dwóch wymiarach i stwierdzić wizualnie czy danemu słowu
bliżej jest do grona słów o pozytywnym czy negatywnych znaczeniu
- wykorzystuję K-means ++ lub SVM aby kategoryzować dane słowa mechanicznie -->

## Mogę również wyrysować chmurę słów

- naszykować frazy, które szukam w tekście, np r"duda jest <kilka dodatkowych słów>"  
- ze wszystkich znalezionych wycinków wybrać słowa opisujące słowa-klucz
- narysować chmurę wyrazów aby mieć ogólny obraz

## Oraz badać sentyment

- biorąc tylko tutyły artykułów lub inne części
- wyliczając sentyment na podstawie różnych słowników wyraz-sentyment

## Na koniec warto porównać wszystkie wykorzystane metody




###### Źródła:
- http://clip.ipipan.waw.pl/LRT
- http://zil.ipipan.waw.pl/


- http://dsmodels.nlp.ipipan.waw.pl/ (wektory dla najczęstszych wyrazów języka polskiego)
- http://plwordnet.pwr.wroc.pl//wordnet/download-wordnet?key=1iflsj&file=4.0 (nacechowanie emocjonalne słów)
- http://zil.ipipan.waw.pl/SlownikWydzwieku (słowo-sentyment)
