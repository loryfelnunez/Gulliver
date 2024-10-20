from langchain.text_splitter import RecursiveCharacterTextSplitter, CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings

import arxiv
import arxivloader
from utils import utils
from datetime import datetime


client = arxiv.Client()
directory =  "./docs"
print ('directory ', directory)


def paper_generator(id_list):
    search = arxiv.Search(id_list=id_list)

    # Yield each paper from the search results
    for paper in client.results(search):
        # Download the PDF to a specified directory with a custom filename.
        paper.download_pdf(dirpath=directory)
        yield paper




def index_query(start_date, end_date, search_text):

    utils.remove_all_in_directory(directory)
    start_date_str = start_date.strftime("%Y%m%d%H%M%S")
    end_date_str = end_date.strftime("%Y%m%d%H%M%S")

    submittedDate = "[" + start_date_str + "+TO+" + end_date_str + "]"

    print(submittedDate)


    keyword = "neural nets"
    prefix = "all"
    query = "search_query={pf}:{kw}+AND+submittedDate:{sd}".format(pf=prefix, kw=keyword, sd=submittedDate)


    df = arxivloader.load(query)
    print (df.columns)
    print (df.summary)
    id_list = list(df.id)

    for paper in paper_generator(id_list):
        try:
            # Process each paper (print the title, download, etc.)
            print(f"Title: {paper.title}")
            # You can add additional processing logic here (e.g., download PDF)
        except Exception as e:
            print(f"Error processing paper: {e}")

    docs = utils.file_loader(directory)

    #
    # # Split
    # from langchain.text_splitter import RecursiveCharacterTextSplitter
    # text_splitter = RecursiveCharacterTextSplitter(
    #     chunk_size = 1500,
    #     chunk_overlap = 150
    # )
    #
    # splits = text_splitter.split_documents(docs)
    #
    # print ("LENGTH OF SPLITS ", len(splits))
    #