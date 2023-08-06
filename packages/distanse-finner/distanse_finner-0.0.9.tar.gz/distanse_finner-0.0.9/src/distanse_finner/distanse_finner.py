from pathlib import Path
from pandas import read_csv, to_datetime, DataFrame
from pylab import arange, arcsin, array, cos, pi, sin, sqrt
from scipy.interpolate import interp1d
from warnings import warn
# Last inn gpxpy kun dersom det er installert
try:
    import gpxpy
    HAR_GPXPY = True
except ImportError:
    HAR_GPXPY = False


def sjekk_at_gpxpy_er_installert():
    """Vis en feilmelding med installasjonsinstrukser om GPXPY ikke er installert.
    """
    if not HAR_GPXPY:
        raise ValueError(
            "Du må installere gpxpy for å bruke gpx-filer. "
            "Den letteste måten å installere gpxpy er med Spyder eller "
            "Jupyter Notebooks. Med Spyder skriver du `!pip install gpxpy` "
            "i terminalvinduet, og trykker <Enter>. Med Jupyter Notebooks "
            "skriver du `!pip install gpxpy` i en celle du kjører."
        )


def haversinus(vinkel):
    """Haversinus funksjonen
    
    Brukes for å regne ut vinkelen mellom to punkt på et kuleskall
    
    Du kan lese om denne funksjonen her
    https://en.wikipedia.org/wiki/Versine
    """
    return sin(vinkel/2)**2


def arc_haversinus(forhold):
    """Den inverse haversinus funksjonen
    
    Brukes for å regne ut vinkelen mellom to punkt på et kuleskall
    
    Du kan lese om denne funksjonen her
    https://en.wikipedia.org/wiki/Versine
    """
    return 2*arcsin(sqrt(forhold))


def sentralvinkel(
    lengdegrad1, breddegrad1, lengdegrad2, breddegrad2,
):
    """Finner sentralvinkelen mellom to punkt på et kuleskall
    
    For å finne sentralvinkelen brukes haversinus formelen,
    som du kan lese om her:
    https://en.wikipedia.org/wiki/Haversine_formula
    """
    lengdegrad_diff = lengdegrad2 - lengdegrad1
    breddegrad_diff = breddegrad1 - breddegrad2
    
    ledd1 = haversinus(lengdegrad_diff)
    ledd2 = cos(lengdegrad1)*cos(lengdegrad2)*haversinus(breddegrad_diff)
    
    return arc_haversinus(ledd1 + ledd2)


def avstand(
    lengdegrad1, breddegrad1, lengdegrad2, breddegrad2, radius
):
    """Finner avstanden mellom to punkt på et kuleskall.
    
    Du kan lese mer om haversinus formelen vi bruker her
    https://en.wikipedia.org/wiki/Haversine_formula
    
    Vinkelene er lister 
     * Første element er lengdegrad 
     * Andre element er breddegrad
    """
    return radius*sentralvinkel(lengdegrad1, breddegrad1, lengdegrad2, breddegrad2)


def jordavstand(
    lengdegrad1, breddegrad1, lengdegrad2, breddegrad2
):
    """Finn luftavstand mellom to punkt på jordoverflata i km.
    
    Her bruker vi en kuleapproksimasjon av jorda, men siden jorda
    er elliptisk vil tallene være noe feil med veldig store
    avstander (f.eks avstand mellom to fjerne land).
    """
    jord_radius_km = 6371
    
    return avstand(
        lengdegrad1, breddegrad1, lengdegrad2, breddegrad2, jord_radius_km
    )


def grad_til_radian(grad):
    """Gjør om grader til radianer
    """
    return grad*pi/180


def finn_tidsendring_i_sekunder(tidspunkt1, tidspunkt2):
    """Finner tidsendring i sekund mellom to tidspunktsvariabler.
    """
    tidsendring = tidspunkt1 - tidspunkt2
    return tidsendring.seconds + tidsendring.microseconds/1_000_000


def hent_forflyttningsdata(data):
    """Lager en array som inneholder hvor langt man har bevegd seg i kilometer ved den gitte målingen.
    """
    forflytning_siden_start = [0]
    
    # Vi starter med å ikke ha noen posisjon
    nåværende_lengdegrad = None
    nåværende_breddegrad = None
    for tidspunkt, rad in data.iterrows():
        forrige_lengdegrad = nåværende_lengdegrad
        forrige_breddegrad = nåværende_breddegrad
        nåværende_lengdegrad = grad_til_radian(rad['lon'])
        nåværende_breddegrad = grad_til_radian(rad['lat'])
        
        # Hvis vi ikke har noen forrige posisjon
        # så fortsetter vi til neste iterasjon
        if forrige_lengdegrad is None:
            continue
        
        # Regn ut avstanden vi har bevegd oss
        posisjonsendring = jordavstand(
            forrige_lengdegrad,
            forrige_breddegrad,
            nåværende_lengdegrad,
            nåværende_breddegrad
        )
        
        # Legg til den avstanden i forflytningen vår
        nåværende_forflytning = forflytning_siden_start[-1] + posisjonsendring
        
        # Plasser den nåværende forflytningen på slutten av forflytningslista
        forflytning_siden_start.append(nåværende_forflytning)
    
    return array(forflytning_siden_start)


def hent_tidsdata(data):
    """Lager en array som inneholder hvor lenge man har bevegd seg i sekunder ved den gitte målingen.
    """
    sekunder_siden_start = [0]
    
    nåværende_tidspunkt = None
    for indeks, rad in data.iterrows():
        forrige_tidspunkt = nåværende_tidspunkt
        nåværende_tidspunkt = indeks
        if forrige_tidspunkt is None:
            continue
        
        tidsendring = finn_tidsendring_i_sekunder(
            nåværende_tidspunkt, forrige_tidspunkt
        )
        tid_siden_start = sekunder_siden_start[-1] + tidsendring
        sekunder_siden_start.append(tid_siden_start)
    
    return array(sekunder_siden_start)


def hent_uniform_data(data, tid_mellom_målinger_s=5):
    """Gjør om datasettet slik at alle målingene er like langt unna hverandre
    
    Trekker en rett linje mellom hvert datapunkt 
    (slik som når vi plotter) og henter ut forflyttningsdata
    med like langt tid mellom hver måling.
    
    Returnerer avstander og tidspunkt.
    """
    tidspunkt_s = hent_tidsdata(data)
    avstander_km = hent_forflyttningsdata(data)
    
    interpolant = interp1d(tidspunkt_s, avstander_km)
    tidspunkt_uniform = arange(0, tidspunkt_s[-1], tid_mellom_målinger_s)
    
    return tidspunkt_uniform, interpolant(tidspunkt_uniform)


def last_rådata_gpslogger(datafil):
    data = read_csv(datafil).set_index('time')
    data.index = to_datetime(data.index)
    data = data[data['provider'] == 'gps']  # Bruk kun rander hvor posisjonsdata kommer fra GPSen
    
    tidspunkt_s = hent_tidsdata(data)
    avstander_km = hent_forflyttningsdata(data)
    
    return tidspunkt_s, avstander_km


def last_uniform_data_gpslogger(datafil, tid_mellom_målinger_s):
    data = read_csv(datafil).set_index('time')
    data.index = to_datetime(data.index)
    data = data[data['provider'] == 'gps']  # Bruk kun rander hvor posisjonsdata kommer fra GPSen
    
    return hent_uniform_data(data, tid_mellom_målinger_s)


def last_rådata_gpx(datafil, track=None):
    with open(datafil, 'r') as gpxfile:
        gpx = gpxpy.parse(gpxfile)
        if len(gpx.tracks) > 0 and track is None:
            warn(
                "Det er mer en ett track i gpx filen, henter det første "
                "om du ønsker track nummer `n`, må du spesifisere `track=n-1` når "
                "du laster inn dataen (f.eks. `last_rådata(datafil, track=2)` "
                "å hente inn track nummer 3).\n\n"
                "For å fjerne denne advarselen kan du kalle på denne funksjonen med "
                "`track=0`."
            )
            track = 0
        
        data = []
        for segment in gpx.tracks[track].segments:
            for point in segment.points:
                rad = {
                    'lat': point.latitude,
                    'lon': point.longitude,
                    'time': point.time
                }
                data.append(rad)
        data = DataFrame(data).set_index('time')
    
    tidspunkt_s = hent_tidsdata(data)
    avstander_km = hent_forflyttningsdata(data)
    
    return tidspunkt_s, avstander_km


def last_uniform_data_gpx(datafil, tid_mellom_målinger_s, track=None):
    with open(datafil, 'r') as gpxfile:
        gpx = gpxpy.parse(gpxfile)
        if len(gpx.tracks) > 0 and track is None:
            warn(
                "Det er mer en ett track i gpx filen, henter det første "
                "om du ønsker track nummer `n`, må du spesifisere `track=n-1` når "
                "du laster inn dataen (f.eks. `last_uniform_data(datafil, dt, track=2)` "
                "å hente inn track nummer 3).\n\n"
                "For å fjerne denne advarselen kan du kalle på denne funksjonen med "
                "`track=0`."
            )
            track = 0
        
        data = []
        for segment in gpx.tracks[track].segments:
            for point in segment.points:
                rad = {
                    'lat': point.latitude,
                    'lon': point.longitude,
                    'time': point.time
                }
                data.append(rad)
        data = DataFrame(data).set_index('time')
    
    return hent_uniform_data(data, tid_mellom_målinger_s)
    

def last_rådata(datafil, track=None):
    """Last inn rådata fra en gpx-fil eller en GPSLogger csv-fil.
    """
    datafil = Path(datafil)
    if datafil.suffix == '.gpx':
        sjekk_at_gpxpy_er_installert()
        return last_rådata_gpx(datafil, track=track)
    elif datafil.suffix == '.csv':
        if track is not None:
            warn("Du kan kun spesifisere track dersom du bruker gpx-filer.")
        return last_rådata_gpslogger(datafil)
    else:
        raise ValueError("Filtypen må enten være csv (for GPSLogger csv filer) eller gpx.")


def last_uniform_data(datafil, tid_mellom_målinger_s, track=None):
    """Gjør om datasettet slik at alle målingene er like langt unna hverandre
    
    Trekker en rett linje mellom hvert datapunkt 
    (slik som når vi plotter) og henter ut forflyttningsdata
    med like langt tid mellom hver måling.
    
    Returnerer avstander og tidspunkt.
    """
    datafil = Path(datafil)
    if datafil.suffix == '.gpx':
        sjekk_at_gpxpy_er_installert()
        return last_uniform_data_gpx(datafil, tid_mellom_målinger_s, track=track)
    elif datafil.suffix == '.csv':
        if track is not None:
            warn("Du kan kun spesifisere track dersom du bruker gpx-filer.")
        return last_uniform_data_gpslogger(datafil, tid_mellom_målinger_s)
    else:
        raise ValueError("Filtypen må enten være csv (for GPS tracker csv filer) eller gpx.")