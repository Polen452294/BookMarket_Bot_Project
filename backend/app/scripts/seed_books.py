from app.models.book import Book

def seed_books(db, category_ids: dict[str, int]):
    books = [
        {
            "title": "Grokking Algorithms",
            "author": "Aditya Bhargava",
            "description": "Понятное введение в алгоритмы с примерами и иллюстрациями.",
            "price": 1348,
            "old_price": 1799,
            "year": 2016,
            "pages": 288,
            "publisher": "Manning Publications",
            "language": "English",
            "rating": 4.7,
            "reviews_count": 1250,
            "cover_url": "https://covers.openlibrary.org/b/id/10521270-L.jpg",
            "category": "Программирование",
        }
    ]

    for b in books:
        exists = db.query(Book).filter(
            Book.title == b["title"],
            Book.author == b["author"]
        ).first()

        if exists:
            continue

        book = Book(
            title=b["title"],
            author=b["author"],
            description=b["description"],
            price=b["price"],
            old_price=b["old_price"],
            year=b["year"],
            pages=b["pages"],
            publisher=b["publisher"],
            language=b["language"],
            rating=b["rating"],
            reviews_count=b["reviews_count"],
            cover_url=b["cover_url"],
            category_id=category_ids[b["category"]],
            is_active=True,
        )

        db.add(book)

    db.commit()