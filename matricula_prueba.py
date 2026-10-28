from abc import ABC, abstractmethod

# Plantilla base para todas las matriculas
class IMatricula(ABC):
    @property
    @abstractmethod
    def estudiante(self) -> str:
        pass

    @abstractmethod
    def calcular_costo(self) -> float:
        pass

# Matricula normal inicial
class MatriculaGeneral(IMatricula):
    def __init__(self, estudiante: str):
        # Protegemos los datos con doble guion bajo para que no se editen desde afuera
        self.__estudiante = estudiante
        self.__monto_base = 60.00  

    @property
    def estudiante(self) -> str:
        return self.__estudiante

    @property
    def monto_base(self) -> float:
        return self.__monto_base

    def calcular_costo(self) -> float:
        return self.__monto_base

# Clase base que nos permite agregar recargos o descuentos a una matricula
class ModificadorMatricula(IMatricula):
    def __init__(self, matricula_envuelta: IMatricula):
        # Guardamos la matricula anterior protegida
        self.__matricula = matricula_envuelta

    @property
    def estudiante(self) -> str:
        # Pide el nombre a la matricula original
        return self.__matricula.estudiante

    @property
    def matricula(self) -> IMatricula:
        return self.__matricula

    @abstractmethod
    def calcular_costo(self) -> float:
        return self.__matricula.calcular_costo()

# Recargo por fuera de fecha
class MatriculaExtemporanea(ModificadorMatricula):
    def calcular_costo(self) -> float:
        # Trae el monto anterior y le suma 15 soles
        return super().calcular_costo() + 15.00

# Recargo por notas bajas
class MatriculaIndiceDesaprobatorio(ModificadorMatricula):
    def calcular_costo(self) -> float:
        # Trae el monto anterior y le suma 15 soles
        return super().calcular_costo() + 15.00

# Descuento por ser becario
class MatriculaBeca(ModificadorMatricula):
    def calcular_costo(self) -> float:
        # Trae el monto anterior y lo divide a la mitad
        return super().calcular_costo() / 2.0


# Pruebas de funcionamiento
if __name__ == "__main__":
    
    # Caso 1: Luis Huamani Cardenas
    # La beca se aplica al final, descontando sobre todo el dinero acumulado
    
    matricula_luis = MatriculaGeneral("Luis Huamani Cardenas")
    matricula_luis = MatriculaExtemporanea(matricula_luis)
    matricula_luis = MatriculaIndiceDesaprobatorio(matricula_luis)
    matricula_luis = MatriculaBeca(matricula_luis)
    
    print("Caso Luis - Beca aplicada al final:")
    print(f"Estudiante: {matricula_luis.estudiante}")
    print(f"Total a pagar: S/ {matricula_luis.calcular_costo():.2f}")
    
    print("\n------------------------------\n")

    # Caso 2: Rosa Ccahuana Prado
    # La beca se aplica primero (solo descuenta los 60 de base) y luego se suman los recargos enteros
    
    matricula_rosa = MatriculaGeneral("Rosa Ccahuana Prado")
    matricula_rosa = MatriculaBeca(matricula_rosa)
    matricula_rosa = MatriculaExtemporanea(matricula_rosa)
    matricula_rosa = MatriculaIndiceDesaprobatorio(matricula_rosa)
    
    print("Caso Rosa - Beca aplicada al inicio:")
    print(f"Estudiante: {matricula_rosa.estudiante}")
    print(f"Total a pagar: S/ {matricula_rosa.calcular_costo():.2f}")
