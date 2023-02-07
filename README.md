# cinecli

Estoy yendo 2 veces por semana al Cairo y siempre voy a la página con una interfaz de mierda a fijarme
que es lo que van a pasar, y de paso nunca la entiendo.

## Dependencias

```terminal
pip install ics icalendar climage requests colorama click arrow beautifulsoup4
```

## Run

```terminal
python3 cinecli.py --help
```

Tested in linux mint 21.

## More info
Cada cine es un comando y un grupo de comandos de click.

Cada cine tendrá su API, cada API, cuando se consulten, devolverá un json del tipo:

```terminal
{
  <otros eventos>
  ...
  "<id unico del evento>": {
    "name": "Una película",
    "begin": "02-02-2023 20:30:00 (en 19 horas)",
    "url": "https://<sarasa>",
    "image_url": "https://<sarasa>"
    "extra_info": {
        "DIRECCIÓN": "Fincher!",
        "ELENCO": "Paul Mescal, Francesca Corio, Celia Rowlson-Hall, Kayleigh Coleman, Sally Messh, names, names",
        "GÉNERO": "Drama",
        "DURACIÓN": "98’",
        "ORIGEN": "Estados Unidos, Reino Unido",
        "AÑO": "2022",
        "CALIFICACIÓN": "SAM13 (Para Mayores de 13 años)"
    }
  },
  ...
  <otros eventos>
}
```
En este momento la API del cairo está impletada leyendo archivos .ics que El Cario provee en la página.
De otros cines todavía no encontré nada parecido.
Tal vez use un crawler en algún momento con alguno para ver que onda y vea si puedo resolver algo.

Si alguien encuentra algún archivo .ics de otros cines la mejor.

# Screenshots

![scrotFeb07012106](https://user-images.githubusercontent.com/52180403/217148297-d6b9bf08-8bab-4ff9-89db-151feb8a8f19.png)

# Future
## General
- [X] Migrate to click framework
- [X] Review the view. I'm not quite satisfied with this one.
- [ ] Populate a sqlite db, fetching the .ics files takes too long.
- [ ] Testing, Error handling.
- [ ] Support notifications.
- [ ] Decide how to 'Standarize' the data in the extra info.
- [ ] Support other cinemas

## ElCairo
- [X] Error handling for dates without shows.
- [X] Understand a little more of what I'm retrieving with that .ics file
- [X] Date sorting (The closest to `now` is returned last)
- [X] Crawl the info url to get more information in the API, e.g the duration of the film
