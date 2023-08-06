

from kolibri.preprocess.text.translation.client import Translator
from kolibri.preprocess.text.translation.constants import LANGCODES, LANGUAGES  # noqa
from kolibri.preprocess.text.translation.apis import translate as __api_translate


def translate(text, to_lang=None, from_lang='auto',  heavy_use=False):

    translated=None
    try:
        translated= Translator(heavy_use).translate(text=text, dest=to_lang, src=from_lang)
    except:
        translated= __api_translate(text, dest=to_lang, src=from_lang)

    return translated

