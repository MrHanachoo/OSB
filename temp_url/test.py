__author__ = 'med'

from temp_url_generator import Container, Generator


cont = Container()
cont_list = cont.list_containers()
chosen_cont = cont.chosen_container(cont_list)
objects = cont.list_objects(chosen_cont)

url_gen = Generator(chosen_cont, 'GET', '60')
data = url_gen.get_data()
storage_url = data[0]
account = data[1]
auth_token = data[2]
key = data[3]
print data
host = url_gen.get_host(storage_url, account)
url_gen.generate(host, url_gen.method, url_gen.seconds, account, chosen_cont, objects, key)