from typing import List

from sklearn.preprocessing import LabelEncoder
from torch.utils.data import Dataset


class CorpusLMDataset(Dataset):
    def __init__(self, corpus):
        """Wraps a tokenized dataset which is provided as a list of tokens

        Targets = source shifted one token to the left (next token prediction)

        Args:
            corpus (List[str] or WordCorpus): List of tokens
        """
        self.source = corpus[:-1]
        self.target = corpus[1:]
        self.transforms = []

    def map(self, t):
        """Append a transform to self.transforms, in order to be applied to the data

        Args:
            t (Callable[[str], Any]): Transform of input token

        Returns:
            CorpusLMDataset: self
        """
        self.transforms.append(t)
        return self

    def __len__(self):
        """Length of corpus

        Returns:
            int: Corpus Length
        """
        return int(len(self.source))

    def __getitem__(self, idx):
        """Get a source and target token from the corpus

        Args:
            idx (int): Token position

        Returns:
            Tuple[torch.Tensor, torch.Tensor]: source=coprus[idx], target=corpus[idx+1]
        """
        src, tgt = self.source[idx], self.target[idx]
        for t in self.transforms:
            src = t(src)
            tgt = t(tgt)
        return src, tgt


class CorpusDataset(Dataset):
    def __init__(self, corpus, labels):
        """Labeled corpus dataset

        Args:
            corpus (WordCorpus, HfCorpus etc..): Input corpus
            labels (List[Any]): Labels for examples
        """
        self.corpus = corpus
        self.labels = labels
        assert len(self.labels) == len(self.corpus), "Incompatible labels and corpus"
        self.transforms = []
        self.label_encoder = None
        if isinstance(self.labels[0], str):
            self.label_encoder = LabelEncoder().fit(self.labels)

    def map(self, t):
        """Append a transform to self.transforms, in order to be applied to the data

        Args:
            t (Callable[[str], Any]): Transform of input token

        Returns:
            CorpusDataset: self
        """
        self.transforms.append(t)
        return self

    def __len__(self):
        """Length of corpus

        Returns:
            int: Corpus Length
        """
        return len(self.corpus)

    def __getitem__(self, idx):
        """Get a source and target token from the corpus

        Args:
            idx (int): Token position

        Returns:
            Tuple[torch.Tensor, torch.Tensor]: (processed sentence, label)
        """
        text, target = self.corpus[idx], self.labels[idx]
        if self.label_encoder is not None:
            target = self.label_encoder.transform([target])[0]
        for t in self.transforms:
            text = t(text)
        return text, target
