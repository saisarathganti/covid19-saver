# UI

>A corona monitoring application written in Python powered by Vue, Flask and Neo4j which will alert users if they were exposed to any infected
person and let them know to take precautions
---

## Build Setup

``` bash
# clone project
git clone "frontend url"

# install vue cli
npm install -g @vue/cli

# init webpack and use default settings
vue init webpack ui

cd ui

# install virtualenv
pip install virtualenv

# initialize virtual environment
virtualenv venv

# activate venv
source venv/bin/activate

#replace the src folder and files in ui with src folder and files in covid-front-end

# install dependencies
npm install

# serve with hot reload at localhost:8080
npm start
```
