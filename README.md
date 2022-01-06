# Online demo:

- APP url: ai.hoang.tech:8000/
- DB connection string: mongodb://hoangntruong:NYTPnHoang@ai.hoang.tech:27018/edu_db/

> Crawler receiver: $HOST:$PORT/crawler-receiver/

> Example query: ai.hoang.tech:8000/university/?institution=stanford university

**Note:** crawler-receiver may need a long time for process 1000 rows 
data file because of calling duckduckgo API (My server have limited network bandwidth for this project)

# Deployment

### 1. With docker
> docker-compose up -d

**Docker-compose Environment Variable:**
- EDU_DATABASE_USERNAME: mongodb username, default by 'mongoadmin'
- EDU_DATABASE_PASSWORD: mongodb password, default by 'P@SSWD22' 
- EDU_DATABASE_HOST: mongodb host alias/IP, default by 'mongo'
- EDU_DATABASE_PORT: mongodb port, default by '27017' 
- EDU_DATABASE_NAME: mongodb database name, default by 'edu_db' 

### 2. App only

> uvicorn api:app --host 0.0.0.0

**Docker-compose Environment Variable:**
- DATABASE_USERNAME: if not set, default by 'hoangntruong'
- DATABASE_PASSWORD: if not set, default by 'NYTPnHoang' 
- DATABASE_HOST: if not set, default by 'ai.hoang.tech'
- DATABASE_PORT: if not set, default by '27017' 
- DATABASE_NAME: if not set, default by 'edu_db' 
