import os
import sqlite3

DB_ABSOLUTE_PATH = os.path.abspath(os.path.dirname(__file__))


class DbModel:
    ''' Sqliteの処理を行うclass '''
    def __init__(self, db_file, is_initial=False):
        self.db_file = DB_ABSOLUTE_PATH + '/' + db_file

        if os.path.isfile(self.db_file) and is_initial:
            os.remove(self.db_file)
        self._init_process()
        if is_initial:
            self._create_table()

    def _init_process(self):
        self.conn = sqlite3.connect(self.db_file)
        self.cur = self.conn.cursor()

    def _create_table(self):
        self.cur.execute('''CREATE TABLE words (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            word STRING,
            frequency INTEGER
        )''')
        self.cur.execute('''CREATE TABLE sentences (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_name STRING,
            word_sentence STRING,
            index_sentence STRING
        )''')
        return self.conn, self.cur

    def select_all_records_words_table(self):
        select_word_sql = 'SELECT * FROM words'
        self.cur.execute(select_word_sql)
        return self.cur.fetchall()

    def select_all_records_words_table_desc(self):
        select_word_sql = 'SELECT * FROM words ORDER BY frequency DESC'
        self.cur.execute(select_word_sql)
        return self.cur.fetchall()

    def select_all_records_sentences_table(self):
        select_word_sql = 'SELECT * FROM sentences'
        self.cur.execute(select_word_sql)
        return self.cur.fetchall()

    def insert_records_words_table(self, words_frequency):
        insert_word_sql = 'INSERT INTO words (word, frequency) values (?,?)'
        inserted_info = []
        for word, frequency in dict(words_frequency).items():
            inserted_info.append((word, frequency))
        self.cur.executemany(insert_word_sql, inserted_info)

    def insert_records_sentences_table(self, inserted_info):
        insert_sentence_sql = '''
            INSERT INTO sentences (
                file_name, word_sentence, index_sentence
            ) values (?,?,?)
        '''
        self.cur.executemany(insert_sentence_sql, inserted_info)

    def close_connection(self):
        self.conn.commit()
        self.conn.close()
