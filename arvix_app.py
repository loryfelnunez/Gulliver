import os
import openai
import sys

sys.path.append('../..')

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file

openai.api_key = os.environ['OPENAI_API_KEY']

#from langchain.document_loaders import ArxivLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings

import arxiv
import arxivloader

submittedDate = "[20220701080000+TO+20240701080000]"
keyword = "neural nets"
prefix = "all"
query = "search_query={pf}:{kw}+AND+submittedDate:{sd}".format(pf=prefix, kw=keyword, sd=submittedDate)

print ('query ', query)
#query = "search_query={pf}:{cat}+AND+submittedDate:{sd}".format(pf=prefix, cat=cat, sd=submittedDate)

client = arxiv.Client()

submittedDate = "[20220701080000+TO+20240701080000]"
keyword = "neural nets"
prefix = "all"
query = "search_query={pf}:{kw}+AND+submittedDate:{sd}".format(pf=prefix, kw=keyword, sd=submittedDate)


df = arxivloader.load(query)
print (df.columns)
print (df.summary)

id_list = list(df.id)

directory = "./docs"
# Define a generator function to yield papers one by one
def paper_generator(id_list):
    search = arxiv.Search(id_list=id_list)

    # Yield each paper from the search results
    for paper in client.results(search):
        # Download the PDF to a specified directory with a custom filename.
        paper.download_pdf(dirpath=directory)
        yield paper


# Use the generator
for paper in paper_generator(id_list):
    try:
        # Process each paper (print the title, download, etc.)
        print(f"Title: {paper.title}")
        # You can add additional processing logic here (e.g., download PDF)
    except Exception as e:
        print(f"Error processing paper: {e}")

from langchain.document_loaders import PyPDFLoader

loaders = []
for filename in os.listdir(directory):
    # Combine the directory path with the filename to get the full file path
    file_path = os.path.join(directory, filename)
    # Check if it's a file (to avoid directories)
    if os.path.isfile(file_path):
        loaders.append(PyPDFLoader(file_path))
        print(f"Filename: {filename}")



docs = []
for loader in loaders:
    docs.extend(loader.load())

# Split
from langchain.text_splitter import RecursiveCharacterTextSplitter
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1500,
    chunk_overlap = 150
)

splits = text_splitter.split_documents(docs)

print ("LENGTH OF SPLITS ", len(splits))

from langchain.vectorstores import Chroma
persist_directory = './docs/chroma/'

embedding = OpenAIEmbeddings()
vectordb = Chroma.from_documents(
    documents=splits,
    embedding=embedding,
    persist_directory=persist_directory
)

print("COLLECTION COUNT ", vectordb._collection.count())

question = "how many layers can a neural net have and what logic can it use"
docs = vectordb.similarity_search(question,k=3)
print ('similar docs reponse ', len(docs))
print ('answer ', docs[0].page_content)
vectordb.persist()
#
# chunk_size = 26
# chunk_overlap = 4
#
# r_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
# c_splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
#
# text1 = 'abcdefghijklmnopqrstuvwxyz'
#
#
# submittedDate = "[20220701080000+TO+20240701080000]"
# keyword = "reasoning"
# prefix = "all"
# query = "search_query={pf}:{kw}".format(pf=prefix, kw=keyword)

#query = "search_query={pf}:{cat}+AND+submittedDate:{sd}".format(pf=prefix, cat=cat, sd=submittedDate)

