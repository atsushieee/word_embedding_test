''' transform data which is retrieved from DbModel '''
from modules.models.DbModel import DbModel
from config.config import CONFIG


class DataTransformation:
    ''' Class prevents from connecting to DB again and again '''
    def __init__(self):
        self.db_model = DbModel(CONFIG['db_file_name'])
        self.words_info = self.db_model.select_all_records_words_table()

    def get_sentences(self):
        sentences_info = self.db_model.select_all_records_sentences_table()
        return [sentence_info[3] for sentence_info in sentences_info]

    def get_idx2word(self):
        idx2word = {}
        for word_info in self.words_info:
            idx2word[word_info[0]] = word_info[1]
        return idx2word

    def get_word2idx(self):
        word2idx = {}
        for word_info in self.words_info:
            word2idx[word_info[1]] = word_info[0]
        return word2idx

    def get_word2idx_limited(self, vocab_size=5000):
        max_vocab_size = self.get_vocab_size()
        if max_vocab_size < vocab_size:
            print("exceed the vocabrary size of training data")
            return None
        self.words_info = self.db_model.select_all_records_words_table_desc()
        selected_words = self.words_info[:vocab_size]
        return selected_words

    def get_vocab_size(self):
        words_info = self.db_model.select_all_records_words_table()
        return len(words_info)
