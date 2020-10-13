# API

>A corona monitoring application written in Python powered by Vue, Flask and Neo4j which will alert users if they were exposed to any infected
person and let them know to take precautions
---

## Build Setup

``` bash
# clone project
git clone "backend url"

# Add the repository key to our keychain for installing neo4j
wget --no-check-certificate -O - https://debian.neo4j.org/neotechnology.gpg.key | sudo apt-key add -

# Add the repository to the list of apt sources.
echo 'deb http://debian.neo4j.org/repo stable/' | sudo tee /etc/apt/sources.list.d/neo4j.list

# Update the repository information and install Neo4j
sudo apt update
sudo apt install neo4j

# You should now be able to access the database server via http://localhost:7474/browser/
sudo service neo4j start
$ export NEO4J_USERNAME=username
$ export NEO4J_PASSWORD=password

cd covid-tracker-backend

# install virtualenv
pip install virtualenv

# initialize virtual environment
virtualenv venv

# activate venv
source venv/bin/activate

# install all requirements and makesure to have py2neo V4 and latest neo4j
pip install -r requirements.txt

# run python file
python run.py
```
