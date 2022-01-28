# install goodies
dnf update -y
dnf install -y nginx

dnf install -y python38
pip3.8 install fastapi
pip3.8 install hypercorn
pip3.8 install psycopg2-binary
pip3.8 install jinja2
pip3.8 install requests
pip3.8 install pytest