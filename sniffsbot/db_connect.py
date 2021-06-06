import sqlite3


class Database:
    def __init__(self, **kwargs):
        self.filename = kwargs.get('filename')
        self.table = kwargs.get('table')
        self.sql_do('CREATE TABLE IF NOT EXISTS {} (id INTEGER PRIMARY KEY, username TEXT, coin INTEGER)'.format(self._table))

    def sql_do(self, sql, *params):
        self._db.execute(sql, params)
        self._db.commit()
    
    def check_exist(self, key):
        if self._db.execute('SELECT 1 FROM {} WHERE username = ?'.format(self._table), (key,)).fetchone():
            return True
        else:
            return False

    def insert(self, row):
        self._db.execute('INSERT INTO {} (username, coin) VALUES (?, ?)'.format(self._table), (row['username'], row['coin']))
        self._db.commit()

    def retrieve(self, key):
        cursor = self._db.execute('SELECT * FROM {} WHERE username = ?'.format(self._table), (key,))
        return dict(cursor.fetchone())

    def update(self, row):
        self._db.execute(
            'UPDATE {} SET coin = ? WHERE username = ?'.format(self._table),
            (row['coin'], row['username'])
        )
        self._db.commit()

    def delete(self, key):
        self._db.execute('DELETE FROM {} WHERE username = ?'.format(self._table), (key,))
        self._db.commit()

    def __iter__(self):
        cursor = self._db.execute('SELECT * FROM {} ORDER by username'.format(self._table))
        for row in cursor:
            yield dict(row)

    @property
    def filename(self): return self._filename
    @filename.setter
    def filename(self, fn):
        self._filename = fn
        self._db = sqlite3.connect(fn)
        self._db.row_factory = sqlite3.Row
    @filename.deleter
    def filename(self): self.close()
    @property
    def table(self): return self._table
    @table.setter
    def table(self, t): self._table = t
    @table.deleter
    def table(self): self._table = 'players'

    def close(self):
        self._db.close()
        del self._filename
