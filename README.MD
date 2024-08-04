# Federated lerning with kafka

## Setup
1. Make a virtual environment with: python -m venv env
2. Activate with: source env/bin/activate on linux, env\Scripts\activate on windows
3. pip3 install confluent-kafka

## Running with local kafka cluster
1. docker compose up -d
2a. python client.py <<< "local" with bash
2b. python client.py and manually enter "local" with powershell

## Running with confluent kafka cluster 
1. Accuire the client.properties file from Aksel
2a. python client.py <<< "cloud" with bash
2b. python client.py and manually enter "cloud" with powershell
