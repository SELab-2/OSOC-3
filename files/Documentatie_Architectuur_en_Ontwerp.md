
Dit bestand geeft een beknopte beschrijving van de gebruikte architectuur en het ontwerp van het project.

## Architectuur
Een visuele voorstelling van onze architectuur staat beschreven in het **deployment diagram**.
### Presentation Layer

Om de pagina's te maken die de eindgebruikers te zien zullen krijgen, gebruiken we TypeScript met het React-framework. Deze spreekt de domain layer aan.

### Domain Layer

Om de data aan te bieden aan de presentation layer via een API, maken we gebruik van Python 3.10.2 met het FastAPI framework. 

### Persistence Layer

Om de database aan te spreken, en om de data makkelijk te kunnen gebruiken in de domain layer, maken we gebruik van SQLAlchemy als ORM.

### Database Layer

De onderliggende databasetechologie die we gebruiken om de data effectief op te slaan is MariaDB.

## Ontwerp
De sequence diagrammen van onze applicatie kunnen [hier](https://github.com/SELab-2/OSOC-3/tree/develop/files) teruggevonden worden.
Hierin worden de belangrijkste interacties tussen objecten getoond.