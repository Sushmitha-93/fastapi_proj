# Python version
FROM python:3.9

# Working directory. We are now in /code folder in docker server
WORKDIR /code

# Copying requirements.txt to /code folder
COPY ./requirements.txt /code/requirements.txt

# Configure server
# RUN pip install --upgrade pip

# Install packages mentioned in requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#  Copy all the file in /app folder to code folder
COPY ./app /code/app

# Command to run fast api app using uvicorn on the server. 
# You can run this "uvicorn app.main:app --host 0.0.0.0 --port 8500" directly in cmd prompt. Then go to localhost:8500/docs for API docs.
# To create and run container from cmd prompt after creating model-fastapi image => $ docker run -d --name myfastapicontainer -p 8500:8500 model-fastapi
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8500"]  

# If you want to deploy on Heroku, use below command. $PORT will be assigned by Heroku randomly.
# CMD uvicorn app.main:app --host 0.0.0.0 --port $PORT

#CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", $PORT]
