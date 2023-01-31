from etl.defines import GENRES, PERSONS, MOVIES
from models.film import Film
from models.person import Person
from models.genre import Genre

INDEXES_AND_MODELS = {
    GENRES: Genre,
    PERSONS: Person,
    MOVIES: Film
}