from transformers import AutoModel, AutoTokenizer

class SBert:
    def __init__(self) -> None:
        self.tokenizer = AutoTokenizer.from_pretrained("cointegrated/rubert-tiny2")
        self.model = AutoModel.from_pretrained("cointegrated/rubert-tiny2")
