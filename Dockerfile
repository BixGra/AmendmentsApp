FROM python:3.10

WORKDIR /etc/AmendmentApp

COPY ./requirements.txt /etc/AmendmentApp/requirements.txt

RUN pip install --upgrade pip && pip --no-cache-dir install -r /etc/AmendmentApp/requirements.txt

COPY . /etc/AmendmentApp/.

ENV PYTHONPATH $PYTHONPATH:$PATH:/etc/AmendmentApp/src/

ENV PATH /opt/conda/envs/env/bin:$PATH

ENV PROJECT_PATH /etc/AmendmentApp/src/

EXPOSE 8000

ENTRYPOINT gunicorn -b 0.0.0.0:8000 -k uvicorn.workers.UvicornWorker src.main:app --threads 2 --workers 1 --timeout 1000 --graceful-timeout 30
