# Itri_Dev    ![Python package](https://github.com/ryany45/Itri_Dev/workflows/Python%20package/badge.svg?branch=preview)

太陽光電達標管考系統


## Installation
### 1. for flask web service only
1. Create a Virtual Environment
    ```cmd
    python -m venv (your environment name)
    ```
2. Activate the  Environment
    * for Windows
    ```cmd
    (Folder Directory)\(Your Environment Folder)\Scripts\activate
    ```
    * for Linux

    ```cmd
    source (Folder Directory)\(Your Environment Folder)/bin/activate
    ```
3. Install the library required
    Use the package manager [pip](https://pip.pypa.io/en/stable/) to install all the requirement.
    Go to the root folder of this project, and run the following command
    ```cmd
    pip install -r requirements.txt
    ```
4. Run the server:
    To normally run the server, execute following
    ```cmd
    python manage.py runserver #server will be run at 127.0.0.1:5000
    ```

    Custom server ip address
    ```cmd
    python manage.py runserver -h (ip address)
    ```

    Custom server port address
    ```cmd
    python manage.py runserver -p (port number)
    ```

5. Remove the pycache:
    ```cmd
    find . | grep -E "(__pycache__|\.pyc|\.pyo$)" | xargs rm -rf
    ```
 
## 2. Run the Itri_Dev web service in Gunicorn and Nginx
In the production environment, it's best for us to deploy the Flask web service in a **WSGI Server** to achieve **handling multi requests**

Although Flask web service can achieve mutli process one way or another by using
```python
app.run(threaded = true)
```
it's a single threaded application using scheduling to achieve multi threaded
so of course the performance won't even come close to a multi threaded framework

so first We will use [Gunicorn](https://gunicorn.org/), a WSGI server to handle multi request.

The Gunicorn will operate as the following:
![](https://i.imgur.com/s1DRjhr.png)

The Wsgi server is controlled by a Master Process called **Supervisor**
This process will actually open a socket and listen to the certain port for request
If a request is coming, the Supervisor will start a worker with our **Itri_Dev** Flask web service to process the request and send the responce to the user

#### And also a **reverse proxy server** is optimal
the reverse proxy server is used for buffering the request
so the **WSGI server** like **Gunicorn** will not be flooded by the numerous amount of requests

The reverse proxy server we use will be [Nginx](https://www.nginx.com/), a lightweight powerful server.
The structure now will be like:
![](https://i.imgur.com/0n5KUPo.png)


### Installation and deploy of Gunicorn with Itri_Dev
So, in the default requirements.txt, it will contain the installation of **Gunicorn** 
but if the installation is failed somehow, you can just installed it using:
```cmd
pip install gunicorn
```
**Noted: Install it in the virtual environment is recommended**
Once the library is included, make sure there is a **wsgi.py** in the project root folder
But if the file is not exist, you can create it by using
```cmd
sudo nano (path to)/Itri_Dev/wsgi.py
```
and paste the following content in the wsgi.py
```python
from module import app

if __name__ == "__main__":
    app.run()
```
 
You can test it to see the Gunicorn work using:
```cmd
gunicorn --bind 0.0.0.0:5000 wsgi:app
```
The output should be look like the following:
```cmd
[28217] [INFO] Starting gunicorn 22.2.0
[28217] [INFO] Listening at: http://0.0.0.0:5000 (28217)
[28217] [INFO] Using worker: sync
[28220] [INFO] Booting worker with pid: 28220
```
The Itri_Dev will supposely run on localhost:5000
<hr>

Now let's register gunicorn as systemd service,
so we don't have to go back and force with the virtual environment every time 

Input the following command
```cmd
sudo nano /etc/systemd/system/Itri_Dev.service
```

In the content paste the following
```cmd
[Unit]
Description=Gunicorn instance to serve Itri_Dev
After=network.target

[Service]
User= <the user in the server you are hosting>
Group=www-data
WorkingDirectory=<path to the Itri_Dev folder>
Environment="PATH= <path to the venv folder for Itri_Dev> "
ExecStart= <path to the venv folder for Itri_Dev>/gunicorn --workers 3 --bind unix:Itri_Dev.sock -m 007 wsgi:app

[Install]
WantedBy=multi-user.target
```
Once you are done, save and close it

You now can start and enable the gunicorn service by
```cmd
sudo systemctl start Itri_Dev
sudo systemctl enable Itri_Dev
```

and you can also check the service status by:
```cmd
sudo systemctl status Itri_Dev
```
The output should be the following
```cmd
● Itri_Dev.service - Gunicorn instance to serve Itri_Dev
   Loaded: loaded (/etc/systemd/system/Itri_Dev.service; disabled; vendor preset: enabled)
   Active: active (running) since 日 2020-02-16 16:41:58 CST; 5s ago
 Main PID: 26890 (gunicorn)
    Tasks: 4
   Memory: 113.5M
      CPU: 565ms
   CGroup: /system.slice/Itri_Dev.service
           ├─26890 /home/netlab/Brian(virus_inside)/Itri_Dev_beta/itri_env/bin/python3.7 /home/netlab/Brian(virus_inside)/Itri_Dev_beta/itri_env/bin/gunicorn --workers 3 --bind unix:Itri_Dev.sock -m 007 wsgi:ap
           ├─26909 /home/netlab/Brian(virus_inside)/Itri_Dev_beta/itri_env/bin/python3.7 /home/netlab/Brian(virus_inside)/Itri_Dev_beta/itri_env/bin/gunicorn --workers 3 --bind unix:Itri_Dev.sock -m 007 wsgi:ap
           ├─26910 /home/netlab/Brian(virus_inside)/Itri_Dev_beta/itri_env/bin/python3.7 /home/netlab/Brian(virus_inside)/Itri_Dev_beta/itri_env/bin/gunicorn --workers 3 --bind unix:Itri_Dev.sock -m 007 wsgi:ap
           └─26911 /home/netlab/Brian(virus_inside)/Itri_Dev_beta/itri_env/bin/python3.7 /home/netlab/Brian(virus_inside)/Itri_Dev_beta/itri_env/bin/gunicorn --workers 3 --bind unix:Itri_Dev.sock -m 007 wsgi:ap

 2月 16 16:41:58 netlab-MS-7B12 systemd[1]: Started Gunicorn instance to serve Itri_Dev.
 2月 16 16:41:58 netlab-MS-7B12 gunicorn[26890]: [2020-02-16 16:41:58 +0800] [26890] [INFO] Starting gunicorn 20.0.4
 2月 16 16:41:58 netlab-MS-7B12 gunicorn[26890]: [2020-02-16 16:41:58 +0800] [26890] [INFO] Listening at: unix:Itri_Dev.sock (26890)
 2月 16 16:41:58 netlab-MS-7B12 gunicorn[26890]: [2020-02-16 16:41:58 +0800] [26890] [INFO] Using worker: sync
 2月 16 16:41:58 netlab-MS-7B12 gunicorn[26890]: [2020-02-16 16:41:58 +0800] [26909] [INFO] Booting worker with pid: 26909
 2月 16 16:41:58 netlab-MS-7B12 gunicorn[26890]: [2020-02-16 16:41:58 +0800] [26910] [INFO] Booting worker with pid: 26910
 2月 16 16:41:58 netlab-MS-7B12 gunicorn[26890]: [2020-02-16 16:41:58 +0800] [26911] [INFO] Booting worker with pid: 26911
```

### Installation and Deployment of Nginx
#### The installation of Nginx
```cmd
sudo apt-get update  
apt-get install nginx 
```

#### Editing the site_available
```cmd
sudo nano /etc/nginx/sites-available/Itri_Dev
```
Paste the following content
```cmd
server {
    listen <the port you want to open>;
    server_name 0.0.0.0;

    location / {
        include proxy_params;
        proxy_pass http://unix:<path to Itri_Dev folder>/Itri_Dev/Itri_Dev.sock;
    }
}
```
Close and save it

copy the config file to site-enabled using
```cmd
sudo ln -s /etc/nginx/sites-available/Itri_Dev /etc/nginx/sites-enabled
```

to test the syntax you can use 
```cmd
sudo nginx -t
```

Now you can start the **Nginx** service to listen for request using:
```cmd
sudo systemctl restart nginx
```

Also allow full access to the Nginx server
```cmd
sudo ufw allow 'Nginx Full'
```

## Usage
If you need to open the full service
```cmd
sudo systemctl start Itri_Dev
sudo systemctl restart Nginx
```

You can check the service status
```cmd
sudo systemctl status Itri_Dev
sudo systemctl status Nginx
```

If you want to check the error log:
```cmd
sudo less /var/log/nginx/error.log
sudo less /var/log/nginx/access.log
sudo journalctl -u nginx
sudo journalctl -u Itri_Dev
```

## structure
    itriDev/  
        module/  
            edit/  
                __init__.py  
                controller.py  
            search/  
                __init__.py  
                controller.py  
            upload/  
                __init__.py  
                controller.py 
            control/  
                __init__.py  
                controller.py 
            __init__.py  
            templates/  
            static/  
        util/  
        manage.py  
        wsgi.py
        requirements.txt  
