#
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Universidad EAN (Bogotá - Colombia)
# Departamento de Sistemas
# Faculta de Ingeniería
#
# Proyecto EAN Python Collections
# @author Luis Cobo (lacobo@universidadean.edu.co)
# Fecha: Mar 09 2026
# Versión: 0.0.1 -> 16 de febrero de 2026 -> Implementación inicial
# Versión: 0.0.2 -> 09 de febrero de 2026 -> Implementación de nodos
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
import math
from datetime import datetime
from math import sqrt, pi

# Definición de elementos genéricos que usaremos a continuación
from typing import TypeVar, Generic

# La clase Nulo: representa un nodo nulo
class Nulo:
    def __init__(self):
        pass

    def __str__(self):
        return "nulo"

    def __repr__(self):
        return "Nulo()"

    def __getattr__(self, nombre: str):
        raise AttributeError(f"El atributo {nombre} no existe en el nodo nulo")

    def __eq__(self, otro: object) -> bool:
        if otro is None:
            raise ValueError("El valor nulo no puede ser comparado con None")
        return isinstance(otro, Nulo)

    def __ne__(self, otro: object) -> bool:
        if otro is None:
            raise ValueError("El valor nulo no puede ser comparado con None")
        return not self.__eq__(otro)

    @property
    def es_nulo(self) -> bool:
        return True

    @property
    def no_es_nulo(self) -> bool:
        return False        

# ----------------------------------------

# Variable global que representa el valor nulo.
nulo = Nulo()

# ------------------------------------------------------------

T = TypeVar('T')

# Los nodos son objetos que permiten almacenar información
# Cada nodo contiene un atributo llamado "información"
# y otro llamado "sig".
class Nodito(Generic[T]):
    def __init__(self, informacion : T):
        self.__informacion = informacion
        self.__siguiente  = nulo
        if informacion is None or informacion == nulo:
            raise ValueError("El valor nulo no puede ser almacenado en un nodo")

    @property
    def es_nulo(self) -> bool:
        return False

    @property
    def no_es_nulo(self) -> bool:
        return True

    @property
    def informacion(self) -> T:
        return self.__informacion

    @informacion.setter
    def informacion(self, valor: T):
        if valor is None or valor == nulo:
            raise ValueError("El valor nulo no puede ser almacenado en un nodo")
        self.__informacion = valor

    @property
    def sig(self) -> 'Nodito | Nulo':
        return self.__siguiente

    @sig.setter
    def sig(self, sig: 'Nodito | Nulo'):
        if sig is None:
            raise ValueError("En este curso nunca usamos None con Noditos. Revise la presentación")
        self.__siguiente = sig

    def __getattr__(self, attr : str):
        raise AttributeError(f"El atributo {attr} no existen en los noditos.\nEn este curso un nodito solo tiene informacion y sig.")

    def __eq__(self, otro: object) -> bool:
        if otro is None:
            raise ValueError("Un nodito no puede ser comparado con None. Uso nulo en su lugar")
        return isinstance(otro, Nodito) and self.informacion == otro.informacion

    def __ne__(self, otro: object) -> bool:
        if otro is None:
            raise ValueError("Un nodito no puede ser comparado con None. Use nulo en su lugar")
        return not self.__eq__(otro)

    def __setattr__(self, attr : str, valor: object):
        if attr == "data" or attr == "value" or attr == "next" or attr == "siguiente" or attr == "valor" or attr == "info" or attr == "dato":
            raise AttributeError(f"El atributo {attr} no existe en los noditos.\nEn este curso un nodito solo tiene informacion y sig.")
        super().__setattr__(attr, valor)

    def __str__(self):
        return f"{str(self.informacion)} -> {str(self.sig)}"


# ---------------------------------------------------------------------
import pandas as pd
from dataclasses import dataclass

@dataclass(frozen=True)
class Persona:
    """
    Clase que representa una persona
    """

    # Atributos de la clase Persona
    cedula: int
    nombre: str
    edad: int
    genero: str
    num_hijos: int
    nivel_educativo: str
    estrato: int
    ingresos: int
    peso: int
    altura: int
    fuma: bool
    usa_lentes: bool
    tiene_casa: bool
    tiene_carro: bool

    # Métodos de la clase persona
    def año_nacimiento(self) -> int:
        return datetime.now().year - self.edad

    def peso_ideal(self) -> float:
        return (self.altura - 100) * 0.9

    def imc(self) -> float:
        return self.peso / (self.altura / 100) ** 2

# ---------------------------------------------
def crear_lista_nodos_personas() -> Nodito[Persona]:
    """
    Permite crear una lista con las personas que están
    en el archivo
    :return: la lista con las personas
    """
    archivo = "https://github.com/luiscobo/poo/raw/refs/heads/main/people.csv"
    df = pd.read_csv(archivo, sep=";", encoding="utf-8")

    cabeza  = nulo
    actual  = nulo

    for index, row in df.iterrows():
        cedula = row["Cedula"]
        nombre = row["Nombres"].upper()
        edad = row["Edad"]
        genero = row["Genero"]
        num_hijos = row["No de hijos"]
        nivel_educativo = row["Nivel Educativo"]
        estrato = row["Estrato Socio"]
        ingresos = row["Ingresos"]
        peso = row["Peso"]
        altura = row["Talla"]
        fuma = row["Fuma"] == "SI"
        usa_lentes = row["Usa Lentes"] == "SI"
        tiene_casa = row["Tiene Casa"] == "SI"
        tiene_carro = row["Tiene Automovil"] == "SI"
        p = Persona(cedula, nombre, edad, genero, num_hijos, nivel_educativo, estrato, ingresos, peso, altura, fuma, usa_lentes, tiene_casa, tiene_carro)
        nodo = Nodito[Persona](p)
        if cabeza is nulo:
            cabeza = nodo
            actual = nodo
        else:
            actual.sig = nodo
            actual = nodo
    return cabeza

# ---------------------------------------------------------------------
def crear_lista_nodos_equipos() -> Nodito:
    """
    Permite crear una lista con los equipos de fútbol que están
    en el archivo
    :return: la cabeza de una lista de nodos con equipos
    """
    archivo = "https://raw.githubusercontent.com/luiscobo/poo/refs/heads/main/LaLiga.csv"
    df = pd.read_csv(archivo, encoding="utf-8")

    cabeza = nulo
    actual = nulo
    
    for index, row in df.iterrows():
        año = int(row["season"][:4])
        nombre = row["club"]
        partidos_ganados_local = int(row["home_win"])
        partidos_ganados_visitante = int(row["away_win"])
        partidos_perdidos_local = int(row["home_loss"])
        partidos_perdidos_visitante = int(row["away_loss"])
        partidos_empatados = int(row["matches_drawn"])
        goles_local = int(row["home_goals"])
        goles_visitante = int(row["away_goals"])
        goles_en_contra = int(row["goals_conceded"])
        e = (año, nombre, partidos_ganados_local, partidos_ganados_visitante,
                         partidos_perdidos_local, partidos_perdidos_visitante,
                         partidos_empatados, goles_local, goles_visitante,
                         goles_en_contra)
        nodo = Nodito(e)
        if cabeza is nulo:
            cabeza = nodo
            actual = nodo
        else:
            actual.sig = nodo
            actual = nodo
        
    return cabeza

# ---------------------------------------------------------------------
@dataclass(frozen=True)
class Departamento:
    """
    Clase que representa la información de un departamento de Colombia
    """
    nombre: str
    cant_municipios: int
    capital: str
    superficie: float
    poblacion: int
    densidad: float
    indice_desarrollo_humano: float
    fecha_creacion: int
    region: str

# ---------------------------------------------------------------------
def crear_lista_nodos_departamentos() -> Nodito[Departamento] | Nulo:
    """
    Permite obtener una lista de departamentos a partir del archivo
    de datos que se encuentra en github
    :return: Una lista con la información de los departamentos
    """
    archivo = "https://raw.githubusercontent.com/luiscobo/poo/refs/heads/main/departamentos2.csv"
    df = pd.read_csv(archivo, encoding="utf-8")
    cabeza = nulo
    actual = nulo
    for index, row in df.iterrows():
        nombre = row["Departamento"]
        municipios = row["Municipios"]
        capital = row["Capital"]
        superficie = row["Superficie"]
        poblacion = row["Población"]
        densidad = row["Densidad"]
        idh = row["IDH6"]
        fecha = row["Fecha de creación"]
        region = row["Región"]
        depto = Departamento(nombre, cant_municipios=municipios, capital=capital, superficie=superficie,
                             poblacion=poblacion, densidad=densidad, indice_desarrollo_humano=idh, fecha_creacion=fecha,
                             region=region)
        nodo = Nodito[Departamento](depto)
        if cabeza is nulo:
            cabeza = nodo
            actual = nodo
        else:
            actual.sig = nodo
            actual = nodo
    return cabeza

# ----------------------------------------------------------------------------------------

def obtener_nodo_pos(cab : Nodito, indice : int) -> Nodito | Nulo:
    """
    Permite obtener el nodo ubicado en una determinada posición
    :param cab: el primer nodo de la lista
    :param indice: la posición que se desea obtener
    :return: el nodo ubicado en la posición especificada por indice
    """
    act = cab
    for i in range(indice):
        act = act.sig
    return act
    

    
