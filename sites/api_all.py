# -*- coding: utf-8 -*-

# Always pay attention to the translations in the menu!
# HTML LangzeitCache hinzugefügt
# showGenre:     48 Stunden
# showEntries:    6 Stunden
# showEpisodes:   4 Stunden

import re
from resources.lib.handler.ParameterHandler import ParameterHandler
from resources.lib.handler.requestHandler import cRequestHandler
from resources.lib.tools import logger, cParser
from resources.lib.gui.guiElement import cGuiElement
from resources.lib.config import cConfig
from resources.lib.gui.gui import cGui
from json import loads

# Domain Abfrage ###

SITE_NAME = 'API Suchmaschine'
SITE_ICON = 'api.png'
SITE_IDENTIFIER = 'api_all'

DOMAIN = cConfig().getSetting('plugin_' + SITE_IDENTIFIER + '.domain', 'api.streamkiste.sx')
STATUS = cConfig().getSetting('plugin_' + SITE_IDENTIFIER + '_status') # Status Code Abfrage der Domain
ACTIVE = cConfig().getSetting('plugin_' + SITE_IDENTIFIER) # Ob Plugin aktiviert ist oder nicht
ORIGIN = 'https://' + DOMAIN + '/'
REFERER = ORIGIN + '/'

URL_API = 'https://' + DOMAIN
URL_MAIN = URL_API + '/data/browse/?lang=%s&type=%s&order_by=%s&page=%s'
URL_SEARCH = URL_API + '/data/browse/?lang=%s&keyword=%s&page=%s'
URL_THUMBNAIL = 'https://image.tmdb.org/t/p/w300%s'
URL_WATCH = URL_API + '/data/watch/?_id=%s'

URL_GENRE = URL_API + '/data/browse/?lang=%s&type=%s&order_by=%s&genre=%s&page=%s'
URL_CAST = URL_API + '/data/browse/?lang=%s&type=%s&order_by=%s&cast=%s&page=%s'
URL_YEAR = URL_API + '/data/browse/?lang=%s&type=%s&order_by=%s&year=%s&page=%s'

# Global search function is thus deactivated!
if cConfig().getSetting('global_search_' + SITE_IDENTIFIER) == 'false':
    SITE_GLOBAL_SEARCH = False
    logger.info('-> [SitePlugin]: globalSearch for %s is deactivated.' % SITE_NAME)


def load():
    logger.info('Load %s' % SITE_NAME)
    params = ParameterHandler()
    sLanguage = cConfig().getSetting('prefLanguage')
    # Änderung des Sprachcodes nach voreigestellter Sprache
    if sLanguage == '0':  # prefLang Alle Sprachen
        sLang = 'all'
    if sLanguage == '1':  # prefLang Deutsch
        sLang = '2'
    if sLanguage == '2':  # prefLang Englisch
        sLang = '3'
    elif sLanguage == '3':  # prefLang Japanisch
        sLang = cGui().showLanguage()
        return
    params.setParam('sLanguage', sLang)

    cGui().addFolder(cGuiElement('Filme', SITE_IDENTIFIER, 'showMovieMenu'), params) # Movies
    cGui().addFolder(cGuiElement('Film Genre', SITE_IDENTIFIER, 'showGenreMMenu'), params) # Movies Genre
    cGui().addFolder(cGuiElement('Serien', SITE_IDENTIFIER, 'showSeriesMenu'), params) # Series
    cGui().addFolder(cGuiElement('Serien Genre', SITE_IDENTIFIER, 'showGenreSMenu'), params) # Series Genre
    cGui().addFolder(cGuiElement('Jahre', SITE_IDENTIFIER, 'showYearsMenu'), params) # Years
    cGui().addFolder(cGuiElement('Schauspieler', SITE_IDENTIFIER, 'showCastMenu'), params) # Cast
    cGui().addFolder(cGuiElement('Suche', SITE_IDENTIFIER, 'showSearch')) # Search
    cGui().setEndOfDirectory()


def _cleanTitle(sTitle):
    sTitle = re.sub("[\xE4]", 'ae', sTitle)
    sTitle = re.sub("[\xFC]", 'ue', sTitle)
    sTitle = re.sub("[\xF6]", 'oe', sTitle)
    sTitle = re.sub("[\xC4]", 'Ae', sTitle)
    sTitle = re.sub("[\xDC]", 'Ue', sTitle)
    sTitle = re.sub("[\xD6]", 'Oe', sTitle)
    sTitle = re.sub("[\x00-\x1F\x80-\xFF]", '', sTitle)
    return sTitle


def _getQuality(sQuality):
    isMatch, aResult = cParser.parse(sQuality, '(HDCAM|HD|WEB|BLUERAY|BRRIP|DVD|TS|SD|CAM)', 1, True)
    if isMatch:
        return aResult[0]
    else:
        return sQuality


def showMovieMenu():
    params = ParameterHandler()
    sLanguage = params.getValue('sLanguage')

    params.setParam('sUrl', URL_MAIN % (sLanguage, 'movies', 'Trending', '1')) ### Trending Filme trending1
    cGui().addFolder(cGuiElement('Derzeit Beliebt', SITE_IDENTIFIER, 'showEntries'), params) ### Trending Filme trending1

    params.setParam('sUrl', URL_MAIN % (sLanguage, 'movies', 'new', '1')) ### neue filme neu1
    cGui().addFolder(cGuiElement('Neue Filme', SITE_IDENTIFIER, 'showEntries'), params) ### neue filme neu1

    params.setParam('sUrl', URL_MAIN % (sLanguage, 'movies', 'views', '1')) ### Views filme views1
    cGui().addFolder(cGuiElement('Meist Gesehen', SITE_IDENTIFIER, 'showEntries'), params) ### Views filme views1

    params.setParam('sUrl', URL_MAIN % (sLanguage, 'movies', 'rating', '1')) ### Rating Filme rating1
    cGui().addFolder(cGuiElement('Top IMDb', SITE_IDENTIFIER, 'showEntries'), params) ### Rating Filme rating1

    params.setParam('sUrl', URL_MAIN % (sLanguage, 'movies', 'votes', '1')) ### votes filme votes 1
    cGui().addFolder(cGuiElement('Votes Filme', SITE_IDENTIFIER, 'showEntries'), params) ###

    params.setParam('sUrl', URL_MAIN % (sLanguage, 'movies', 'updates', '1')) ### updates filme updates 1
    cGui().addFolder(cGuiElement('Updates Filme', SITE_IDENTIFIER, 'showEntries'), params) ###

    params.setParam('sUrl', URL_MAIN % (sLanguage, 'movies', 'name', '1')) ### name filme
    cGui().addFolder(cGuiElement('Name Filme', SITE_IDENTIFIER, 'showEntries'), params) ###

    params.setParam('sUrl', URL_MAIN % (sLanguage, 'movies', 'featured', '1')) ### featured filme features1
    cGui().addFolder(cGuiElement('Featured Filme', SITE_IDENTIFIER, 'showEntries'), params) ###

    params.setParam('sUrl', URL_MAIN % (sLanguage, 'movies', 'requested', '1')) ### requested filme
    cGui().addFolder(cGuiElement('Requested Filme', SITE_IDENTIFIER, 'showEntries'), params) ###

    params.setParam('sUrl', URL_MAIN % (sLanguage, 'movies', 'releases', '1')) ### releases filme
    cGui().addFolder(cGuiElement('Releases Filme', SITE_IDENTIFIER, 'showEntries'), params) ### Filme releases 1
    cGui().setEndOfDirectory()

# show movie genre menue
def showGenreMMenu():
    params = ParameterHandler()
    sLanguage = params.getValue('sLanguage')

    cGui().addFolder(cGuiElement('Film Genre Trending', SITE_IDENTIFIER, 'showGenreMTMenu'), params) # Movies Genre Trending
    cGui().addFolder(cGuiElement('Film Genre New', SITE_IDENTIFIER, 'showGenreMNEMenu'), params) # Movies Genre New
    cGui().addFolder(cGuiElement('Film Genre Views', SITE_IDENTIFIER, 'showGenreMVIMenu'), params) # Movies Genre Views
    cGui().addFolder(cGuiElement('Film Genre Votes', SITE_IDENTIFIER, 'showGenreMVMenu'), params) # Movies Genre Votes
    cGui().addFolder(cGuiElement('Film Genre Updates', SITE_IDENTIFIER, 'showGenreMUMenu'), params) # Movies Genre Updates
    cGui().addFolder(cGuiElement('Film Genre Rating', SITE_IDENTIFIER, 'showGenreMRMenu'), params) # Movies Genre Rating
    cGui().addFolder(cGuiElement('Film Genre Name', SITE_IDENTIFIER, 'showGenreMNAMenu'), params) # Movies Genre Name
    cGui().addFolder(cGuiElement('Film Genre Requested', SITE_IDENTIFIER, 'showGenreMREMenu'), params) # Movies Genre Requested
    cGui().addFolder(cGuiElement('Film Genre Featured', SITE_IDENTIFIER, 'showGenreMFEMenu'), params) # Movies Genre Featured
    cGui().addFolder(cGuiElement('Film Genre Releases', SITE_IDENTIFIER, 'showGenreMRAMenu'), params) # Movies Genre Releases
    cGui().setEndOfDirectory()

# Genre Movie Trending Menu
def showGenreMTMenu():
    params = ParameterHandler()
    sLanguage = params.getValue('sLanguage')

    genres = [
        "Action", "Abenteuer", "Animation", "Biographie", "Komödie",
        "Krimi", "Dokumentation", "Drama", "Familie", "Fantasy",
        "Geschichte", "Horror", "Musik", "Mystery", "Romantik",
        "Reality-TV", "Sci-Fi", "Sport", "Thriller", "Krieg", "Western"
    ]

    for genre in genres:
        params.setParam('sUrl', URL_GENRE % (sLanguage, 'movies', 'Trending', genre, '1'))
        cGui().addFolder(cGuiElement(genre, SITE_IDENTIFIER, 'showEntries'), params)

    cGui().setEndOfDirectory()


# Genre Movie Neu Menu
def showGenreMNEMenu():
    params = ParameterHandler()
    sLanguage = params.getValue('sLanguage')

    genres = [
        "Action", "Abenteuer", "Animation", "Biographie", "Komödie",
        "Krimi", "Dokumentation", "Drama", "Familie", "Fantasy",
        "Geschichte", "Horror", "Musik", "Mystery", "Romantik",
        "Reality-TV", "Sci-Fi", "Sport", "Thriller", "Krieg", "Western"
    ]

    for genre in genres:
        params.setParam('sUrl', URL_GENRE % (sLanguage, 'movies', 'Neu', genre, '1'))
        cGui().addFolder(cGuiElement(genre, SITE_IDENTIFIER, 'showEntries'), params)

    cGui().setEndOfDirectory()


# Genre Movie Views Menu
def showGenreMVIMenu():
    params = ParameterHandler()
    sLanguage = params.getValue('sLanguage')

    genres = [
        "Action", "Abenteuer", "Animation", "Biographie", "Komödie",
        "Krimi", "Dokumentation", "Drama", "Familie", "Fantasy",
        "Geschichte", "Horror", "Musik", "Mystery", "Romantik",
        "Reality-TV", "Sci-Fi", "Sport", "Thriller", "Krieg", "Western"
    ]

    for genre in genres:
        params.setParam('sUrl', URL_GENRE % (sLanguage, 'movies', 'Views', genre, '1'))
        cGui().addFolder(cGuiElement(genre, SITE_IDENTIFIER, 'showEntries'), params)

    cGui().setEndOfDirectory()


# Genre Movie Votes Menu
def showGenreMVMenu():
    params = ParameterHandler()
    sLanguage = params.getValue('sLanguage')

    genres = [
        "Action", "Abenteuer", "Animation", "Biographie", "Komödie",
        "Krimi", "Dokumentation", "Drama", "Familie", "Fantasy",
        "Geschichte", "Horror", "Musik", "Mystery", "Romantik",
        "Reality-TV", "Sci-Fi", "Sport", "Thriller", "Krieg", "Western"
    ]

    for genre in genres:
        params.setParam('sUrl', URL_GENRE % (sLanguage, 'movies', 'Votes', genre, '1'))
        cGui().addFolder(cGuiElement(genre, SITE_IDENTIFIER, 'showEntries'), params)

    cGui().setEndOfDirectory()


# Genre Movie Updates Menu
def showGenreMUMenu():
    params = ParameterHandler()
    sLanguage = params.getValue('sLanguage')

    genres = [
        "Action", "Abenteuer", "Animation", "Biographie", "Komödie",
        "Krimi", "Dokumentation", "Drama", "Familie", "Fantasy",
        "Geschichte", "Horror", "Musik", "Mystery", "Romantik",
        "Reality-TV", "Sci-Fi", "Sport", "Thriller", "Krieg", "Western"
    ]

    for genre in genres:
        params.setParam('sUrl', URL_GENRE % (sLanguage, 'movies', 'Updates', genre, '1'))
        cGui().addFolder(cGuiElement(genre, SITE_IDENTIFIER, 'showEntries'), params)

    cGui().setEndOfDirectory()


# Genre Movie Rating Menu
def showGenreMRMenu():
    params = ParameterHandler()
    sLanguage = params.getValue('sLanguage')

    genres = [
        "Action", "Abenteuer", "Animation", "Biographie", "Komödie",
        "Krimi", "Dokumentation", "Drama", "Familie", "Fantasy",
        "Geschichte", "Horror", "Musik", "Mystery", "Romantik",
        "Reality-TV", "Sci-Fi", "Sport", "Thriller", "Krieg", "Western"
    ]

    for genre in genres:
        params.setParam('sUrl', URL_GENRE % (sLanguage, 'movies', 'Rating', genre, '1'))
        cGui().addFolder(cGuiElement(genre, SITE_IDENTIFIER, 'showEntries'), params)

    cGui().setEndOfDirectory()


# Genre Movie Name Menu
def showGenreMNAMenu():
    params = ParameterHandler()
    sLanguage = params.getValue('sLanguage')

    genres = [
        "Action", "Abenteuer", "Animation", "Biographie", "Komödie",
        "Krimi", "Dokumentation", "Drama", "Familie", "Fantasy",
        "Geschichte", "Horror", "Musik", "Mystery", "Romantik",
        "Reality-TV", "Sci-Fi", "Sport", "Thriller", "Krieg", "Western"
    ]

    for genre in genres:
        params.setParam('sUrl', URL_GENRE % (sLanguage, 'movies', 'Name', genre, '1'))
        cGui().addFolder(cGuiElement(genre, SITE_IDENTIFIER, 'showEntries'), params)

    cGui().setEndOfDirectory()


# Genre Movie Requested Menu
def showGenreMREMenu():
    params = ParameterHandler()
    sLanguage = params.getValue('sLanguage')

    genres = [
        "Action", "Abenteuer", "Animation", "Biographie", "Komödie",
        "Krimi", "Dokumentation", "Drama", "Familie", "Fantasy",
        "Geschichte", "Horror", "Musik", "Mystery", "Romantik",
        "Reality-TV", "Sci-Fi", "Sport", "Thriller", "Krieg", "Western"
    ]

    for genre in genres:
        params.setParam('sUrl', URL_GENRE % (sLanguage, 'movies', 'requested', genre, '1'))
        cGui().addFolder(cGuiElement(genre, SITE_IDENTIFIER, 'showEntries'), params)

    cGui().setEndOfDirectory()


# Genre Movie Featured Menu
def showGenreMFEMenu():
    params = ParameterHandler()
    sLanguage = params.getValue('sLanguage')

    genres = [
        "Action", "Abenteuer", "Animation", "Biographie", "Komödie",
        "Krimi", "Dokumentation", "Drama", "Familie", "Fantasy",
        "Geschichte", "Horror", "Musik", "Mystery", "Romantik",
        "Reality-TV", "Sci-Fi", "Sport", "Thriller", "Krieg", "Western"
    ]

    for genre in genres:
        params.setParam('sUrl', URL_GENRE % (sLanguage, 'movies', 'featured', genre, '1'))
        cGui().addFolder(cGuiElement(genre, SITE_IDENTIFIER, 'showEntries'), params)

    cGui().setEndOfDirectory()


# Genre Movie Releases Menu
def showGenreMRAMenu():
    params = ParameterHandler()
    sLanguage = params.getValue('sLanguage')

    genres = [
        "Action", "Abenteuer", "Animation", "Biographie", "Komödie",
        "Krimi", "Dokumentation", "Drama", "Familie", "Fantasy",
        "Geschichte", "Horror", "Musik", "Mystery", "Romantik",
        "Reality-TV", "Sci-Fi", "Sport", "Thriller", "Krieg", "Western"
    ]

    for genre in genres:
        params.setParam('sUrl', URL_GENRE % (sLanguage, 'movies', 'releases', genre, '1'))
        cGui().addFolder(cGuiElement(genre, SITE_IDENTIFIER, 'showEntries'), params)

    cGui().setEndOfDirectory()


# Serienmenue
def showSeriesMenu():
    params = ParameterHandler()
    sLanguage = params.getValue('sLanguage')

    params.setParam('sUrl', URL_MAIN % (sLanguage, 'tvseries', 'neu', '1')) ### serien neu 1
    cGui().addFolder(cGuiElement('Neue Serien', SITE_IDENTIFIER, 'showEntries'), params) ###

    params.setParam('sUrl', URL_MAIN % (sLanguage, 'tvseries', 'views', '1')) ### serien views 1
    cGui().addFolder(cGuiElement('Views Serien', SITE_IDENTIFIER, 'showEntries'), params) ###

    params.setParam('sUrl', URL_MAIN % (sLanguage, 'tvseries', 'votes', '1')) ### serien votes 1
    cGui().addFolder(cGuiElement('Votes Serien', SITE_IDENTIFIER, 'showEntries'), params) ###

    params.setParam('sUrl', URL_MAIN % (sLanguage, 'tvseries', 'updates', '1')) ### serien updates 1
    cGui().addFolder(cGuiElement('Updates Serien', SITE_IDENTIFIER, 'showEntries'), params) ###

    params.setParam('sUrl', URL_MAIN % (sLanguage, 'tvseries', 'name', '1')) ### serien name 1
    cGui().addFolder(cGuiElement('Name Serien', SITE_IDENTIFIER, 'showEntries'), params) ###

    params.setParam('sUrl', URL_MAIN % (sLanguage, 'tvseries', 'featured', '1')) ###
    cGui().addFolder(cGuiElement('Featured Serien', SITE_IDENTIFIER, 'showEntries'), params) ###

    params.setParam('sUrl', URL_MAIN % (sLanguage, 'tvseries', 'requested', '1')) ### serien requested
    cGui().addFolder(cGuiElement('Requested Serien', SITE_IDENTIFIER, 'showEntries'), params) ###

    params.setParam('sUrl', URL_MAIN % (sLanguage, 'tvseries', 'releases', '1')) ### serien releases 1
    cGui().addFolder(cGuiElement('Releases Serien', SITE_IDENTIFIER, 'showEntries'), params) ###

    params.setParam('sUrl', URL_MAIN % (sLanguage, 'tvseries', 'rating', '1')) ### serien rating 1
    cGui().addFolder(cGuiElement('Rating Serien', SITE_IDENTIFIER, 'showEntries'), params) ###

    #params.setParam('sUrl', URL_MAIN % (sLanguage, 'tvseries', 'Jahr', '1'))  # ##
    #cGui().addFolder(cGuiElement('Jahr', SITE_IDENTIFIER, 'showEntries'), params) ##

    #params.setParam('sCont', 'Jahr') #
    #cGui().addFolder(cGuiElement('Jahr', SITE_IDENTIFIER, 'showValue'), params) #
    cGui().setEndOfDirectory()


# show genre serien menue
def showGenreSMenu():
    params = ParameterHandler()
    sLanguage = params.getValue('sLanguage')

    cGui().addFolder(cGuiElement('Serien Genre Trending', SITE_IDENTIFIER, 'showGenreSTMenu'), params) # Movies Genre Trending
    cGui().addFolder(cGuiElement('Serien Genre New', SITE_IDENTIFIER, 'showGenreSNEMenu'), params) # Movies Genre New
    cGui().addFolder(cGuiElement('Serien Genre Views', SITE_IDENTIFIER, 'showGenreSVIMenu'), params) # Movies Genre Views
    cGui().addFolder(cGuiElement('Serien Genre Votes', SITE_IDENTIFIER, 'showGenreSVMenu'), params) # Movies Genre Votes
    cGui().addFolder(cGuiElement('Serien Genre Updates', SITE_IDENTIFIER, 'showGenreSUMenu'), params) # Movies Genre Updates
    cGui().addFolder(cGuiElement('Serien Genre Rating', SITE_IDENTIFIER, 'showGenreSRMenu'), params) # Movies Genre Rating
    cGui().addFolder(cGuiElement('Serien Genre Name', SITE_IDENTIFIER, 'showGenreSNAMenu'), params) # Movies Genre Name
    cGui().addFolder(cGuiElement('Serien Genre Requested', SITE_IDENTIFIER, 'showGenreSREMenu'), params) # Movies Genre Requested
    cGui().addFolder(cGuiElement('Serien Genre Featured', SITE_IDENTIFIER, 'showGenreSFEMenu'), params) # Movies Genre Featured
    cGui().addFolder(cGuiElement('Serien Genre Releases', SITE_IDENTIFIER, 'showGenreSRAMenu'), params) # Movies Genre Releases

    cGui().setEndOfDirectory()


# Genre Series Trending Menu
def showGenreSTMenu():
    params = ParameterHandler()
    sLanguage = params.getValue('sLanguage')

    genres = [
        "Action", "Abenteuer", "Animation", "Biographie", "Komödie",
        "Krimi", "Dokumentation", "Drama", "Familie", "Fantasy",
        "Geschichte", "Horror", "Musik", "Mystery", "Romantik",
        "Reality-TV", "Sci-Fi", "Sport", "Thriller", "Krieg", "Western"
    ]

    for genre in genres:
        params.setParam('sUrl', URL_GENRE % (sLanguage, 'tvseries', 'Trending', genre, '1'))
        cGui().addFolder(cGuiElement(genre, SITE_IDENTIFIER, 'showEntries'), params)

    cGui().setEndOfDirectory()


# Genre Series Neu Menu
def showGenreSNEMenu():
    params = ParameterHandler()
    sLanguage = params.getValue('sLanguage')

    genres = [
        "Action", "Abenteuer", "Animation", "Biographie", "Komödie",
        "Krimi", "Dokumentation", "Drama", "Familie", "Fantasy",
        "Geschichte", "Horror", "Musik", "Mystery", "Romantik",
        "Reality-TV", "Sci-Fi", "Sport", "Thriller", "Krieg", "Western"
    ]

    for genre in genres:
        params.setParam('sUrl', URL_GENRE % (sLanguage, 'tvseries', 'Neu', genre, '1'))
        cGui().addFolder(cGuiElement(genre, SITE_IDENTIFIER, 'showEntries'), params)

    cGui().setEndOfDirectory()


# Genre Series Views Menu
def showGenreSVIMenu():
    params = ParameterHandler()
    sLanguage = params.getValue('sLanguage')

    genres = [
        "Action", "Abenteuer", "Animation", "Biographie", "Komödie",
        "Krimi", "Dokumentation", "Drama", "Familie", "Fantasy",
        "Geschichte", "Horror", "Musik", "Mystery", "Romantik",
        "Reality-TV", "Sci-Fi", "Sport", "Thriller", "Krieg", "Western"
    ]

    for genre in genres:
        params.setParam('sUrl', URL_GENRE % (sLanguage, 'tvseries', 'Views', genre, '1'))
        cGui().addFolder(cGuiElement(genre, SITE_IDENTIFIER, 'showEntries'), params)

    cGui().setEndOfDirectory()


# Genre Series Votes Menu ###
def showGenreSVMenu():
    params = ParameterHandler()
    sLanguage = params.getValue('sLanguage')

    genres = [
        "Action", "Abenteuer", "Animation", "Biographie", "Komödie",
        "Krimi", "Dokumentation", "Drama", "Familie", "Fantasy",
        "Geschichte", "Horror", "Musik", "Mystery", "Romantik",
        "Reality-TV", "Sci-Fi", "Sport", "Thriller", "Krieg", "Western"
    ]

    for genre in genres:
        params.setParam('sUrl', URL_GENRE % (sLanguage, 'tvseries', 'Votes', genre, '1'))
        cGui().addFolder(cGuiElement(genre, SITE_IDENTIFIER, 'showEntries'), params)

    cGui().setEndOfDirectory()


# Genre Series Updates Menu
def showGenreSUMenu():
    params = ParameterHandler()
    sLanguage = params.getValue('sLanguage')

    genres = [
        "Action", "Abenteuer", "Animation", "Biographie", "Komödie",
        "Krimi", "Dokumentation", "Drama", "Familie", "Fantasy",
        "Geschichte", "Horror", "Musik", "Mystery", "Romantik",
        "Reality-TV", "Sci-Fi", "Sport", "Thriller", "Krieg", "Western"
    ]

    for genre in genres:
        params.setParam('sUrl', URL_GENRE % (sLanguage, 'tvseries', 'Updates', genre, '1'))
        cGui().addFolder(cGuiElement(genre, SITE_IDENTIFIER, 'showEntries'), params)

    cGui().setEndOfDirectory()


# Genre Series Rating Menu
def showGenreSRMenu():
    params = ParameterHandler()
    sLanguage = params.getValue('sLanguage')

    genres = [
        "Action", "Abenteuer", "Animation", "Biographie", "Komödie",
        "Krimi", "Dokumentation", "Drama", "Familie", "Fantasy",
        "Geschichte", "Horror", "Musik", "Mystery", "Romantik",
        "Reality-TV", "Sci-Fi", "Sport", "Thriller", "Krieg", "Western"
    ]

    for genre in genres:
        params.setParam('sUrl', URL_GENRE % (sLanguage, 'tvseries', 'Rating', genre, '1'))
        cGui().addFolder(cGuiElement(genre, SITE_IDENTIFIER, 'showEntries'), params)

    cGui().setEndOfDirectory()


# Genre Series Name Menu
def showGenreSNAMenu():
    params = ParameterHandler()
    sLanguage = params.getValue('sLanguage')

    genres = [
        "Action", "Abenteuer", "Animation", "Biographie", "Komödie",
        "Krimi", "Dokumentation", "Drama", "Familie", "Fantasy",
        "Geschichte", "Horror", "Musik", "Mystery", "Romantik",
        "Reality-TV", "Sci-Fi", "Sport", "Thriller", "Krieg", "Western"
    ]

    for genre in genres:
        params.setParam('sUrl', URL_GENRE % (sLanguage, 'tvseries', 'Name', genre, '1'))
        cGui().addFolder(cGuiElement(genre, SITE_IDENTIFIER, 'showEntries'), params)

    cGui().setEndOfDirectory()


# Genre Series Requested Menu
def showGenreSREMenu():
    params = ParameterHandler()
    sLanguage = params.getValue('sLanguage')

    genres = [
        "Action", "Abenteuer", "Animation", "Biographie", "Komödie",
        "Krimi", "Dokumentation", "Drama", "Familie", "Fantasy",
        "Geschichte", "Horror", "Musik", "Mystery", "Romantik",
        "Reality-TV", "Sci-Fi", "Sport", "Thriller", "Krieg", "Western"
    ]

    for genre in genres:
        params.setParam('sUrl', URL_GENRE % (sLanguage, 'tvseries', 'requested', genre, '1'))
        cGui().addFolder(cGuiElement(genre, SITE_IDENTIFIER, 'showEntries'), params)

    cGui().setEndOfDirectory()


# Genre Series Featured Menu
def showGenreSFEMenu():
    params = ParameterHandler()
    sLanguage = params.getValue('sLanguage')

    genres = [
        "Action", "Abenteuer", "Animation", "Biographie", "Komödie",
        "Krimi", "Dokumentation", "Drama", "Familie", "Fantasy",
        "Geschichte", "Horror", "Musik", "Mystery", "Romantik",
        "Reality-TV", "Sci-Fi", "Sport", "Thriller", "Krieg", "Western"
    ]

    for genre in genres:
        params.setParam('sUrl', URL_GENRE % (sLanguage, 'tvseries', 'featured', genre, '1'))
        cGui().addFolder(cGuiElement(genre, SITE_IDENTIFIER, 'showEntries'), params)

    cGui().setEndOfDirectory()


# Genre Series Releases Menu
def showGenreSRAMenu():
    params = ParameterHandler()
    sLanguage = params.getValue('sLanguage')

    genres = [
        "Action", "Abenteuer", "Animation", "Biographie", "Komödie",
        "Krimi", "Dokumentation", "Drama", "Familie", "Fantasy",
        "Geschichte", "Horror", "Musik", "Mystery", "Romantik",
        "Reality-TV", "Sci-Fi", "Sport", "Thriller", "Krieg", "Western"
    ]

    for genre in genres:
        params.setParam('sUrl', URL_GENRE % (sLanguage, 'tvseries', 'releases', genre, '1'))
        cGui().addFolder(cGuiElement(genre, SITE_IDENTIFIER, 'showEntries'), params)

    cGui().setEndOfDirectory()


def showYearsMenu():
    params = ParameterHandler()
    sLanguage = params.getValue('sLanguage')

    # Anfangs- und Endjahr für das menü eintragen
    start_jahr = 1931
    end_jahr = 2025

    for jahr in range(start_jahr, end_jahr + 1):
        params.setParam('sUrl', URL_YEAR % (sLanguage, 'movies', 'views', str(jahr), '1'))
        cGui().addFolder(cGuiElement(str(jahr), SITE_IDENTIFIER, 'showEntries'), params)

    cGui().setEndOfDirectory()


def showCastMenu():
    params = ParameterHandler()
    sLanguage = params.getValue('sLanguage')

    def addActor(name, name_url, mode='views'):
        encoded_name = cParser.quotePlus(name_url)
        params.setParam('sUrl', URL_CAST % (sLanguage, 'movies', mode, encoded_name, '1'))
        re.sub(name, '%20', ' ')
        cGui().addFolder(cGuiElement(name, SITE_IDENTIFIER, 'showEntries'), params)

    addActor('Leo Fitzpatrick', 'Leo%20Fitzpatrick')
    addActor('Ice-T', 'Ice-T')
    addActor('Vincent Cassel', 'Vincent%20Cassel')
    addActor('Jonathan Velasquez', 'Jonathan%20Velasquez')
    addActor('AlPacino', 'Al%20Pacino')
    addActor('Sean Penn', 'Sean%20Penn')
    addActor('Jason Statham', 'Jason%20Statham')
    addActor('Ryan Reynolds', 'Ryan%20Reynolds')
    addActor('Tom Hardy', 'Tom%20Hardy')
    addActor('Nicolas Cage','Nicolas%20Cage')
    addActor('Liam Neeson', 'Liam%20Neeson')
    addActor('Morgan Freeman', 'Morgan%20Freeman')
    addActor('Josh Hartnett', 'Josh%20Hartnett')
    addActor('Kevin Hart', 'Kevin%20Hart')
    addActor('Jack Nicholson', 'Jack%20Nicholson')
    addActor('Clint Eastwood', 'Clint%20Eastwood')
    addActor('Stacy Peralta', 'Stacy%20Peralta', mode='releases')
    addActor('EmileHirsch', 'Emile%20Hirsch')

    cGui().setEndOfDirectory()


def showEntries(entryUrl=False, sGui=False, sSearchText=False):
    oGui = sGui if sGui else cGui()
    params = ParameterHandler()
    isTvshow = False
    sThumbnail = ''
    sLanguage = params.getValue('sLanguage')
    if not entryUrl: entryUrl = params.getValue('sUrl')
    try:
        oRequest = cRequestHandler(entryUrl)
        if cConfig().getSetting('global_search_' + SITE_IDENTIFIER) == 'true':
            oRequest.cacheTime = 60 * 60 * 6  # HTML Cache Zeit 6 Stunden
        oRequest.addHeaderEntry('Referer', REFERER)
        oRequest.addHeaderEntry('Origin', ORIGIN)
        sJson = oRequest.request()
        aJson = loads(sJson)
    except:
        if not sGui: oGui.showInfo()
        return
    if 'movies' not in aJson or len(aJson['movies']) == 0: ### LEN funktioniert noch nicht richtig anhand der api.
        #if not sGui: oGui.showInfo()
        #    return
        cGui().showInfo()
        return

    total = 0
    # ignore movies which does not contain any streams
    for movie in aJson['movies']:
        if '_id' in movie:
            total += 1
    for movie in aJson['movies']:
        sTitle = movie['title']
        if sSearchText and not cParser().search(sSearchText, sTitle):
            continue
        if 'Staffel' in sTitle:
            isTvshow = True
        oGuiElement = cGuiElement(sTitle, SITE_IDENTIFIER, 'showEpisodes' if isTvshow else 'showHosters')
        if 'poster_path_season' in movie:
            sThumbnail = URL_THUMBNAIL % movie['poster_path_season']
        elif 'poster_path' in movie:
            sThumbnail = URL_THUMBNAIL % movie['poster_path']
        elif 'backdrop_path' in movie:
            sThumbnail = URL_THUMBNAIL % movie['backdrop_path']
        oGuiElement.setThumbnail(sThumbnail)
        if 'storyline' in movie:
            oGuiElement.setDescription(movie['storyline'])
        elif 'overview' in movie:
            oGuiElement.setDescription(movie['overview'])
        if 'year' in movie:
            oGuiElement.setYear(movie['year'])
        if 'quality' in movie:
            oGuiElement.setQuality(_getQuality(movie['quality']))
        if 'rating' in movie:
            oGuiElement.addItemValue('rating', movie['rating'])
        if 'lang' in movie:
            if (sLanguage != '1' and movie['lang'] == 2):  # Deutsch
                oGuiElement.setLanguage('DE')
            if (sLanguage != '2' and movie['lang'] == 3):  # Englisch
                oGuiElement.setLanguage('EN')
        oGuiElement.setMediaType('tvshows' if isTvshow else 'movie')
        if 'runtime' in movie:
            isMatch, sRuntime = cParser.parseSingleResult(movie['runtime'], '\d+')
            if isMatch:
                oGuiElement.addItemValue('duration', sRuntime)
        params.setParam('entryUrl', URL_WATCH % movie['_id'])
        params.setParam('sName', sTitle)
        params.setParam('sThumbnail', sThumbnail)
        oGui.addFolder(oGuiElement, params, isTvshow, total)

    if not sGui and not sSearchText:
        curPage = aJson['pager']['currentPage']
        if curPage < aJson['pager']['totalPages']:
            sNextUrl = entryUrl.replace('page=' + str(curPage), 'page=' + str(curPage + 1))
            params.setParam('sUrl', sNextUrl)
            oGui.addNextPage(SITE_IDENTIFIER, 'showEntries', params)
        oGui.setView('tvshows' if isTvshow else 'movies')
        oGui.setEndOfDirectory()



def showEpisodes():
    aEpisodes = []
    params = ParameterHandler()
    sUrl = params.getValue('entryUrl')
    sThumbnail = params.getValue("sThumbnail")
    try:
        oRequest = cRequestHandler(sUrl)
        if cConfig().getSetting('global_search_' + SITE_IDENTIFIER) == 'true':
            oRequest.cacheTime = 60 * 60 * 4  # HTML Cache Zeit 4 Stunden
        oRequest.addHeaderEntry('Referer', REFERER)
        oRequest.addHeaderEntry('Origin', ORIGIN)
        sJson = oRequest.request()
        aJson = loads(sJson)
    except:
        cGui().showInfo()
        return

    if 'streams' not in aJson or len(aJson['streams']) == 0:
        cGui().showInfo()
        return

    for stream in aJson['streams']:
        if 'e' in stream:
            aEpisodes.append(int(stream['e']))
    if aEpisodes:
        aEpisodesSorted = set(aEpisodes)
        total = len(aEpisodesSorted)
        for sEpisode in aEpisodesSorted:
            oGuiElement = cGuiElement('Episode ' + str(sEpisode), SITE_IDENTIFIER, 'showHosters')
            oGuiElement.setThumbnail(sThumbnail)
            if 's' in aJson:
                oGuiElement.setSeason(aJson['s'])
            oGuiElement.setTVShowTitle('Episode ' + str(sEpisode))
            oGuiElement.setEpisode(sEpisode)
            oGuiElement.setMediaType('episode')
            cGui().addFolder(oGuiElement, params, False, total)
    cGui().setView('episodes')
    cGui().setEndOfDirectory()


def showHosters():
    hosters = []
    params = ParameterHandler()
    sUrl = params.getValue('entryUrl')
    sEpisode = params.getValue('episode')
    try:
        oRequest = cRequestHandler(sUrl)
        oRequest.addHeaderEntry('Referer', REFERER)
        oRequest.addHeaderEntry('Origin', ORIGIN)
        sJson = oRequest.request()
    except:
        return hosters
    if sJson:
        aJson = loads(sJson)
        if 'streams' in aJson:
            i = 0
            for stream in aJson['streams']:
                if (('e' not in stream) or (str(sEpisode) == str(stream['e']))):
                    sHoster = str(i) + ':'
                    isMatch, aName = cParser.parse(stream['stream'], '//([^/]+)/')
                    if isMatch:
#                        sName = cParser.urlparse(sUrl) ### angezeigter hostername api
                        
                        sName = aName[0][:aName[0].rindex('.')] ### angezeigte hosternamen, jedoch "substring" nicht ausreichend für den film "DUNE teil2"..
                        if cConfig().isBlockedHoster(sName)[0]: continue  # Hoster aus settings.xml oder deaktivierten Resolver ausschließen
                        sHoster = sHoster + ' ' + sName
                    if 'release' in stream:
                        sHoster = sHoster + ' [I][' + _getQuality(stream['release']) + '][/I]'
                    hoster = {'link': stream['stream'], 'name': sHoster}
                    hosters.append(hoster)
                    i += 1
    if hosters:
        hosters.append('getHosterUrl')
    return hosters


def getHosterUrl(sUrl=False):
    return [{'streamUrl': sUrl, 'resolved': False}]


def showSearch():
    oGui = cGui()
    sSearchText = oGui.showKeyBoard()
    if not sSearchText: return
    _search(False, sSearchText)
    oGui.setEndOfDirectory()


def _search(oGui, sSearchText):
    params = ParameterHandler()
    sLanguage = cConfig().getSetting('prefLanguage')
    if sLanguage == '0':  # prefLang Alle Sprachen
        sLang = 'all'
    if sLanguage == '1':  # prefLang Deutsch
        sLang = '2'
    if sLanguage == '2':  # prefLang Englisch
        sLang = '3'
    showEntries(URL_SEARCH % (sLang, cParser().quotePlus(sSearchText), '1'), oGui, sSearchText)
