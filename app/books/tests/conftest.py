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

def sample_book():
    return Book.objects.create(
        title=book['title'],
        author=book['author'],
        published_date=book['published_date'],
        ISBN=book['ISBN'],
        pages_count=book['pages_count'],
        cover_link=book['cover_link'],
        language=book['language']
    )
