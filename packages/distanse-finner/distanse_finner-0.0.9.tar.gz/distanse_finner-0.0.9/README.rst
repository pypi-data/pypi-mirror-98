Finne avstander fra GPS posisjonsdata
=====================================

Dette er et lite bibliotek for å hente ut hvor langt man har bevegd
seg basert på GPX-filer fra en hvilken som helst GPS-logger, eller
CSV-filene laget med open-source appen GPSLogger for Android. 
Sistnevnte er en gratis app med åpen kildekode som lar deg logge GPS
spor uten at denne informasjonen deles med andre. Dessverre ble den
fjernet fra Play Store, men du kan finne installasjonsinstrukser på
https://gpslogger.app/

For å bruke dette biblioteket starter du scriptet ditt med

.. code:: python

    from distanse_finner import last_rådata
    
eller

.. code:: python

    from distanse_finner import last_uniform_data

Deretter kan du bruke denne kommandoen:

.. code:: python

    tidspunkt, avstander = last_rådata(datafil)

for å hente ut avstandsdata og tidspunktene de dataene er hentet på.
Dessverre klarer ikke GPS-loggere å måle posisjonen med like lang
tid mellom hver måling, så for å få uniformt fordelte data 
(altså data med like lang tid mellom hver måling), kan du bruke funksjonen:

.. code:: python

    tidspunkt, avstander = last_uniform_data(datafil, sekund_mellom_målinger)

hvor ``sekund_mellom_målinger`` er hvor mange sekund du ønsker mellom hver
måling.
