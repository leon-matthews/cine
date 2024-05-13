
from cine import readers


name_basics = readers.NameBasics(
    nconst='nm0000999',
    primary_name='Red Buttons',
    birth_year=1919,
    death_year=2006,
    primary_profession=('actor', 'soundtrack', 'miscellaneous'),
    known_for_titles=('tt0076538', 'tt0069113', 'tt0056197', 'tt0050933'),
)

name_basics_strings = [
    'nm0000999',
    'Red Buttons',
    '1919',
    '2006',
    'actor,soundtrack,miscellaneous',
    'tt0076538,tt0069113,tt0056197,tt0050933',
]

name_basics_strings2 = [
    'nm0000998',
    'Jake Busey',
    '1971',
    '\\N',
    'actor,producer,music_department',
    'tt0120201,tt0116365,tt0120660,tt3829266',
]

title_akas = readers.TitleAkas(
    title_id='tt0000084',
    ordering=1,
    title='The Drunkards',
    region='GB',
    language=None,
    types=('imdbDisplay',),
    attributes=None,
    is_original_title=False,
)

title_akas_strings = [
    'tt0000084', '1', 'The Drunkards', 'GB', '\\N', 'imdbDisplay', '\\N', '0',
]

title_basics = readers.TitleBasics(
    tconst='tt0000831',
    title_type='short',
    primary_title='The Cord of Life',
    original_title='The Cord of Life',
    is_adult=False,
    start_year=1909,
    end_year=None,
    runtime_minutes=9,
    genres=('Crime', 'Drama', 'Short'),
)

title_basics_strings = [
    'tt0000831',
    'short',
    'The Cord of Life',
    'The Cord of Life',
    '0',
    '1909',
    '\\N',
    '9',
    'Crime,Drama,Short',
]

title_crew = readers.TitleCrew(
    tconst='tt0001004',
    directors=('nm0674600',),
    writers=('nm0275421', 'nm0304098'),
)

title_crew_strings = ['tt0001004', 'nm0674600', 'nm0275421,nm0304098']

title_episodes = readers.TitleEpisodes(
    tconst='tt0078459',
    parent='tt0159876',
    season=6,
    episode=5,
)

title_principals = readers.TitlePrincipals(
    tconst='tt0000109',
    ordering=4,
    nconst='nm0005658',
    category='cinematographer',
    job=None,
    characters=None,
)

title_principals_strings = [
    'tt0000546', '1', 'nm0106151', 'actor', '\\N', '["The Rarebit Fiend"]',
]

title_principals_strings2 = [
    'tt0000109', '4', 'nm0005658', 'cinematographer', '\\N', '\\N',
]

title_ratings = readers.TitleRatings(
    tconst='tt0000001',
    average_rating=4.5,
    num_votes=466,
)

title_ratings_strings = ['tt0000001', '4.5', '466']
