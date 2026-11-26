from operaciones import sumar
from operaciones import mayor_de_tres

def test_sumar():

    resultado = sumar(2,3)

    assert resultado == 5


def test_sumarUnaResta():

    resultado = sumar (-2, 5)

    assert resultado == 3


def test_sumar3():

    resultado = sumar(10, 5)

    assert resultado == 15


def test_sumar4():

    resultado = sumar(0, 10)

    assert resultado == 10


# ---------------------------

def test_mayordetres1():

    resultado = mayor_de_tres(1, 2, 3)

    assert resultado == 3


def test_mayordetres2():

    resultado = mayor_de_tres(1, 3, 2)

    assert resultado == 3


def test_mayordetres3():

    resultado = mayor_de_tres(3, 1, 2)

    assert resultado == 3

def test_mayordetres4():

    resultado = mayor_de_tres(-5, 5, 6)

    assert resultado == 6


def test_mayordetres1():

    resultado = mayor_de_tres(5, 5, 5)

    assert resultado == 5

