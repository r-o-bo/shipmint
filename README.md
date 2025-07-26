
#  Shipmint

Shipmint is a Dockerized Python data querying and export tool built for running analytical SQL queries on the [dvdrental](https://www.postgresqltutorial.com/postgresql-sample-database/) dataset. It connects to a PostgreSQL database, executes pre-defined queries, and exports the results to CSV files.

This project includes a working **Continuous integration pipeline** using GitHub Actions that builds and pushes a Docker image to **Azure Container Registry**.

---

##  Project Structure

```bash
.
├── .github/workflows/ci.yml     
├── .dockerignore
├── Dockerfile                          
├── flyingnimbus.py              
├── requirements.txt
└── README.md
```


---

## ⚙️ Features

* Connects to a remote PostgreSQL database using `psycopg2`
* Executes complex SQL queries on the dvdrental dataset
* Exports query results to CSV using the `csv` module
* Dockerized 
* Continuous Integration pipeline via GitHub Actions

---

##  Setup

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/shipmint.git
cd shipmint
```

### 2. Create a `.env` file

```env
DB_HOST=your_postgres_host
DB_NAME=dvdrental
DB_USER=your_username
DB_PASSWORD=your_password
```

---

## 🐳 Running with Docker

```bash
docker build -t flying-nimbus .
docker run --env-file .env flying-nimbus
```

---

## ✅ CI Pipeline (GitHub Actions)

Every push to `master` triggers a GitHub Actions workflow to:

1. Log into Azure Container Registry (ACR)
2. Build the Docker image
3. Push the image to your ACR repository

> You'll need to add these secrets in your repository:

* `ACR_LOGIN_SERVER`
* `ACR_USERNAME`
* `ACR_PASSWORD`

---

##  Future Scope

* Plan to add Continuous **Delivery** to Azure Container Instances 
* Logging and monitoring
* Unit testing and pre-commit linting

---
## 📜 License
This project is licensed under the MIT License.

```
