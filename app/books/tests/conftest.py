from books.models import Book


book = {
    'title': 'Book Title',
    'author': 'Test Author',
    'published_date': '2020-01-01',
    'ISBN': '1234567890123',
    'pages_count': 123,
    'cover_link': 'http://books.google.pl/books?id=n6-NZGO6PxkC&printsec=frontcover&dq=intitle:Juliet&hl=&cd=4&source=gbs_api',
    'language': 'English'
}


def sample_book() -> Book:
    return Book.objects.create(
        title=book['title'],
        author=book['author'],
        published_date=book['published_date'],
        ISBN=book['ISBN'],
        pages_count=book['pages_count'],
        cover_link=book['cover_link'],
        language=book['language']
    )


def mock_google_api() -> list:
    return [
        {
            "volumeInfo": {
                "title": "The Witcher 3: Wild Hunt - Strategy Guide",
                "authors": [
                    "GamerGuides.com"
                ],
                "publishedDate": "2015-10-20",
                "industryIdentifiers": [
                    {
                        "type": "ISBN_13",
                        "identifier": "9781630417543"
                    },
                    {
                        "type": "ISBN_10",
                        "identifier": "1630417548"
                    }
                ],
                "pageCount": 184,
                "language": "en",
                "previewLink": "http://books.google.pl/books?id=lfHRCgAAQBAJ&printsec=frontcover&dq=intitle:Witcher&hl=&cd=1&source=gbs_api"
            }
    }
]
