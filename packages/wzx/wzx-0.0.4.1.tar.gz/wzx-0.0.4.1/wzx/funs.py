import sys
import re
import numpy as np
import pickle
from bisect import bisect_left
import time
from tqdm import tqdm,trange


if (sys.version_info[0] < 3):
    import urllib2
    import urllib
    import HTMLParser
else:
    import html.parser
    import urllib.request
    import urllib.parse
    import html

agent = {'User-Agent':
             "Mozilla/4.0 (\
             compatible;\
             MSIE 6.0;\
             Windows NT 5.1;\
             SV1;\
             .NET CLR 1.1.4322;\
             .NET CLR 2.0.50727;\
             .NET CLR 3.0.04506.30\
             )"}


def unescape(text):
    if (sys.version_info[0] < 3):
        parser = HTMLParser.HTMLParser()
    else:
        parser = html.parser.HTMLParser()
    return (html.unescape(text))


def translate(to_translate, to_language="auto", from_language="auto"):
    """Returns the translation using google translate
    you must shortcut the language you define
    (French = fr, English = en, Spanish = es, etc...)
    if not defined it will detect it or use english by default
    Example:
    print(translate("salut tu vas bien?", "en"))
    hello you alright?
    """
    errflg = False
    try:
        base_link = "http://translate.google.cn/m?tl=%s&sl=%s&q=%s"
        if (sys.version_info[0] < 3):
            to_translate = urllib.quote_plus(to_translate)
            link = base_link % (to_language, from_language, to_translate)
            request = urllib2.Request(link, headers=agent)
            raw_data = urllib2.urlopen(request).read()
        else:
            to_translate = urllib.parse.quote(to_translate)
            link = base_link % (to_language, from_language, to_translate)
            request = urllib.request.Request(link, headers=agent)
            raw_data = urllib.request.urlopen(request, timeout=2).read()
    except BaseException as e:
        errflg = True
        print(e)
        print(type(e))

    if not errflg:
        data = raw_data.decode("utf-8")
        # expr = r'class="t0">(.*?)<'
        expr = r'class="result-container">(.*?)<'
        re_result = re.findall(expr, data)
        if (len(re_result) == 0):
            result = ""
        else:
            result = unescape(re_result[0])
        return (result)
    else:
        return ("")



class Sorted_dict(object):
    def __init__(self, seq=None, keyfunc=lambda v: v, valfunc=lambda v: v, ascending=True):
        super().__init__()
        if seq is None:
            seq = list()
        self.seq = list(seq)
        self.keyfunc = keyfunc
        self.valfunc = valfunc
        self.values = [self.valfunc(data) for data in self.seq]
        self.kvdict = {self.keyfunc(data): self.valfunc(data) for data in self.seq}

    def pop(self, pos=-1):
        val = self.values.pop(pos)
        item = self.seq.pop(pos)
        key = self.keyfunc(item)
        del self.kvdict[key]
        return item, key, val

    def insert(self, item):
        """Insert an item into a sorted list using a separate corresponding
           sorted keys list and a keyfunc() to extract the key from each item.
        """
        key = self.keyfunc(item)
        if key not in self.kvdict:
            val = self.valfunc(item)
            i = bisect_left(self.values, val)  # Determine where to insert item.
            self.values.insert(i, val)  # Insert key of item to keys list.
            self.seq.insert(i, item)  # Insert the item itself in the corresponding place.
            self.kvdict[key] = val
        else:
            old_val = self.kvdict[key]
            i = bisect_left(self.values, old_val)  # Determine where to insert item.
            while i < len(self.seq) and self.keyfunc(self.seq[i]) != key:
                i += 1
            if i < len(self.seq) and self.keyfunc(self.seq[i]) == key:
                self.pop(pos=i)
                self.insert(item)


class ViterbiSegment():
    def __init__(self, mode="train"):
        if mode == "work":  # 如果是工作模式，需要加载已经训练好的参数
            self.vocab, self.word_distance, self.max_word_len = pickle.load(open("model.pkl", 'rb'))

    # 加载人民日报语料https://pan.baidu.com/s/1gd6mslt,形成每个句子的词语列表，用于后面统计词语频数
    def load_corpus(self,fn=None, default_corpus_size=None):
        words_list = []
        #with open('./data/词性标注@人民日报199801.txt', 'r', encoding='utf8') as f:
        if fn is None:
            fn = './data/词性标注@人民日报199801.txt'
        with open(fn, 'r', encoding='utf8') as f:
            lines = f.readlines()
            lines = list(filter(lambda x: len(x) > 0, lines))  # 删除空行
            if default_corpus_size != None: lines = lines[:default_corpus_size]  # 测试阶段截取较小的语料
            print("文档总行数是", len(lines))
            for line in lines:
                line = line.replace('\n', '').split("  ")[1:]
                words = list(map(lambda x: x.split('/')[0], line))
                words = list(filter(lambda x: len(x) > 0, words))
                words_list.append(words)
        return words_list

    # 基于标注语料，训练一份词语的概率分布，以及条件概率分布————当然最终目的，是得到两个词语之间的连接权重(也可以理解为转移概率)
    # 转移概率越大，说明两个词语前后相邻的概率越大，那么，从前一个词转移到后一个词语花费的代价就越小。
    def train_simple(self, default_corpus_size=None):  # 简单的边权重计算方式
        self.word_num = {}
        self.word_pair_num = {}
        for words in self.load_corpus(default_corpus_size=default_corpus_size):
            words = ["<start>"] + words + ["<end>"]  # 首尾添加标记
            for word in words:
                self.word_num[word] = self.word_num.get(word, 0) + 1  # 词语频数

            for i in range(len(words) - 1):
                word_pair = (words[i], words[i + 1])  # 由于要计算的是条件概率，词语先后是需要考虑的
                self.word_pair_num[word_pair] = self.word_pair_num.get(word_pair, 0) + 1  # 词语对的频数
        # p(AB)=p(A)*p(B|A)=(num_A/num_all)*(num_AB/num_A)=num_AB/num_all。
        # 这个权重计算公式的优点是计算效率快；缺点是丢失了num_A带来的信息
        # 这个训练算法的效率不太重要；权重包含的信息量尽量大，或者说更精准地刻画词语对的分布，是最重要的事情。
        # hanlp设计了一个权重计算方式,来综合考虑num_A，num_all， num_A带来的信息。
        num_all = np.sum(list(self.word_num.values()))  # 语料中词语的总数
        word_pair_prob = {}
        for word_pair in self.word_pair_num:
            word_pair_prob[word_pair] = self.word_pair_num[word_pair] / num_all  # 词语对，也就是边出现的概率

        # 由于我们最终要做的是求最短路径，要求图的边权重是一个表示“代价”或者距离的量，即权重越大，两个节点之间的距离就越远。而前面得到的条件概率与这个距离是负相关的
        # 我们需要对条件概率求倒数，来获得符合场景要求的权重
        # 另外，由于条件概率可能是一个非常小的数，比如0.000001，倒数会很大。我们在运行维特比的时候，需要把多条边的权重加起来——可能遇到上溢出的情况。
        # 常用的避免上溢出的策略是去自然对数。
        self.word_distance = {}
        for word_pair in self.word_pair_num:
            self.word_distance[word_pair] = np.log(1 / word_pair_prob[word_pair])

        self.vocab = set(list(self.word_num.keys()))
        self.max_word_len = 0
        for word in self.vocab:
            if len(word) > self.max_word_len: self.max_word_len = len(word)

        model = (self.vocab, self.word_distance, self.max_word_len)
        pickle.dump(model, open("model.pkl", 'wb'))  # 保存参数

    def train_hanlp(self, default_corpus_size=None):
        """
        hanlp里使用的连接器权重计算方式稍微复杂一点，综合考虑了前词出现的概率，以及后词出现的条件规律，有点像全概率p(A)*p(B|A)=p(AB)
#         dSmoothingPara 平滑参数0.1, frequency A出现的频率, MAX_FREQUENCY 总词频
#         dTemp 平滑因子 1 / MAX_FREQUENCY + 0.00001, nTwoWordsFreq AB共现频次
#         -Math.log(dSmoothingPara * frequency / (MAX_FREQUENCY)
#         + (1 - dSmoothingPara) * ((1 - dTemp) * nTwoWordsFreq / frequency + dTemp));
        """

        self.word_num = {}
        self.word_pair_num = {}
        for words in self.load_corpus(default_corpus_size=default_corpus_size):
            words = ["<start>"] + words + ["<end>"]
            for word in words:
                self.word_num[word] = self.word_num.get(word, 0) + 1

            for i in range(len(words) - 1):
                word_pair = (words[i], words[i + 1])  # 由于要计算的是条件概率，词语先后是需要考虑的
                self.word_pair_num[word_pair] = self.word_pair_num.get(word_pair, 0) + 1

        num_all = np.sum(list(self.word_num.values()))
        dSmoothingPara = 0.1
        dTemp = 1 / num_all + 0.00001
        word_pair_prob = {}
        for word_pair in self.word_pair_num:
            word_A, word_B = word_pair
            # hanlp里的权重计算公式比较复杂，在查不到设计思路的情况下，我们默认hanlp作者是辛苦研制之后，凑出来的~
            word_pair_prob[word_pair] = dSmoothingPara * self.word_num.get(word_A) / num_all + \
                                        (1 - dSmoothingPara) * ((1 - dTemp) * self.word_pair_num[word_pair] / (
                    self.word_num.get(word_A) + dTemp))

        # 由于我们最终要做的是求最短路径，要求图的边权重是一个表示“代价”或者距离的量，即权重越大，两个节点之间的距离就越远。而前面得到的条件概率与这个距离是负相关的
        # 我们需要对条件概率求倒数，来获得符合场景要求的权重
        # 另外，由于条件概率可能是一个非常小的数，比如0.000001，倒数会很大。我们在运行维特比的时候，需要把多条边的权重加起来——可能遇到上溢出的情况。
        # 常用的避免上溢出的策略是去自然对数。
        self.word_distance = {}
        for word_pair in self.word_pair_num:
            word_A, _ = word_pair
            self.word_distance[word_pair] = np.log(1 / word_pair_prob[word_pair])
        #         print(self.word_distance)
        self.vocab = set(list(self.word_num.keys()))
        self.max_word_len = 0
        for word in self.vocab:
            if len(word) > self.max_word_len: self.max_word_len = len(word)

        model = (self.vocab, self.word_distance, self.max_word_len)
        pickle.dump(model, open("model.pkl", 'wb'))

    # 使用改版前向最大匹配法生成词图
    def generate_word_graph(self, text):
        word_graph = []
        for i in range(len(text)):
            cand_words = []
            window_len = self.max_word_len
            # 当索引快到文本右边界时，需要控制窗口长度，以免超出索引
            if i + self.max_word_len >= len(text): window_len = len(text) - i + 1
            for j in range(1, window_len):  # 遍历这个窗口内的子字符串，查看是否有词表中的词语
                cand_word = text[i: i + j]
                next_index = i + len(cand_word) + 1
                if cand_word in self.vocab:
                    cand_words.append([cand_word, next_index])
            if [text[i], i + 1 + 1] not in cand_words:
                cand_words.append([text[i], i + 1 + 1])  # 单字必须保留
            word_graph.append(cand_words)
        return word_graph

    # 使用维特比算法求词图的最短路径
    def viterbi_org(self, word_graph):
        path_length_map = {}  # 用于存储所有的路径，后面的临街词语所在位置，以及对应的长度
        word_graph = [[["<start>", 1]]] + word_graph + [[["<end>", -1]]]
        # 这是一种比较简单的数据结构
        path_length_map[("<start>",)] = [1, 0]  # start处，后面的临接词语在列表的1处，路径长度是0,。

        for i in range(1, len(word_graph)):
            distance_from_start2current = {}
            if len(word_graph[i]) == 0: continue

            for former_path in list(path_length_map.keys()):  # path_length_map内容一直在变，需要深拷贝key,也就是已经积累的所有路径
                # 取出已经积累的路径，后面的临接词语位置，以及路径的长度。
                [next_index_4_former_path, former_distance] = path_length_map[former_path]
                former_word = former_path[-1]
                later_path = list(former_path)
                if next_index_4_former_path == i:  # 如果这条路径的临接词语的位置就是当前索引
                    for current_word in word_graph[i]:  # 遍历词图数据中，这个位置上的所有换选词语，然后与former_path拼接新路径
                        current_word, next_index = current_word
                        new_path = tuple(later_path + [current_word])  # 只有int, string, tuple这种不可修改的数据类型可以hash，
                        # 也就是成为dict的key
                        # 计算新路径的长度
                        new_patn_len = former_distance + self.word_distance.get((former_word, current_word), 100)

                        path_length_map[new_path] = [next_index, new_patn_len]  # 存储新路径后面的临接词语，以及路径长度

                        # 维特比的部分。选择到达当前节点的路径中，最短的那一条
                        if current_word in distance_from_start2current:  # 如果已经有到达当前词语的路径，需要择优
                            if distance_from_start2current[current_word][1] > new_patn_len:  # 如果当前新路径比已有的更短
                                distance_from_start2current[current_word] = [new_path, new_patn_len]  # 用更短的路径数据覆盖原来的
                        else:
                            distance_from_start2current[current_word] = [new_path, new_patn_len]  # 如果还没有这条路径，就记录它
        sortest_path = distance_from_start2current["<end>"][0]
        sortest_path = sortest_path[1:-1]
        return sortest_path

    def viterbi(self, word_graph, timeout=0):
        time_start = time.time()
        word_graph = [[["<start>", 1]]] + word_graph + [[["<end>", -1]]]

        # 准备数据
        pathes = [(("<start>",), 1, 0)]
        valfunc = lambda tup: tup[2]
        keyfunc = lambda tup: tup[0]
        sdict = Sorted_dict(seq=pathes, keyfunc=keyfunc, valfunc=valfunc)

        while len(sdict.seq) > 0 and sdict.seq[0][0][-1] != '<end>':
            if timeout > 0 and time.time() - time_start > timeout:
                return ()
            # 在集合中找出最短路径
            path_item, key, val = sdict.pop(pos=0)

            # 拼接所有可能的最短路径
            former_word = path_item[0][-1]
            for word in word_graph[path_item[1]]:
                current_word, next_index = word
                new_path_item = ((*path_item[0], current_word), next_index,
                                 path_item[2] + self.word_distance.get((former_word, current_word), 250))
                sdict.insert(new_path_item)

        if sdict.seq[0][0][-1] == '<end>':
            sortest_path = sdict.seq[0][0][1:-1]
            return sortest_path

    # 对文本分词
    def segment_org(self, text):
        word_graph = self.generate_word_graph(text)
        shortest_path = self.viterbi_org(word_graph)
        return shortest_path

    # 对文本分词
    def segment(self, text, timeout=0):
        word_graph = self.generate_word_graph(text)
        shortest_path = self.viterbi(word_graph, timeout=timeout)
        return shortest_path

    def segment_multi(self, text, timeout=0):
        txt_list = text.split('。')
        seg_ = tuple()
        for i in range(len(txt_list) - 1):
            txt = txt_list[i]
            seg = self.segment(txt, timeout=timeout)
            seg_ += (seg + ('。',))
        txt = txt_list[-1]
        seg = self.segment(txt, timeout=timeout)
        seg_ += (seg)
        return seg_

    # 基于标注语料，对模型进行评价
    def evaluation(self):
        lines = self.load_corpus()
        N = len(lines)

        time_used = np.zeros(N)
        text_len = np.zeros(N)

        succeed = 0
        time_out_n = 0

        # for i in trange(100):
        for i in trange(len(lines)):
            # print(i, end=', ')
            line = lines[i]
            text = ''.join(line)
            text_len[i] = len(text)
            st = time.time()
            seg = self.segment_multi(text, timeout=5)
            time_used[i] = time.time() - st

            if tuple(line) == seg:
                succeed += 1
            elif seg == ():
                time_out_n += 1
                print()
                print('-' * 80)
                print(i, text_len[i])
                print(line)
                print(seg)
            else:
                #print()
                #print('-' * 80)
                #print(i, text_len[i])
                #print(line)
                #print(seg)
                pass

        print('+' * 80)
        print(succeed / len(lines))
        print(time_out_n / len(lines))
        #plt.plot(text_len, time_used)
