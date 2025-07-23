from mcp.server.fastmcp import FastMCP

import os
import pickle
# Loader
from langchain_community.document_loaders.csv_loader import CSVLoader
# Splitter
from langchain_text_splitters import RecursiveCharacterTextSplitter
# Embedding
from langchain_openai import OpenAIEmbeddings
# Store
from langchain_chroma import Chroma
from langchain_community.retrievers import BM25Retriever
from langchain.retrievers import EnsembleRetriever
from kiwipiepy import Kiwi

mcp = FastMCP("Wine Price Search")

os.environ["OPENAI_API_KEY"] = ""

BASE_DIR = os.path.dirname(os.path.abspath(__file__))        
PROJECT_ROOT = os.path.dirname(BASE_DIR)                   
DATASET_DIR = os.path.join(PROJECT_ROOT, './mcp_server/dataset') 
CSV_FILE_PATH = os.path.join(DATASET_DIR, 'wine_price.csv')

kiwi = Kiwi()

def kiwi_tokenize(text):
    return [token.form for token in kiwi.tokenize(text)]

vector_db = os.path.join("./mcp_server/vector_store/wine_price", "chroma.sqlite3")
if not os.path.exists(vector_db):
    loader = CSVLoader(CSV_FILE_PATH, encoding="utf-8")
    docs = loader.load()

    text_splliter = RecursiveCharacterTextSplitter(
        chunk_size = 500,
        chunk_overlap = 100
    )

    chunks = text_splliter.split_documents(docs)

    embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")

    VECTOR_STORE_PATH = "./mcp_server/vector_store"
    WINE_PRICE_VECTOR_STORE_PATH = os.path.join(VECTOR_STORE_PATH, "wine_price")
    vectorstore = Chroma.from_documents(
        chunks,
        embedding=embedding_model,
        persist_directory=WINE_PRICE_VECTOR_STORE_PATH
    )
    similarity_retriever = vectorstore.as_retriever()

    WINE_PRICE_BM25_STORE_PATH = os.path.join(VECTOR_STORE_PATH, "wine_price")
    bm25_retriever = BM25Retriever.from_documents(chunks, preprocess_func=kiwi_tokenize)
    bm25_file_name = 'bm25_retriever_wine_price.pkl'
    bm25_path = os.path.join(WINE_PRICE_BM25_STORE_PATH, bm25_file_name)
    with open(bm25_path, 'wb') as f:
        pickle.dump(bm25_retriever, f)

@mcp.tool()
def wine_price_search(query : str) -> str:
    """
    와인의 가격 및 재고량을 검색하는 RAG 기반 도구
    Parameter : query (와인 이름 및 연도)
    """
    # Vector DB 가져오기
    embedding_model = OpenAIEmbeddings(model="text-embedding-3-small")        # OpenAI 임베딩을 사용하여 기본 임베딩 설정
    STORE_PATH = os.path.join('./mcp_server/vector_store', 'wine_price')
    # Vector store 로드
    vectorstore = Chroma(persist_directory=STORE_PATH, embedding_function=embedding_model)
    similarity_retriever = vectorstore.as_retriever()

    # BM25 Retriever
    bm25_file_name = 'bm25_retriever_wine_price.pkl'
    bm25_path = os.path.join(STORE_PATH, bm25_file_name)
    if os.path.exists(bm25_path):
        with open(bm25_path, 'rb') as f:
            bm25_retriever = pickle.load(f)
        bm25_retriever.k = 2

    ensemble_retriever = EnsembleRetriever(
        retrievers=[similarity_retriever, bm25_retriever],
        weights=[0.3, 0.7]
    )

    return ensemble_retriever.invoke(query)


if __name__ == '__main__':
    mcp.run(transport="stdio")