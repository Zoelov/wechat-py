#!/usr/bin/env bash
cat >> /usr/local/apache2/conf/httpd.conf <<EOF
ServerName localhost:80
LoadModule wsgi_module modules/mod_wsgi.so
AddType text/html .py
WSGIScriptAlias / /data/wechat/wh/wsgi.py
WSGIPythonPath /data/wechat/wh/
<Directory /data/wechat/wh/>
    <Files wsgi.py>
        Require all granted
    </Files>
</Directory>
Alias /wechat/static/ /data/wechat/wechat/static/
<Directory /data/wechat/wechat/static/>
    Require all granted
</Directory>

EOF
service httpd start
python ../wechat/user.py &

chmod -R 777 /data/wechat/logs/

tail -f /var/log/messages



