from torch import nn


def aggregate_annotations(annotated_text):
    aggregate_labels = []
    start = 0
    end = 0
    current_label = ""
    for token in annotated_text["spans"]:
        if (
            token["label"].startswith("I")
            and current_label == token["label"].split("-")[-1]
        ):
            end = token["end"]
        elif token["label"].startswith("B-"):
            aggregate_labels.append(
                {"start": start, "end": end, "label": current_label}
            )
            start = token["start"]
            end = token["end"]
            current_label = token["label"].split("-")[-1]

    annotation = [start, end, current_label]
    if annotation != [
        aggregate_labels[-1]["start"],
        aggregate_labels[-1]["end"],
        aggregate_labels[-1]["label"],
    ]:
        aggregate_labels.append(
            {"start": annotation[0], "end": annotation[1], "label": annotation[-1]}
        )
    return {"text": annotated_text["text"], "spans": aggregate_labels[1:]}


class CamembertForTokenClassification(nn.Module):
    def __init__(self, camembert_model, classifier, tokenizer, labels):
        super().__init__()
        self.camembert_model = camembert_model
        self.classifier = classifier
        self.tokenizer = tokenizer
        self.labels = labels

    def forward(self, text):
        tokens = self.tokenizer(text, return_tensors="pt", return_offsets_mapping=True)
        logits = self.classifier(
            self.camembert_model(
                input_ids=tokens["input_ids"], attention_mask=tokens["attention_mask"]
            ).last_hidden_state
        )
        output_labels = [
            self.labels[i] for i in logits.squeeze(0).argmax(dim=1).tolist()
        ]
        annotated_text = {
            "text": text,
            "spans": [
                {"start": offset[0], "end": offset[1], "label": label}
                for offset, label in zip(
                    tokens["offset_mapping"].squeeze(0).tolist()[1:-1],
                    output_labels[1:-1],
                )
            ],
        }
        return aggregate_annotations(annotated_text)
