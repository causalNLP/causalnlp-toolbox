# statistical_estimator

### DataViewer

#### Get Started

```python
>>> import seaborn as sns
>>> data = sns.load_dataset("tips")
>>> data["male"] = data["sex"]=="Male"
>>> data["female"] = data["sex"]=="Female"
>>> dataViewer = DataViewer(data, target = "total_bill", features = ["male","female"],
                 target_threshold = 20.0, features_threshold = 0.5, save_to_pdf = True, ordered = False)
>>> dataViewer.target_distribution()
```

#### Some Examples With Colab

* [CivilComment](https://colab.research.google.com/drive/1YtpDrfV7vtCC9WPfYF5Y6Ln2GCh8ABTH?usp=sharing)
* [AI_scholar](https://colab.research.google.com/drive/1v7cnSf8kazFSQJXSBs2pGEcCGVWyP0-d?usp=sharing)