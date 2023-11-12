# Python-15-Factor-App

`python-15-factor-app` is a Python application that serves as a practical example of implementing the 15 Factor App methodology. This methodology is designed to create efficient, scalable, and maintainable software applications.

## Getting Started

### Prerequisites
- Python
- Pipenv
- Docker & Docker Compose

### Installation
1. **Clone the Repository**
   ```bash
   git clone https://github.com/Scaleups-cloud/python-15-factor-app.git

### Install Dependencies
1. **Install Pipenv**
   ```bash
   pipenv install
   ```
### Setting Up the Environment
* Use docker-compose along with the .env file to set up the environment and database (PostgreSQL).

### Accessing Application
* **Swagger Specification:** Access the Swagger UI for API documentation at http://127.0.0.1:5000/swagger/
* **Metrics:** Access application metrics at http://127.0.0.1:5000/metrics

### Running Tests
* Execute tests using the following command:
```bash
python -m unittest discover -s tests
```
### Authentication and Authorization
* Use the token generated from the authentication process to access APIs.
* Authorization details, especially for admin roles, can be found in the init_script.

License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/Scaleups-cloud/python-15-factor-app/blob/main/LICENSE) file for details.




