import os
import json
import types
from typing import List

import transformers as tfm
import torch
import numpy as np
import tqdm

from bert_reranker.gen_utils import custom_encoder_func
from bert_reranker.data.predict_gen import Predictor as ExplanationPredictor
from bert_reranker.data.predict_mtl_rating import Predictor as RatingPredictor
from bert_reranker.generation_be import generate


def trunc_model_out(feedback: str):
    fb_tokens = feedback.split()
    feedback = " ".join(fb_tokens[:50])
    if not feedback.endswith("."):
        if len(fb_tokens) < 49:
            feedback += "."
        else:
            index_of_comma = [i for i, x in enumerate(feedback) if x == "."]
            feedback = feedback[: index_of_comma[-1] + 1]
    return feedback


class BartFQA:
    def __init__(self, retriever_path: str, regions=["Australia", "CDC", "UK", "WHO"]):
        device = self.device = torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )

        ret = self.ret = torch.load(retriever_path, map_location=device)

        tokenizer = self.tokenizer = tfm.AutoTokenizer.from_pretrained(
            "facebook/bart-base"
        )
        bart_gen = tfm.BartForConditionalGeneration.from_pretrained(
            "facebook/bart-base"
        ).to(device)
        bart_gen.model.encoder = ret.bert_question_encoder.bert.model.encoder.to(device)
        bart_gen.model.decoder = ret.bert_question_encoder.bert.model.decoder.to(device)
        bart_gen = bart_gen.to(device)

        bart_gen.get_encoder = types.MethodType(custom_encoder_func, bart_gen)
        bart_gen.generate = types.MethodType(torch.no_grad()(generate), bart_gen)

        self.explanation_predictor = ExplanationPredictor(bart_gen, tokenizer)
        self.rating_predictor = RatingPredictor(ret, tokenizer)

        self.embeds = None
        self.masks = None
        self.passages = None

        self.regions = regions

    def load_kb_files(self, load_dir: str, verbose=True):
        """
        Parameters:
            load_dir:
                The directory where we are loading cached pt files representing the embedded candidates
        Returns:
            embeds:
                dictionary of region (str) mapping to embeddings (pytorch tensors)
            masks:
                dictionary of region (str) mapping to model (pytorch tensors)
            masks:
                dictionary of region (str) mapping to passages (list of dictionaries)
        """
        embeds = {}
        masks = {}
        passages = []

        for region in tqdm.auto.tqdm(self.regions, disable=not verbose):
            embeds[region] = torch.load(
                os.path.join(load_dir, f"candidates_embed_{region}.pt"),
                map_location=self.device,
            )
            masks[region] = torch.load(
                os.path.join(load_dir, f"candidates_mask_{region}.pt"),
                map_location=self.device,
            )
            passages.extend(
                json.load(open(os.path.join(load_dir, f"passages_{region}.json"), "rb"))
            )

        return embeds, masks, passages

    def generate_embeddings(self, load_dir: str, verbose=True):
        embeds = {}
        masks = {}
        passages = []

        for region in tqdm.auto.tqdm(self.regions, disable=not verbose):
            path = os.path.join(load_dir, f"passages_{region}.json")
            passage_region = json.load(open(path, "r"))
            candidates = [p["content"] for p in passage_region]

            passages.extend(passage_region)
            embeds[region], masks[region] = self.ret.embed_paragrphs(
                candidates, progressbar=verbose
            )

        return embeds, masks, passages

    def make_single_prediction(self, questions, candidates):
        predictor = self.explanation_predictor
        device = self.device

        inp = predictor.prepare_rerank_input(questions, candidates)
        pred = predictor.model.generate(
            inp["question"]["ids"].to(device),
            inp["candidate"]["ids"].to(device),
            min_length=3,
            num_beams=5,
            max_length=128,
            early_stopping=True,
            num_return_sequences=1,
        )
        return predictor.tokenizer.batch_decode(
            pred.cpu().numpy(), skip_special_tokens=True
        )

    def build_knowledge_base(self, embeds, masks, passages):
        self.embeds = embeds
        self.masks = masks
        self.passages = passages

    def retrieve_idx(self, query: str, k: int = 10) -> List[int]:
        if self.embeds is None:
            error_msg = "Please run build_knowledge_base first before attempting to perform retrieval."
            raise Exception(error_msg)
        all_scores = []

        for region in self.regions:
            scores, prediction, prob = self.ret.predict(
                query,
                (self.embeds[region], self.masks[region]),
                passages_already_embedded=True,
            )
            
            all_scores.append(scores)

        all_scores = torch.cat(all_scores, dim=1).squeeze()
        scores_np = all_scores.cpu().numpy()
        best_idx = scores_np.argsort()[::-1][:k].tolist()
        
        return best_idx

    def retrieve(self, query: str, k: int = 10) -> List[dict]:
        best_idx = self.retrieve_idx(query, k)
        best_passages = [self.passages[i] for i in best_idx]

        return best_passages

    def rate(self, query: str, candidates: List[str]) -> List[str]:
        query_repeated = [query]*len(candidates)
        predictions = self.rating_predictor.predict(query_repeated, candidates)
        
        return predictions

    def give_feedback(
        self, query: str, candidates: List[str], verbose: bool = False
    ) -> List[str]:
        query_repeated = [query]*len(candidates)

        data_list = list(zip(query_repeated, candidates))
        loader = torch.utils.data.DataLoader(data_list, batch_size=8)

        generated_text = []
        test_ratings = []

        for q, c in tqdm.auto.tqdm(loader, disable=not verbose):
            pred = [trunc_model_out(x) for x in self.make_single_prediction(q, c)]
            generated_text.extend(pred)
        
        return generated_text