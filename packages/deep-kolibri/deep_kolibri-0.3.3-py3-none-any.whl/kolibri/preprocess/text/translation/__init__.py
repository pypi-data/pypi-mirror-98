

from kolibri.preprocess.text.translation.client import Translator
from kolibri.preprocess.text.translation.constants import LANGCODES, LANGUAGES  # noqa
from kolibri.preprocess.text.translation.apis import translate as __api_translate

__translator=Translator(heavy_use=True)

def translate(text, to_lang=None, from_lang='auto'):

    translated=None
    try:
        translated= __translator.translate(text=text, dest=to_lang, src=from_lang)
    except Exception as e:
        translated= __api_translate(text, dest=to_lang, src=from_lang)

    return translated

