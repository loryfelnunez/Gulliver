import os
import openai
import sys

sys.path.append('../..')

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key = os.environ['OPENAI_API_KEY']

from langchain.document_loaders import ArxivLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter


chunk_size = 26
chunk_overlap = 4

r_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
c_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)

text1 = 'abcdefghijklmnopqrstuvwxyz'

loader = ArxivLoader(
    query='reasoning',
    load_max_docs=20
)

docs = []

for doc in loader.get_summaries_as_docs():
    docs.append(doc)
    print ('length of summary')
    print(len(docs[0].page_content))
    print(docs[0].metadata)
    if len(docs) > 10:
        #do some ops
        docs = []
print (len (docs))

