# Annotation_tools

This repository explains overall process for using annotation tools.

We will see how to annotate person key points with annotation tools.



### Setup

1. Clone annotation tools repository on your home directory

```
cd /home/ubuntu
git clone https://github.com/visipedia/annotation_tools.git
```

2. Use virtual environment

```
mkvirtualenv py2 --python=python2
```

3. Install the python requirements

```
cd /home/ubuntu/annotation_tools
pip install -r requirements.txt
```

4. Install MongoDB

```\
sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 2930ADAE8CAF5059EE73BB4B58712A2291FA4AD5

echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu xenial/mongodb-org/3.6 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-3.6.list

sudo apt update
sudo apt install -y mongodb-org


sudo systemctl start mongod.service

sudo systemctl status mongod
```

** If you need to remove MongoDB **

```
sudo systemctl stop mongod.service

sudo apt purge mongodb-org*

sudo rm -r /var/log/mongodb
sudo rm -r /var/lib/mongodb
```



### Create files

1. Create json file with python 

```
cd /home/ubuntu/annotation_tools
python person.py
```

2. Start the web server to serve the images

```
cd /home/ubuntu/images
python -m SimpleHTTPServer 6008

http://localhost:6008/
```



### Import the Dataset

```
cd /home/ubuntu/annotation_tools
python run.py --port 8008
```

```
I added one line in 'annotation_tools.py'
(/home/ubuntu/annotation_tools/annotation_tools/annotation_tools.py)

app.config["MONGO_URI"] = "mongodb://localhost:27017/mydatabase"
** mydatabase is db_name
```

```
cd /home/ubuntu/annotation_tools
python -m annotation_tools.db_dataset_utils --action load \
--dataset /home/ubuntu/input.json
```



### Edit image

```
http://localhost:8008/edit_image/image_name
http://localhost:8008/edit_task/?start=0&end=100
```



### Export the Dataset

```
python -m annotation_tools.db_dataset_utils --action export \
--output /home/ubuntu/output.json --denormalize
```

