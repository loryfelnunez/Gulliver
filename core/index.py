from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings

import arxiv
import arxivloader
from utils import utils

from pathlib import Path

client = arxiv.Client()
directory = str(Path(Path.cwd()).parents[0])  + "/docs"
print ('directory ', directory)


def paper_generator(id_list):
    search = arxiv.Search(id_list=id_list)

    # Yield each paper from the search results
    for paper in client.results(search):
        # Download the PDF to a specified directory with a custom filename.
        paper.download_pdf(dirpath=directory)
        yield paper



def index_query(start_date, end_date, search_text):

    utils.delete_files_in_directory(directory)

    submittedDate = "[" + start_date + "+TO+" + end_date + "]"
    print ('TEST submitted date ', submittedDate)
    keyword = "neural nets"
    prefix = "all"
    query = "search_query={pf}:{kw}+AND+submittedDate:{sd}".format(pf=prefix, kw=keyword, sd=submittedDate)


    df = arxivloader.load(query)
    print (df.columns)
    print (df.summary)