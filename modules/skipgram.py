''' skip-gramを使った単語の出現確率をMatrix化する処理 '''
from builtins import input
import numpy as np
import time
from tqdm import tqdm
from modules.models.DataTransformation import DataTransformation


def get_skipgram_word_probs(sentences,
                            remapped_id2ids,
                            window_size=4,
                            smooth_alpha=1):
    v_size = len(remapped_id2ids)
    # use add-smoothing
    word_probs = np.ones((v_size, v_size)) * smooth_alpha
    half_window_size = int(window_size/2)

    pbar = tqdm(total=len(sentences))
    pbar.set_description('words fequency based on skipgram')
    for sentence_txt in sentences:
        pbar.update(1)
        # in the case of len(sentence_txt) == 1, the type of it is judged int
        sentence_words = str(sentence_txt).split(', ')
        # for comparison with key of remapped_id2ids dictionary
        sentence_words_int = [int(n) for n in sentence_words]
        len_words = len(sentence_words_int)

        for i, sentence_word in enumerate(sentence_words_int):
            if sentence_word not in remapped_id2ids:
                continue
            start_idx = 0 if i-half_window_size < 0 else i-half_window_size
            end_idx = len_words-1 if i+half_window_size >= len_words else i+half_window_size

            count_words = sentence_words_int[start_idx:i]
            count_words.extend(sentence_words_int[i+1:end_idx+1])

            for count_word in count_words:
                if count_word not in remapped_id2ids:
                    continue
                # type of number is judged as string
                # index of words table is started from 1 not 0
                word_probs[
                    remapped_id2ids[sentence_word], remapped_id2ids[count_word]
                ] += 1

    start_time = time.clock()
    word_probs /= word_probs.sum(axis=1, keepdims=True)
    end_time = time.clock()
    pbar.close()
    print(
        "Probability Calculation Processing Time (in seconds):",
        end_time-start_time
    )
    return word_probs


def skipgram():
    data = DataTransformation()
    sentences = data.get_sentences()
    word2idx = data.get_word2idx()
    idx2word = data.get_idx2word()

    selected_words = data.get_word2idx_limited(20000)
    if selected_words is None:
        return
    # remap word ids to dimention reduction
    remapped_origin2new_ids = {}
    remapped_new2origin_ids = {}
    for idx, selected_word in enumerate(selected_words):
        remapped_origin2new_ids[selected_word[0]] = idx
        remapped_new2origin_ids[idx] = selected_word[0]
    top_no = 50

    word_probs = get_skipgram_word_probs(sentences, remapped_origin2new_ids)
    print(word_probs)

    while True:
        search_word = input('Please enter a word: ')
        if search_word == 'q':
            break
        if search_word not in word2idx:
            print('there is no word in dataset.')
            continue
        search_original_idx = word2idx[search_word]
        if search_original_idx not in remapped_origin2new_ids:
            print('there is no word in dataset.')
            continue
        search_idx = remapped_origin2new_ids[search_original_idx]
        similar_words_list = np.flip(np.argsort(word_probs[search_idx]))
        for i in range(top_no):
            word_original_idx = remapped_new2origin_ids[similar_words_list[i]]
            print(str(i+1) + ': ' + idx2word[word_original_idx])

    print('app was closed')
