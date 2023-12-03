import multiprocessing as mp
import time

import nltk

nltk.download('gutenberg')
nltk.download('averaged_perceptron_tagger')

corpus = {f_id: nltk.corpus.gutenberg.raw(f_id)
          for f_id in nltk.corpus.gutenberg.fileids()}


# За секој од документите се активира функцијата за токенизација:
def tokenize_and_pos_tag(pair):
    f_id, doc = pair
    return f_id, nltk.pos_tag(nltk.word_tokenize(doc))


# Потоа се импортира мултипроцесирањето
if __name__ == '__main__':
    # automatically uses mp.cpu_count() as number of workers
    # mp.cpu_count()  is 4 -> use 4 jobs
    start_time = time.time()
    with mp.Pool() as pool:
        tokens = pool.map(tokenize_and_pos_tag, corpus.items())
    end_time = time.time()
    print(end_time - start_time)

# %%
