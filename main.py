import csv
from rac_entities import User, Machine
from pony.orm import *

@db_session
def add_csv_data():
    with open('all_users.csv', 'r') as f:
        csv_reader = csv.reader(f)
        next(csv_reader)

        user_dict = {}
        machine_set = set()
        machine_dict = {}

        for row in csv_reader:
            city = row[0]
            user = row[1]
            machine_list = [row[i] for i in [2, 4, 6] if row[i] != '']
            if user not in user_dict:
                user_dict[user] = {}
                user_dict[user]['machines'] = machine_list
                user_dict[user]['city'] = city

            if machine_list:
                for machine in machine_list:
                    machine_set.add(machine)

        # Create all Machine entity instances
        for machine in machine_set:
            machine_dict[machine] = Machine(name=machine)

        # Create all User entity instances
        for k, v in user_dict.items():
            User(name=k, city=user_dict[k]['city'],
                 machines=[machine_dict[machine] for machine in user_dict[k]['machines']])

@db_session
def test():
    machines = select(m for m in Machine)
    for m in machines:
        print(str(list(m.users.name._items_.keys())) + ' ' + m.name)

    dave = select(u for u in User if u.name == 'Dave McLinden').get()
    print(str(list(dave.machines.name._items_.keys())) + ' ' + dave.name)

    dave_machines = select(m for m in Machine if 'Dave McLinden' in m.users.name)
    for m in dave_machines:
        print('Dave\'s ' + m.name)


if __name__ == '__main__':
    db.bind(provider='sqlite', filename=':memory:')
    db.generate_mapping(create_tables=True)
    add_csv_data()
    test()

