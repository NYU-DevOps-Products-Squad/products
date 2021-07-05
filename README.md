# products
Repo for the products team or NYU DevOps 2021 summer

## Prerequisite Installation using Vagrant VM

Initiating a development environment requires  **Vagrant** and **VirtualBox**. if you don't have this software the first step is down download and install it.

Download [VirtualBox](https://www.virtualbox.org/)

Download [Vagrant](https://www.vagrantup.com/)

Then all you have to do is clone this repo and invoke vagrant to start:

```bash
    git clone https://github.com/Devops-2020-Products/products
    cd products
    vagrant up
    vagrant ssh
    cd /vagrant
    ...
```


## Structure of the repo

```
├── service
│   ├── models.py
│   └── routes.py
├── tests
│   ├── factories.py
│   ├── test_models.py
│   └── test_routes.py
```

### Database  Fields
| Fields | Type | Description
| :--- | :--- | :--- |
| id | String | ID 
| name | String | Product Name
| description | String | Product Description
| price | Float | Product Price
| inventory | Int | Product Amount
| Owner | String | OwnerID
| Category | String | Product Category|

## Vagrant shutdown

When you are done, you should exit the virtual machine and shut down the vm with:

```bash
 $ exit
 $ vagrant halt
```

If the VM is no longer needed you can remove it with:

```bash
  $ vagrant destroy
```
