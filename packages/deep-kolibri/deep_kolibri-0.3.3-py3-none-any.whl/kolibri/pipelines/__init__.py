#
# import warnings
# from typing import TYPE_CHECKING, Any, Dict, Optional, Tuple, Union
# from kolibri.logger import get_logger
# from kolibri.dnn import is_tf_available, is_torch_available
# from kolibri.pipelines.default_models import get_default_model
# if is_tf_available():
#     import tensorflow as tf
#
#     from kolibri.dnn.tasks.text import (
#         TF_MODEL_FOR_QUESTION_ANSWERING_MAPPING,
#         TF_MODEL_FOR_SEQ_TO_SEQ_CAUSAL_LM_MAPPING,
#         TF_MODEL_FOR_SEQUENCE_CLASSIFICATION_MAPPING,
#         TF_MODEL_FOR_TOKEN_CLASSIFICATION_MAPPING,
#         TF_MODEL_WITH_LM_HEAD_MAPPING,
#         TFAutoModel,
#         TFAutoModelForCausalLM,
#         TFAutoModelForMaskedLM,
#         TFAutoModelForQuestionAnswering,
#         TFAutoModelForSeq2SeqLM,
#         TFAutoModelForSequenceClassification,
#         TFAutoModelForTokenClassification,
#     )
#
# if is_torch_available():
#     import torch
#
#     from ..models.auto.modeling_auto import (
#         MODEL_FOR_MASKED_LM_MAPPING,
#         MODEL_FOR_QUESTION_ANSWERING_MAPPING,
#         MODEL_FOR_SEQ_TO_SEQ_CAUSAL_LM_MAPPING,
#         MODEL_FOR_SEQUENCE_CLASSIFICATION_MAPPING,
#         MODEL_FOR_TABLE_QUESTION_ANSWERING_MAPPING,
#         MODEL_FOR_TOKEN_CLASSIFICATION_MAPPING,
#         AutoModel,
#         AutoModelForCausalLM,
#         AutoModelForMaskedLM,
#         AutoModelForQuestionAnswering,
#         AutoModelForSeq2SeqLM,
#         AutoModelForSequenceClassification,
#         AutoModelForTableQuestionAnswering,
#         AutoModelForTokenClassification,
#     )
# if TYPE_CHECKING:
#     from ..modeling_tf_utils import TFPreTrainedModel
#     from ..modeling_utils import PreTrainedModel
#
# logger = get_logger(__name__)
#
#
# # Register all the supported tasks here
# SUPPORTED_TASKS = {
#
#     "classification": {
#         "impl": TextClassificationPipeline,
#         "tf": TFAutoModelForSequenceClassification if is_tf_available() else None,
#         "pt": AutoModelForSequenceClassification if is_torch_available() else None,
#         "default": {
#             "model": {
#                 "pt": "distilbert-base-uncased-finetuned-sst-2-english",
#                 "tf": "distilbert-base-uncased-finetuned-sst-2-english",
#             },
#         },
#     },
#     "ner": {
#         "impl": TokenClassificationPipeline,
#         "tf": TFAutoModelForTokenClassification if is_tf_available() else None,
#         "pt": AutoModelForTokenClassification if is_torch_available() else None,
#         "default": {
#             "model": {
#                 "pt": "dbmdz/bert-large-cased-finetuned-conll03-english",
#                 "tf": "dbmdz/bert-large-cased-finetuned-conll03-english",
#             },
#         },
#     },
#     "summarization": {
#         "impl": SummarizationPipeline,
#         "tf": TFAutoModelForSeq2SeqLM if is_tf_available() else None,
#         "pt": AutoModelForSeq2SeqLM if is_torch_available() else None,
#         "default": {"model": {"pt": "sshleifer/distilbart-cnn-12-6", "tf": "t5-small"}},
#     },
#     # This task is a special case as it's parametrized by SRC, TGT languages.
#     "topics": {
#         "impl": TranslationPipeline,
#         "tf": TFAutoModelForSeq2SeqLM if is_tf_available() else None,
#         "pt": AutoModelForSeq2SeqLM if is_torch_available() else None,
#         "default": {
#             ("en", "fr"): {"model": {"pt": "t5-base", "tf": "t5-base"}},
#             ("en", "de"): {"model": {"pt": "t5-base", "tf": "t5-base"}},
#             ("en", "ro"): {"model": {"pt": "t5-base", "tf": "t5-base"}},
#         },
#     },
# }
#
#
# def check_task(task: str) -> Tuple[Dict, Any]:
#     """
#     Checks an incoming task string, to validate it's correct and return the default Pipeline and Model classes, and
#     default models if they exist.
#     Args:
#         task (:obj:`str`):
#             The task defining which pipeline will be returned. Currently accepted tasks are:
#             - :obj:`"feature-extraction"`
#             - :obj:`"sentiment-analysis"`
#             - :obj:`"ner"`
#             - :obj:`"question-answering"`
#             - :obj:`"fill-mask"`
#             - :obj:`"summarization"`
#             - :obj:`"translation_xx_to_yy"`
#             - :obj:`"translation"`
#             - :obj:`"text-generation"`
#             - :obj:`"conversational"`
#     Returns:
#         (task_defaults:obj:`dict`, task_options: (:obj:`tuple`, None)) The actual dictionary required to initialize the
#         pipeline and some extra task options for parametrized tasks like "translation_XX_to_YY"
#     """
#     if task in SUPPORTED_TASKS:
#         targeted_task = SUPPORTED_TASKS[task]
#         return targeted_task, None
#
#     if task.startswith("translation"):
#         tokens = task.split("_")
#         if len(tokens) == 4 and tokens[0] == "translation" and tokens[2] == "to":
#             targeted_task = SUPPORTED_TASKS["translation"]
#             return targeted_task, (tokens[1], tokens[3])
#         raise KeyError("Invalid translation task {}, use 'translation_XX_to_YY' format".format(task))
#
#     raise KeyError(
#         "Unknown task {}, available tasks are {}".format(task, list(SUPPORTED_TASKS.keys()) + ["translation_XX_to_YY"])
#     )
#
#
# def pipeline(task, model= None, config= None):
#     """
#     Utility factory method to build a :class:`~transformers.Pipeline`.
#     Pipelines are made of:
#         - A :doc:`tokenizer <tokenizer>` in charge of mapping raw textual input to token.
#         - A :doc:`model <model>` to make predictions from the inputs.
#         - Some (optional) post processing for enhancing model's output.
#     Args:
#         task (:obj:`str`):
#             The task defining which pipeline will be returned:
#
#         model: The model that will be used by the pipeline to make predictions.
#         config: The configuration that will be used by the pipeline to instantiate the model.
#     """
#     # Retrieve the task
#     targeted_task, task_options = check_task(task)
#
#     # Use default model/config/tokenizer for the task if no model is provided
#     if model is None:
#         # At that point framework might still be undetermined
#         model, framework = get_default_model(targeted_task, task_options)
#
#
#     task_class, model_class = targeted_task["impl"], targeted_task[framework]
#
#
#
#     return task_class