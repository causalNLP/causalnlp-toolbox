from pandas.core.arrays.numeric import T
import seaborn as sns
import pandas as pd
from tqdm import tqdm


class DataViewer(object):
    r"""DataViewer build from pandas dataset, with features and target,
    To visualize the Uni-variable distribution of feature and target,
    Or the Bi-variable relation feature|target>=target_threshold, Corr(feature, target)

    The feature to be processed must be a number, in some cases the preprocess to the dataset is needed.

    Example::
        >>> import seaborn as sns
        >>> data = sns.load_dataset("tips")
        >>> data["male"] = data["sex"]=="Male"
        >>> data["female"] = data["sex"]=="Female"
        >>> dataViewer = DataViewer(data, target = "total_bill", features = ["male","female"],
                 target_threshold = 20.0, features_threshold = 0.5, save_to_pdf = True, ordered = False)
        >>> dataViewer.target_distribution()
    """
    def __init__(self, dataset, target="label", features=None,
                 target_threshold=0.5, features_threshold=0.5, split=None,
                 ordered=False, save_to_pdf=False):
        self.dataset = dataset
        self.target = target
        if (features == None):
            self.features = list(self.dataset.index)
        else:
            self.features = features
        self.target_threshold = target_threshold
        self.features_threshold = features_threshold
        self.split = split
        self.ordered = ordered
        self.save_to_pdf = save_to_pdf

    def set_target(self, target):
        self.target = target

    def set_features(self, features):
        self.features = features

    def set_target_threshold(self, target_threshold):
        self.target_threshold = target_threshold

    def set_features_threshold(self, features_threshold):
        self.features_threshold = features_threshold

    def set_split(self, split):
        self.split = split

    def _get_rate(self, name):
        if (len(self.dataset[self.dataset[name] >= 0]) == 0):
            return 0
        return 1.0 * len(self.dataset[self.dataset[name] >= self.features_threshold]) / len(
            self.dataset[self.dataset[name] >= 0])

    def _get_target_rate(self, name = None):
        subset = self.dataset[self.dataset[name] >= self.features_threshold]
        if (len(subset) == 0):
            return 0
        return 1.0*len(subset[subset[self.target] >= self.target_threshold])/len(subset)

    # P(features>features_threshold)
    def features_distribution(self):
        features = []
        rate = []
        for i in self.features:
            features.append(i)
            rate.append(self._get_rate(i))
        df = pd.DataFrame.from_dict({"features": features, "rate": rate})
        if self.ordered:
            df = df.sort_values(by=['rate'], ascending=False)

        g = sns.barplot(y="features", x="rate", data=df)
        sum = 0
        for index, row in df.iterrows():
            g.text(row['rate'], sum + 0.3, round(row["rate"] * 100, 3))
            sum += 1

        if (self.save_to_pdf):
            plt.tight_layout()
            plt.savefig('a.pdf', dpi=300)
        plt.show()

    # P(target>=target_threshold | features>features_threshold)
    def target_distribution(self):
        tags = []
        rate = []
        for i in self.features:
            tags.append(i)
            rate.append(self._get_target_rate(i))
        df = pd.DataFrame.from_dict({"target_rate_in_sub_datasets": tags, "rate": rate})
        if self.ordered:
            df = df.sort_values(by=['rate'], ascending=False)

        g = sns.barplot(y="target_rate_in_sub_datasets", x="rate", data=df)
        sum = 0
        for index, row in df.iterrows():
            g.text(row['rate'], sum + 0.3, round(row["rate"] * 100, 3))
            sum += 1

        if (self.save_to_pdf):
            plt.tight_layout()
            plt.savefig('a.pdf', dpi=300)
        plt.show()

    # corr(key, target), method = {‘pearson’, ‘kendall’, ‘spearman’}
    def key_traget_correlation(self, method='pearson'):
        x = self.dataset.corr(method) if not method is None else self.dataset.corr()
        idx = list(x.index)
        for i in range(len(idx)):
            if not idx[i] in self.features:
                idx[i] = None
            else:
                idx[i] = " ".join(idx[i].split("_"))
        x["index"] = idx

        if self.ordered:
            x = x.sort_values(by=['rate'], ascending=False)
        g = sns.barplot(y='index', x=self.target, data=x)
        sum = 0
        for index, row in x.iterrows():
            if (row['index'] != None):
                g.text(row[self.target], sum + 0.3, round(row[self.target] * 100, 3))
                sum += 1

        if (self.save_to_pdf):
            plt.tight_layout()
            plt.savefig('a.pdf', dpi=300)
        plt.show()

    # kernel_pdf/cdf(feature)
    def feature_distribution_continuous(self, feature, log_format=False, cumulative=False, data_trans=None):
        if (type(feature) == list):
            for i in feature:
                x = self.dataset[i][self.dataset[i] >= 0]
                if cumulative:
                    sns.kdeplot(x, cumulative=True, label=i)
                else:
                    ax = sns.distplot(x, kde_kws={"label": i})
        else:
            x = self.dataset[feature][self.dataset[feature] >= 0]
            if cumulative:
                sns.kdeplot(x, cumulative=True, label=feature)
            else:
                ax = sns.distplot(x, kde_kws={"label": feature})
        import matplotlib.pyplot as plt
        if (log_format):
            ax.set_yscale('log')

        plt.legend()
        if (self.save_to_pdf):
            plt.tight_layout()
            plt.savefig('a.pdf', dpi=300)
        # plt.xlim(0, 1)

    # kernel_pdf/cdf(target|feature>features_threshold)
    def target_distribution_continuous(self, feature, log_format=False, cumulative=False, data_trans=None):
        if (type(feature) == list):
            for i in feature:
                x = all_data[self.target][all_data[i] >= self.features_threshold]
                if cumulative:
                    sns.kdeplot(x, cumulative=True, label=i)
                else:
                    ax = sns.distplot(x, hist=False, kde_kws={"label": i})
        else:
            x = all_data[self.target][all_data[feature] >= self.features_threshold]

            if cumulative:
                sns.kdeplot(x, cumulative=True, label=feature)
            else:
                ax = sns.distplot(x, kde_kws={"label": feature})
        import matplotlib.pyplot as plt
        if (log_format):
            ax.set_yscale('log')

        plt.legend()
        if (self.save_to_pdf):
            plt.tight_layout()
            plt.savefig('a.pdf', dpi=300)
        plt.xlim(0, 1)

    # kernel_pdf(target, feature>features_threshold)
    def feature_relation_2d(self, x, y=None):
        if (y == None):
            y = self.target
        subdataset = self.dataset[self.dataset[x] > 0]
        ax = sns.jointplot(x=y, y=x, data=subdataset, kind="kde", shade=True, cbar=True)

        if (self.save_to_pdf):
            plt.tight_layout()
            plt.savefig('a.pdf', dpi=300)
