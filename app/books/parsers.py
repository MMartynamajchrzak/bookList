from .validators import validate_date


def _parse_book(_api) -> dict:
    api_base = _api['volumeInfo']

    author = ''
    authors = api_base.get('authors')
    if authors:
        if len(authors) > 0:
            author = authors[0]

    identifier = None
    ii = api_base.get('industryIdentifiers')
    if ii:
        if len(ii) >= 2 and ii[1].get('identifier').isdigit():
            identifier = ii[1].get('identifier')

    return {
        'title': api_base.get('title') or 'No data',
        'author': author or 'No data',
        'published_date': validate_date(api_base.get('publishedDate', '')),
        'ISBN': identifier,
        'pages_count': api_base.get('pageCount'),
        'cover_link': api_base.get('previewLink'),
        'language': api_base.get('language') or 'No data'
    }
