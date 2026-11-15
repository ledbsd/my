FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    build-essential git vim unzip && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /src

RUN pip install jupyter==1.0.0 Flask==3.1.3 gunicorn==25.3.0 uwsgi==2.0.31 starlette==1.0.0 Jinja2==3.1.6 uvicorn==0.46.0 uvloop==0.22.1

CMD ["jupyter", "notebook", "--ip=0.0.0.0", "--port=8888", "--no-browser", "--allow-root", "--NotebookApp.token=''"]
