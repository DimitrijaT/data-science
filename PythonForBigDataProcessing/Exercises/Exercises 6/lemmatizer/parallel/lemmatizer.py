from collections import defaultdict


from utils.tags import MORPHOLOGICAL_SUBSTITUTIONS_PRE, MORPHOLOGICAL_SUBSTITUTIONS_SUFF, POS_TAG_LIST

from multiprocessing.pool import Pool
words = {}


class Lemmatizer:

    def __init__(self) -> None:
        self._exception_map = {}
        self._loaded_words = {}
        self._pos_list = POS_TAG_LIST

    def load_words(self, pos):
        with open('wfl-mk.tbl') as file:
            for f in file:
                try:
                    w, l, at = f.split('\t')
                    if at.startswith(pos.upper()):
                        self._loaded_words[w] = l
                except:
                    pass
        with open('wfl-mk.exc') as file:
            for f in file:
                try:
                    w, l, at = f.split('\t')
                    if at.startsWith(pos.upper()):
                        self._loaded_words[w] = l
                except:
                    pass

    def _parallel_morphy(self, form, parallel, cpu_count):
        if parallel:
            search_params = [(form, y) for y in self._pos_list]

            with Pool(cpu_count) as pool:
                res = pool.map(self._args_unwrapper, search_params)
            return res
        else:
            for pos_tag in self._pos_list:
                res = self._morphy(form, pos_tag)
            return res

    def _args_unwrapper(self, args):
        return self._morphy(*args)

    def _morphy(self, form, pos, check_exceptions=True):

        self.load_words(pos)
        exceptions = self._exception_map

        if pos == '':
            substitutions = []
            substitutions_pre = []
        else:
            substitutions = MORPHOLOGICAL_SUBSTITUTIONS_SUFF[pos]
            substitutions_pre = MORPHOLOGICAL_SUBSTITUTIONS_PRE[pos]

        store_form = []

        def apply_rules(forms):

            check_prefix = [
                form[len(old):] + new
                for form in forms
                for old, new in substitutions_pre
                if form.endswith(old)

            ]
            if check_prefix:
                return check_prefix

            return [
                form[: -len(old)] + new
                for form in forms
                for old, new in substitutions
                if form.endswith(old)
            ]

        def filter_forms(forms):
            result = []
            seen = set()
            for form in forms:
                if form in self._loaded_words:
                    if form not in seen:
                        result.append(self._loaded_words[form])
                        seen.add(form)
            return result

        if check_exceptions:
            if form in exceptions:
                return filter_forms([form] + exceptions[form])

        forms = apply_rules([form])

        results = filter_forms([form] + forms)

        if results:
            return results

        while forms:
            store_form.append(forms)
            forms = apply_rules(forms)
            results = filter_forms(forms)
            if results:
                store_form = []
                return results

        if store_form:
            return store_form

        return []

    def lemmatize(self, word, pos="", parallel=True, cpu_count=4):
        if pos == "":
            lemmas = self._parallel_morphy(word, parallel, cpu_count)
        lemmas = self._morphy(word, pos)
        return min(lemmas, key=len) if lemmas else word
