import setuptools

setuptools.setup(
    name="qrookDB",
    version="1.2.0.1",
    author="Kurush",
    author_email="ze17@ya.ru",
    description="tiny ORM for SQL-databases",
    long_description_content_type="text/markdown",
    url="https://gitlab.com/qrook/db",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    long_description='''
# Usage example:
```python
    import DB as db
from data import QRTable
books, books_authors, authors, events = [QRTable()] * 4

DB = db.DB('postgres', 'db_name', 'user_name', 'password', format_type='dict')
op = DB.operators
DB.create_logger(app_name='app', file='app_log.log')
DB.create_data(__name__, in_module=True)

print(DB.books)
print(books, books.id)
data = DB.select(books).where(original_publication_year=2000, language_code='eng').\
    where(id=op.In(470, 490, 485)).all()
print(data[:10])

data = books.select('count(*)').group_by(books.original_publication_year).all()
print(data[:10])

data = DB.select(books, books.id).where('id < 10').order_by(books.id, desc=True).\
    limit(3).offset(2).all()
print('limit & offset', data)

data = books.select(authors.id, books.id)\
    .join(books_authors, op.Eq(books_authors.book_id, books.id))\
    .join(authors, op.Eq(books_authors.author_id, authors.id)).all()
    # .join(books_authors, 'books_authors.book_id = books.id')\
print(data[:10])

data = books.select(books.id).where(id=1).where(bool='or', id=2).limit(10).all()
print('with or:', data)

ok = DB.delete(events, auto_commit=True).where(id=1).exec()
print(ok)

from datetime import datetime
t = datetime.now().time()
d = datetime.now().date()
ok = DB.update(events, auto_commit=True).set(time=t).where(id=6).exec()
print(ok)

#ok = DB.insert(events, events.time, auto_commit=True).values([t]).exec()
#ok = DB.insert(events, events.date, events.time, auto_commit=True).values([d, t]).exec()
query = events.insert(events.date, events.time, auto_commit=True).values([[d, t], [None, t]]).returning('*')
data = query.all()
print(data)

query = events.insert(events.date, events.time, auto_commit=True).values([[d, t], [None, t]]).returning(events.date, events.time)
data = query.all()
print(data)

query = events.insert(events.date, events.time, auto_commit=True).values([[d, t], [None, t]]).returning(['date', 'time'])
data = query.all()
print(data)

query = events.insert(events.date, events.time, auto_commit=True).values([[d, t], [None, t]]).returning('date', 'time')
data = query.all()
print(data)

data = DB.exec('select * from get_book_authors(1) as f(id int, name varchar)').config_fields('id', 'name').all()
print(data)

q = DB.select(events, events.id, events.id).where(id=1)
data = q.all()
print('data:', data, ';\terror:', q.get_error())
```
'''
)
