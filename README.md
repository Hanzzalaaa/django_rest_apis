# django_rest_apis with swagger documentation

I'm sharing with you the postman api collection


https://api.postman.com/collections/31238669-dae97e70-7828-4def-a9d6-9f657f1f32e1?access_key=PMAT-01HKDH7ZH232W9F84RHR4AB0AE

open postman click on import button and then paste above key there

i make for you signup,signin,reset password (means you hit this api you enter email of your token send to your email with confirm reset api endpoint)
note im using smtp service for sending token to email but when i go to sendgrid to make testing for the test it does not allow to login me so i check properly you just need to go to settings.py file and just replace 
EMAIL_HOST_USER = 'user you make of any smtp service'
EMAIL_HOST_PASSWORD = 'password of your smtp account'
after this reset password work properly
your requirements fullfilled when you check postman collection


Clone the repository:

git clone git@github.com:asadraza-69/dockerized_backend_api.git

localenviroment

Creating env and activating env :

python3 -m venv docker_backend_env
source bin\activate

Navigate to the project directory:

cd dockerized_backend_api

Install the project dependencies:

pip install -r requirements.txt

Apply migrations: uncomment DB_LOCALHOST from settings

python manage.py migrate

Applying fixtures:

python manage.py loaddata initial_data

Start the development server:

python manage.py runserver



dockerenviroment

First run this command for update your os dependencies:

sudo apt-get update

Fetches the Docker package from the repositories and installs it on your system:

sudo apt install docker.io

Download and install the Docker package from the Snap Store, which is a central repository for snap packages:

sudo snap install docker

Docker version:

docker --version

Download and run any docker image/container:

docker pull postgres
sudo docker run (image name)

Available docker image/container in your system:

sudo docker ps -a

Install all dependencies in your Docker that your project need:

sudo docker build -t myapp .

Command to build docker-compose file:

sudo docker-compose up --build

you check all images in your system:

sudo docker ps -a

output:
CONTAINER ID           IMAGE                       COMMAND                  CREATED          STATUS                      PORTS     NAMES
9ff0241e7711     django_project_lambda-web   "bash -c 'python man…"   19 seconds ago   Exited (1) 16 seconds ago                myapp

For restart the docker container run this command:

sudo docker-compose restart

If you want to stop the running docker container run this command:

sudo docker-compose down

If you want to start docker container run this command:

sudo docker-compose up


