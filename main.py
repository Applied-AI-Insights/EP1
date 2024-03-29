from langchain_community.llms import Ollama
from langchain_community.document_loaders import WebBaseLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import GPT4AllEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA

ollama = Ollama(base_url="http://localhost:11434", model='llama2-chinese')

loader = WebBaseLoader('https://zh.wikipedia.org/wiki/LLaMA')
data = loader.load()

text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
all_splits = text_splitter.split_documents(data)

vectorstores = Chroma.from_documents(documents=all_splits, embedding=GPT4AllEmbeddings())

qachain = RetrievalQA.from_chain_type(ollama,retriever=vectorstores.as_retriever())

question = "請介紹一下Llama2"

print(qachain.invoke(question))