from transformers import AutoTokenizer, AutoModelForSequenceClassification

from .base_prediction import BasePrediction
from .constants import CLASS_NAMES
from .transformation import data_preprocessing
# from config import cnf


class PytorchPrediction(BasePrediction):
    def __init__(self):
        super().__init__()

        self.loaded_model = AutoModelForSequenceClassification.from_pretrained(
            'models/bert', # Use the 12-layer BERT model, with an uncased vocab.
            num_labels = 2, # The number of output labels--2 for binary classification.
                            # You can increase this for multi-class tasks.   
            output_attentions = False, # Whether the model returns attentions weights.
            output_hidden_states = False, # Whether the model returns all hidden-states.
            
        )

        self.tokenizer = AutoTokenizer.from_pretrained('models/bert', do_lower_case=True)
        self.loaded_model.cpu()

    def predict(self, review: str):
        self.loaded_model.eval()
        # test_text = 'It is the worst product I have ever bought'
        review = data_preprocessing(review)
        tokens = self.tokenizer.encode(review, return_tensors='pt')
        result = self.loaded_model(tokens.cpu())
        prediction = result.logits.squeeze(0).softmax(0)
        class_id = prediction.argmax().item()
        score = prediction.max().item()

        return CLASS_NAMES[class_id], score
