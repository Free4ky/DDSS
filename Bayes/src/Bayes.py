import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn import datasets


class NaiveBayes:

    def fit(self, X, y):
        n_samples, n_features = X.shape
        self._classes = np.unique(y)
        n_classes = len(self._classes)

        # calculate mean, var, and prior for each class
        self._mean = np.zeros((n_classes, n_features), dtype=np.float64)
        self._var = np.zeros((n_classes, n_features), dtype=np.float64)
        self._priors = np.zeros(n_classes, dtype=np.float64)

        for idx, c in enumerate(self._classes):
            X_c = X[y == c]
            self._mean[idx, :] = X_c.mean(axis=0)
            self._var[idx, :] = X_c.var(axis=0)
            self._priors[idx] = X_c.shape[0] / float(n_samples)

    def predict(self, X):
        y_pred = [self._predict(x) for x in X]
        return np.array(y_pred)

    def _predict(self, x):
        posteriors = []

        # calculate posterior probability for each class
        for idx, c in enumerate(self._classes):
            prior = np.log(self._priors[idx])
            posterior = np.sum(np.log(self._pdf(idx, x)))
            posterior = posterior + prior
            posteriors.append(posterior)

            # print(posterior)

        # return class with the highest posterior
        return self._classes[np.argmax(posteriors)]

    def _pdf(self, class_idx, x):
        mean = self._mean[class_idx]
        var = self._var[class_idx]
        numerator = np.exp(-((x - mean) ** 2) / (2 * var))
        denominator = np.sqrt(2 * np.pi * var)
        return numerator / denominator


def accuracy(y_true, y_pred):
    return np.sum(y_true == y_pred) / len(y_true)


if __name__ == '__main__':
    dataset = datasets.load_iris()
    X, y = dataset.data, dataset.target

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=123)

    naive_byes = NaiveBayes()

    naive_byes.fit(X_train, y_train)

    y_pred = naive_byes.predict(X_test)
    res_df = pd.DataFrame(
        data=np.c_[X_test, y_test, y_pred],
        columns=dataset.feature_names + ['target', 'prediction']
    )
    res_df.target = res_df.target.astype(int)
    res_df.prediction = res_df.prediction.astype(int)
    print(f"Accuracy: {accuracy(y_test, y_pred)}")
    print(res_df)
