import boto3
import nltk.data
from argparse import ArgumentParser
from botocore.exceptions import ClientError

source_document = "Amazon Translate is a text translation service. You can use Amazon Translate to translate unstructured text documents."

# Tell the NLTK data loader to look for resource files in /tmp/
nltk.data.path.append("/tmp/")
# Download NLTK tokenizers to /tmp/
nltk.download('punkt', download_dir='/tmp/')
# Load the language tokenizer
tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
# Split input text into a list of sentences
sentences = tokenizer.tokenize(source_document)
# create translate client
translate_client = boto3.client('translate')

# argument parser for target language
parser = ArgumentParser(description='Amazon Translate Large Text Documents')
parser.add_argument('-l', '--lang', required=True, help="Target Languages: en, fr, de, ja, pt, es, tr..")
args = parser.parse_args()

def main():
    translated_text = ''
    source_text_chunk = ''
    source_lang = "auto"
    target_lang = args.lang
    
    try:
        for sentence in sentences:
            if ((len(sentence.encode('utf-8')) + len(source_text_chunk.encode('utf-8')) < 5000)):
                source_text_chunk = source_text_chunk + ' ' + sentence
            else:
                translation_chunk = translate_client.translate_text(Text=source_text_chunk,SourceLanguageCode=source_lang,TargetLanguageCode=target_lang)
                translated_text = translated_text + ' ' + translation_chunk["TranslatedText"]
                source_text_chunk = sentence

        # Translate the final chunk of input text
        translation_chunk = translate_client.translate_text(Text=source_text_chunk,SourceLanguageCode=source_lang,TargetLanguageCode=target_lang)
        translated_text = translated_text + ' ' + translation_chunk["TranslatedText"]

        print(translated_text)

    except ClientError as e:
        print(e)

if __name__ == "__main__":
    main()