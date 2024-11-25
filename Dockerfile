FROM python:3.12-slim-bullseye

WORKDIR /news_con/

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt && python -m spacy download en_core_web_sm

COPY . .

# CMD [ "python3", "-m", "flask", "--app", "core/nsa", "run", "-h", "0.0.0.0"]
