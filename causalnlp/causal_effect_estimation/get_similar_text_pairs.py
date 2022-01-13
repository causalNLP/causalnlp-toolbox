import numpy as np
import time
import torch
import os
from tqdm import trange
from tqdm import tqdm
import nltk
import pandas as pd

from sentence_transformers import SentenceTransformer, util

class Matcher:
    def _generate_saliency_map(self, embedding_batch_1, embedding_batch_2):
        with torch.no_grad():
            a = torch.tensor(embedding_batch_1, device='cuda:0')
            b = torch.tensor(embedding_batch_2, device='cuda:0')
            similarity = util.cos_sim(a, b)
            positions = torch.where(similarity > 0.6)
            ret = [positions[0].cpu().numpy().copy(), positions[1].cpu().numpy().copy()], similarity[
                similarity > 0.6].cpu().numpy().copy()
        del similarity
        del positions
        return ret

    def __init__(self, list1, list2, cache_dir = './.cache/', threshold = 0.6, clean_cache = False):
        if (clean_cache):
            os.system(f"rm -rf {cache_dir}")
        self.corpus_1 = list1
        self.corpus_2 = list2
        self.cache_dir = cache_dir
        self.threshold = threshold
        try:
            self.model = SentenceTransformer(os.path.join(self.cache_dir, 'sbert_multi_lingual'), device='cuda')
        except:
            self.model = SentenceTransformer('paraphrase-multilingual-mpnet-base-v2')
            self.model.save(os.path.join(self.cache_dir, 'sbert_multi_lingual'))
        print("Finish load the model")

        try:
            embeddings_1 = np.load(os.path.join(self.cache_dir, 'embeddings_1.npy'), allow_pickle=True)
        except:
            embeddings_1 = np.array(self.model.encode(corpus_1, convert_to_tensor=True).cpu())
            print("Finish calculating embeddings_1")
            np.save(os.path.join(self.cache_dir, 'embeddings_1.npy'), embeddings_1)

        try:
            embeddings_2 = np.load(os.path.join(self.cache_dir, 'embeddings_2.npy'), allow_pickle=True)
        except:
            embeddings_2 = np.array(self.model.encode(corpus_2, convert_to_tensor=True).cpu())
            print("Finish calculating embeddings_2")
            np.save(os.path.join(self.cache_dir, 'embeddings_2.npy'), embeddings_2)

        print("Finish embedding the corpus")
        i,j = 0,0
        n = len(embeddings_1)
        li1, li2 = [], []
        last_time = time.time()

        print("Calculating the saliency map:")
        for i in trange(0,n,500):
            while (j < n):
                x, y = self._generate_saliency_map(embeddings_1[i:min(i + 500, n)], embeddings_2[j:min(j + 500, n)])
                x[0] += i+1
                x[1] += j+1
                li1.append(x)
                li2.append(y)
                j += 500
            j = 0
        np.save(os.path.join(self.cache_dir, 'edge1.npy'), np.array(li1))
        np.save(os.path.join(self.cache_dir, 'edge2.npy'), np.array(li2))
        self.li1 = li1
        self.li2 = li2
        self.pairs = []

    def general_matcher(self, length_rate = None):
        print("Filtering edges:")
        len_corpus_1, len_corpus_2 = [], []
        if (length_rate != None):
            nltk.download('punkt')
            try:
                len_corpus_1 = np.load(os.path.join(self.cache_dir, 'corpus_length_1.npy'), allow_pickle=True)
            except:
                print("Calculating the length of corpus_1:")
                for i in tqdm(self.corpus_1):
                    len_corpus_1.append(len(nltk.word_tokenize(i)))
                len_corpus_1 = np.array(len_corpus_1)
                np.save(os.path.join(self.cache_dir, 'corpus_length_1.npy'), len_corpus_1)

            try:
                len_corpus_2 = np.load(os.path.join(self.cache_dir, 'corpus_length_2.npy'), allow_pickle=True)
            except:
                print("Calculating the length of corpus_2:")
                for i in tqdm(self.corpus_2):
                    len_corpus_2.append(len(nltk.word_tokenize(i)))
                len_corpus_2 = np.array(len_corpus_2)
                np.save(os.path.join(self.cache_dir, 'corpus_length_2.npy'), len_corpus_2)

        print("Checking the edges")
        sum = 0
        li1, li2 = self.li1, self.li2
        pairs = []
        for i in trange(len(li1)):
            for j in range(len(li1[i][1])):
                pair = [li1[i][0][j], li1[i][1][j]]
                value = li2[i][j]
                rate = 1.0 * len_corpus_1[pair[0] - 1] / len_corpus_2[pair[1] - 1]
                if (rate <= 0 or value < self.threshold):
                    continue
                if (rate < 1):
                    rate = 1 / rate
                if (rate > length_rate):
                    continue
                sum += 1
                pairs.append(pair)

        with open(os.path.join(self.cache_dir, 'pairs.in'), 'w') as f:
            f.write(f"{sum}\n")
            for i in pairs:
                f.write(f"{i[0]} {i[1]}\n")
        print(f"The edge number is {sum}.")

        import dinic
        os.system(f"g++ {dinic.__file__[:-11] + 'dinic.cpp'} -o {os.path.join(self.cache_dir, 'dinic')}")
        matched_pairs = os.popen(f"./{os.path.join(self.cache_dir, 'dinic')} <{os.path.join(self.cache_dir, 'pairs.in')}").read()

        print("Reading matched pairs")
        for i in tqdm(matched_pairs.split("\n")):
            try:
                x, y = i.split(' ')
                x, y = int(x), int(y)
                self.pairs.append((x, y))
            except:
                pass
        print(f"The matched pairs number is {len(self.pairs)}.")


    def get_matched_pair_ixs(self):
        pairs = [[], []]
        for i in tqdm(self.pairs):
            pairs[0].append(i[0]-1)
            pairs[1].append(i[1]-1)
        data = {"corpus1_idx":pairs[0], "corpus2_idx":pairs[1]}
        return pd.DataFrame(data)

    def get_matched_pairs(self):
        pairs = [[],[]]
        for i in self.pairs:
            pairs[0].append(self.corpus_1[i[0]-1])
            pairs[1].append(self.corpus_2[i[1]-1])
        data = {"corpus1":pairs[0], "corpus2":pairs[1]}
        return pd.DataFrame(data)


    def save_matched_pairs_to_file(self, output_path = "./pairs.csv"):
        df = self.get_matched_pairs()
        df.to_csv(output_path)

if __name__ == '__main__':
    PATH_1 = "/home/roboadm/zhlyu/projects/MTX/datasets/fr-es/train.fr"
    PATH_2 = "/home/roboadm/zhlyu/projects/MTX/datasets/es-fr/train.fr"
    corpus_1 = []
    corpus_2 = []
    with open(PATH_1, "r") as f:
        for i in f.readlines():
            corpus_1.append(i)
    with open(PATH_2, "r") as f:
        for i in f.readlines():
            corpus_2.append(i)
    matcher = Matcher(corpus_1, corpus_2, threshold = 0.7)
    matcher.general_matcher(length_rate = 1.1)
    print(matcher.get_matched_pair_ixs()[0:10])
    print(matcher.get_matched_pairs()[0:10])
    matcher.save_matched_pairs_to_file()

