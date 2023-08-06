from kolibri.dnn import is_tf_available, is_torch_available



__default_models_configs={
    "classification": {
        "tf":{
            "emails":{},
            "social_media": {},
            "default": {}
        },
        "pt": {
            "emails": {},
            "social_media": {},
            "default": {}
        },
        "sklearn": {
            "emails": {},
            "social_media": {},
            "default": {}
        }
    }
}


def get_default_model(task,  task_options=None):
    """
    Select a default model to use for a given task. Defaults to pytorch if ambiguous.
    Returns
        :obj:`str` The model string representing the default model for this pipeline
    """
    if is_torch_available() and not is_tf_available():
        framework = "pt"
    elif is_tf_available() and not is_torch_available():
        framework = "tf"
    else:
        framework = "sklearn"
    default_models = __default_models_configs[task][framework]
    if task_options:
        if task_options not in default_models:
            raise ValueError("The task does not provide any default models for options {}".format(task_options))
        default_model=default_models[task_options]
    else:
        # XXX This error message needs to be updated to be more generic if more tasks are going to become
        # parametrized
        raise ValueError('The task defaults is not correctly selected.')

    return default_model, framework