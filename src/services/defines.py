from src.core.config import settings
from src.models.film import Film
from src.models.person import Person
from src.models.genre import Genre

INDEXES_AND_MODELS = {
    settings.GENRES_INDEX: Genre,
    settings.PERSONS_INDEX: Person,
    settings.MOVIES_INDEX: Film
}