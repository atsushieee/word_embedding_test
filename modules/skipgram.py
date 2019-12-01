''' skip-gramを使った単語の出現確率をMatrix化する処理 '''
from builtins import input
import numpy as np
from tqdm import tqdm
from modules.models.DataTransformation import DataTransformation


def get_skipgram_word_probs(sentences, v_size, window_size=4, smooth_alpha=1):
    # use add-smoothing
    word_probs = np.ones((v_size, v_size)) * smooth_alpha
    half_window_size = int(window_size/2)

    pbar = tqdm(total=len(sentences))
    pbar.set_description('words fequency based on skipgram')
    for sentence_txt in sentences:
        pbar.update(1)
        # in the case of len(sentence_txt) == 1, the type of it is judged int
        sentence = str(sentence_txt).split(', ')
        len_words = len(sentence)

        for i in range(len_words):
            start_idx = 0 if i-half_window_size < 0 else i-half_window_size
            end_idx = len_words-1 if i+half_window_size >= len_words else i+half_window_size

            count_words = sentence[start_idx:i]
            count_words.extend(sentence[i+1:end_idx+1])
            for word_idx in count_words:
                # type of number is judged as string
                # index of words table is started from 1 not 0
                word_probs[int(sentence[i])-1, int(word_idx)-1] += 1

    # word_probs /= word_probs.sum(axis=1, keepdims=True)
    pbar.close()
    return word_probs


def skipgram():
    data = DataTransformation()
    sentences = data.get_sentences()
    word2idx = data.get_word2idx()
    idx2word = data.get_idx2word()
    vocab_size = data.get_vocab_size()
    top_no = 50

    word_probs = get_skipgram_word_probs(sentences, vocab_size)

    while True:
        search_word = input('Please enter a word: ')
        if search_word == 'q':
            break
        search_idx = word2idx[search_word]
        similar_words_list = np.flip(np.argsort(word_probs[search_idx-1]))
        for i in range(top_no):
            print(str(i+1) + ': ' + idx2word[similar_words_list[i]+1])

    print('app was closed')
