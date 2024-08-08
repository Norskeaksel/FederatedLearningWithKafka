# Federated Learning with Kafka

## Setup
0. git clone https://github.com/Norskeaksel/FederatedLearningWithKafka.git; cd FederatedLearningWithKafka
1. Make a virtual environment with: python -m venv env  
2. Activate with: source env/bin/activate on linux, env\Scripts\activate on windows.  
DON'T try to run the source command on windows with git bash! It can mess up your envirornment.
3. pip install -r requirements. txt

## Running with local kafka cluster
0. Install and run docker desktop
1. docker compose up -d  
2. python produce_initial_recommender_weights.py  
3. python controller.py <<< "local" Only have ONE controller active at the time!
4a. python client.py <<< "local" with bash  
4b. python client.py and manually enter "local" with powershell  
5. To run with 3 clients at the same time, run this command in bash  
python client.py <<<"local" & python client.py <<<"local" & python client.py <<<"local" &

## Running with confluent kafka cluster 
1.  Rename the [cloud_client_dummy.properties](kafkaLogic/config/cloud_client_dummy.properties) 
file to "cloud_client.properties" and get the sasl username and password from Aksel  
2. python controller.py <<< "cloud" Only have ONE controller active at the time!  
3a. python client.py <<< "cloud" with bash  
3b. python client.py and manually enter "cloud" with powershell  
4. To run with 3 clients at the same time, run this command in bash  
python client.py <<<"cloud" & python client.py <<<"cloud" & python client.py <<<"cloud" &