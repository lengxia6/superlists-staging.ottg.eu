配置新网站
==========================

## 需要的包：


* nginx
* Python 3.6
* virtualenv + pip
* Git


以Ubuntu为例：

    sudo add-apt-repository ppa:fkrull/deadsnakes
    sudo apt-get install nginx git python3.6 python3.6-venv

## Nginx虚拟主机

* 参考nginx.template.conf
* 把SITENAME替换成所需要的域名，例如superlists-staging.ottg.eu

## Systemd服务

* 参考gunicorn-upstart.template.conf
* 把SITENAME替换成所需要的域名，例如superlists-staging.ottg.eu

## 文件夹结构
假设有用户账户，家目录为/home/username


/home/username
└── sites
    └── SITENAME
	├── database
	├── source
	├── static
	└── virtualenv


然后提交上述改动：

    $ git add deploy_tools
    $ git status # 看到3个新文件
    $ git commit -m "Notes and template config files for provisioning"

现在，源码的目录结构如下所示：

    .
    ├── deploy_tools
    │   ├── gunicorn-systemd.template.service
    │   ├── nginx.template.conf
    │   └── provisioning_notes.md
    ├── funcional_tests
    │   ├── [...]
    ├── lists
    │   ├── __init__.py
    │   ├── models.py
    │   ├── [...]
    │   ├── static
    │   │   ├── base.css
    │   │   └── bootstrap
    │   │   ├── [...]
    │   ├── templates
    │   │   ├── base.html
    │   │   ├── [...]
    │   ├── tests.py
    │   ├── urls.py
    │   └── views.py
    ├── manage.py
    ├── requirements.txt
    └── superlists
        ├── [...]
































