from parallel.lemmatizer import Lemmatizer

import time

if __name__ == '__main__':
    start_time = time.time()
    s = Lemmatizer()
    r = s.lemmatize("големата", parallel=True)
    end_time = time.time()
    print(''.join(r))
    print("time = ", end_time - start_time)
