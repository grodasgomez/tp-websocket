from data.db import *
def see_state(data):
    print('see_state')
    print(getAll())


def create_bed(data):
    print('create_bed')


def delete_bed(data):
    print('delete_bed')


def occupy_bed(data):
    print('occupy_bed')


def vacate_bed(data):
    print('vacate_bed')


# Creamo nuestro diccionario de las funciones que manejaran cada operacion
HANDLERS = {1: see_state, 2: create_bed,
            3: delete_bed, 4: occupy_bed, 5: vacate_bed}
