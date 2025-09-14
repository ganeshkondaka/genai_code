from dotenv import load_dotenv

from pathlib import Path
from langchain_community.document_loaders import WebBaseLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore

load_dotenv()
#you can get this data from the colab python notebook
# youtube_chai_docs = ['https://docs.chaicode.com/youtube/chai-aur-c/functions/', 'https://docs.chaicode.com/youtube/chai-aur-c/loops/', 'https://docs.chaicode.com/youtube/chai-aur-git/managing-history/', 'https://docs.chaicode.com/youtube/chai-aur-sql/joins-and-keys/', 'https://docs.chaicode.com/youtube/chai-aur-c/hello-world/', 'https://docs.chaicode.com/youtube/chai-aur-devops/welcome/', 'https://docs.chaicode.com/youtube/chai-aur-django/getting-started/', 'https://docs.chaicode.com/youtube/chai-aur-html/html-tags/', 'https://docs.chaicode.com/youtube/chai-aur-c/welcome/', 'https://docs.chaicode.com/youtube/chai-aur-c/control-flow/', 'https://docs.chaicode.com/youtube/chai-aur-c/data-types/', 'https://docs.chaicode.com/youtube/chai-aur-sql/database-design-exercise/', 'https://docs.chaicode.com/youtube/chai-aur-devops/postgresql-vps/', 'https://docs.chaicode.com/youtube/chai-aur-c/introduction/', 'https://docs.chaicode.com/youtube/chai-aur-sql/joins-exercise/', 'https://docs.chaicode.com/youtube/chai-aur-devops/node-logger/', 'https://docs.chaicode.com/youtube/chai-aur-django/tailwind/', 'https://docs.chaicode.com/youtube/chai-aur-html/emmit-crash-course/', 'https://docs.chaicode.com/youtube/chai-aur-git/diff-stash-tags/', 'https://docs.chaicode.com/youtube/chai-aur-git/behind-the-scenes/', 'https://docs.chaicode.com/youtube/chai-aur-c/variables-and-constants/', 'https://docs.chaicode.com/youtube/chai-aur-devops/setup-nginx/', 'https://docs.chaicode.com/youtube/chai-aur-django/relationships-and-forms/', 'https://docs.chaicode.com/youtube/getting-started', 'https://docs.chaicode.com/youtube/chai-aur-sql/normalization/', 'https://docs.chaicode.com/youtube/chai-aur-sql/introduction/', 'https://docs.chaicode.com/youtube/chai-aur-c/operators/', 'https://docs.chaicode.com/youtube/chai-aur-sql/welcome/', 'https://docs.chaicode.com/youtube/chai-aur-devops/nginx-rate-limiting/', 'https://docs.chaicode.com/youtube/chai-aur-html/welcome/', 'https://docs.chaicode.com/youtube/chai-aur-devops/setup-vpc/', 'https://docs.chaicode.com/youtube/getting-started/', 'https://docs.chaicode.com/youtube/chai-aur-sql/postgres/', 'https://docs.chaicode.com/youtube/', 'https://docs.chaicode.com/youtube/chai-aur-devops/node-nginx-vps/', 'https://docs.chaicode.com/youtube/chai-aur-django/jinja-templates/', 'https://docs.chaicode.com/youtube/chai-aur-html/introduction/', 'https://docs.chaicode.com/youtube/chai-aur-django/welcome/', 'https://docs.chaicode.com/youtube/chai-aur-devops/nginx-ssl-setup/', 'https://docs.chaicode.com/youtube/chai-aur-git/github/', 'https://docs.chaicode.com/youtube/chai-aur-git/welcome/', 'https://docs.chaicode.com/youtube/chai-aur-git/terminology/', 'https://docs.chaicode.com/youtube/chai-aur-devops/postgresql-docker/', 'https://docs.chaicode.com/youtube/chai-aur-git/introduction/', 'https://docs.chaicode.com/youtube/chai-aur-django/models/', 'https://docs.chaicode.com/youtube/chai-aur-git/branches/'] 

youtube_chai_docs = ['https://docs.chaicode.com/youtube/chai-aur-c/functions/', 'https://docs.chaicode.com/youtube/chai-aur-c/loops/']

#chunking
text_splitter=RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=400
)

# Vector Embeddings
embedding_model = OpenAIEmbeddings(
    model="text-embedding-3-large"
    #dont need to mentions the openai api key, it will be picked up automatically
)

for link in youtube_chai_docs:
    loader = WebBaseLoader(link)
    docs=loader.load()
    print('Number of docs: ', len(docs), 'for link: ', link, '\n','docs: ', docs)

    # #adding some metadata
    # for doc in docs:
    #     doc.metadata['url'] = link 
    #     doc.metadata["section"] = link.split("/")[-3]
    #     doc.metadata["sub_section"] = link.split("/")[-2]  
    
    # #chunking
    # split_docs = text_splitter.split_documents(documents = docs) 

    # # Vector DB
    # vector_db = QdrantVectorStore.from_documents(
    #     documents=split_docs,
    #     embedding=embedding_model,
    #     url="http://localhost:6333",
    #     collection_name="chaicode_docs"
    # )