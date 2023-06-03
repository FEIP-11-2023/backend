FROM python:3

COPY requirements.txt .
RUN pip install --no-cache -r requirements.txt
COPY . .
CMD python3 -m app 