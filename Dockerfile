FROM python:3.10-slim
WORKDIR /usr/src/app
COPY . /usr/src/app
RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev
EXPOSE 8000
CMD ["poetry", "run","uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]