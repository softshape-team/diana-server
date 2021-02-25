FROM python:3

# Working directory
WORKDIR /src/app

# Environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install dependencies
RUN pip install --upgrade pip && pip install pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv install --system --deploy --ignore-pipfile

# Copy the project
COPY . .

# Run entrypoint.sh
ENTRYPOINT ["/src/app/entrypoint.sh"]
