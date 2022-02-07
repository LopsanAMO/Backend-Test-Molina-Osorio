# Cornershop Test

Cornershop Test. Check out the project's [documentation](http://ec2-54-71-45-249.us-west-2.compute.amazonaws.com:8001/).

[![Run in Postman](https://run.pstmn.io/button.svg)](https://app.getpostman.com/run-collection/b9555e7e412740e39c1a?action=collection%2Fimport)

# Prerequisites

- [Docker](https://docs.docker.com/docker-for-mac/install/)

- [Unierse a slack](https://join.slack.com/t/corner-testespacio/shared_invite/zt-tfxesdh1-RvHNTAVEEjsUDmXNxD4PpA) ```https://join.slack.com/t/corner-testespacio/shared_invite/zt-tfxesdh1-RvHNTAVEEjsUDmXNxD4PpA```

# Initialize the project

Copie the .env.sample file to a new file called .env.

```bash
cp .env.sample .env
```
update the .env entries to real values:

```bash
DB_NAME=postgres
DB_USER=postgres
DB_PASS=postgres
SECRET_KEY=AUniqueSecretKey
ALLOWED_HOSTS=*
SLACK_API_KEY=xxx-xxxxxxx
```

Start the dev server for local development:

```bash
docker-compose up
```

Create a superuser to login to the admin:

```bash
docker-compose run --rm web ./manage.py createsuperuser
```

# Documentation

[API Documentation](http://ec2-54-71-45-249.us-west-2.compute.amazonaws.com:8001/)  ```http://ec2-54-71-45-249.us-west-2.compute.amazonaws.com:8001/```

[Swagger Schema](http://ec2-54-71-45-249.us-west-2.compute.amazonaws.com/api/schema/swagger-ui/) ```http://ec2-54-71-45-249.us-west-2.compute.amazonaws.com/api/schema/swagger-ui/```

[Running Proyect](http://ec2-54-71-45-249.us-west-2.compute.amazonaws.com/admin) ```http://ec2-54-71-45-249.us-west-2.compute.amazonaws.com/admin```

### Admin User

User: ```nora```

Password: ```cornershop```