import requests
import requests_cache
from templates.text import TextTemplate
from templates.button import ButtonTemplate

def process(input, entities):
    output = {}
    try:
        word = entities['synonym'][0]['value']

        with requests_cache.enabled('synonym_cache', backend='sqlite', expire_after=86400):
            r = requests.get('https://api.datamuse.com/words', params={
                'rel_syn': word,
                'max': 5
            })
            data = r.json()

        if data:
            synonyms = ', '.join([item['word'] for item in data])

            template = TextTemplate()
            template.set_text('Synonyms for "{}": {}'.format(word, synonyms))
            text = template.get_text()

            template = ButtonTemplate(text)
            template.add_web_url('More Synonyms', 'https://www.thesaurus.com/browse/{}'.format(word))

            output['input'] = input
            output['output'] = template.get_message()
            output['success'] = True
        else:
            raise ValueError("No synonyms found")

    except Exception as e:
        error_message = 'I couldn\'t find any synonyms for the word "{}".'.format(word)
        error_message += '\nPlease try another word, like:'
        error_message += '\n  - happy'
        error_message += '\n  - sad'
        error_message += '\n  - fast'
        output['error_msg'] = TextTemplate(error_message).get_message()
        output['success'] = False

    return output

