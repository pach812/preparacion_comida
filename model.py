import io
from typing import Annotated

from pandas import DataFrame
from pydantic import BaseModel, BeforeValidator, field_validator


class Porcion(BaseModel):
    nombres: str | list[str]
    porciones: int | list[int]

    @property
    def total(self):
        if isinstance(self.porciones, int):
            # Si es un valor único, simplemente devuelve ese valor
            return self.porciones
        elif isinstance(self.porciones, list):
            # Si es una lista, devuelve la suma de los valores
            return sum(self.porciones)
        else:
            # Manejar otros casos según sea necesario
            return None

    @field_validator("nombres")
    @classmethod
    def capitalize(cls, v: str | list[str]) -> list:
        if isinstance(v, str):
            return v.capitalize()
        return [i.capitalize() for i in v]

    def listar_elementos(self, dias: int = 7) -> str:
        proporcion = dias / 7
        if isinstance(self.nombres, list):
            if isinstance(self.porciones, list):
                return_string = ", ".join(
                    [
                        f"{self.porciones[i]*proporcion} gr de {self.nombres[i]}"
                        for i in range(len(self.nombres))
                    ]
                )
                return f"{return_string}"
            return_string = ", ".join(self.nombres)
            return f"{self.porciones*proporcion} gr de cualquiera de estos: {return_string}"

        else:
            return f"{self.porciones*proporcion} gr de {self.nombres}"


def porciones(valores: dict[str : list[str | int]]) -> Porcion:
    """recibe un diccionario con valores, elementos y valores para generar
    objeto porcion o lista de porciones."""
    if len(valores["elementos"]) == 1:
        return Porcion(nombres=valores["elementos"][0], porciones=valores["valores"][0])
    elif len(valores["valores"]) == 1:
        return Porcion(nombres=valores["elementos"], porciones=valores["valores"][0])
    else:
        return Porcion(nombres=valores["elementos"], porciones=valores["valores"])


porcion = Annotated[Porcion, BeforeValidator(porciones)]


class Perrito(BaseModel):
    nombre: str
    peso: float
    muscular: porcion
    visceral: porcion
    hueso: porcion
    arroz: porcion
    vegetales: porcion
    frutas: porcion
    total_semana: int = 0
    total_dia: float = 0

    def model_post_init(self, *args, **kwargs):
        self.total_semana = sum(
            [
                self.muscular.total,
                self.visceral.total,
                self.hueso.total,
                self.arroz.total,
                self.vegetales.total,
                self.frutas.total,
            ]
        )
        self.total_dia = round(self.total_semana / 7, 2)

    def display_info(self, dias: int = 7) -> str:
        with io.StringIO() as buffer:
            # Iterate through all attributes of the object that start with 'info_'
            for attr_name, attr_value in vars(self).items():
                if isinstance(attr_value, Porcion):
                    return_string = attr_value.listar_elementos(dias=dias)
                    buffer.write(f"{return_string}\n")

            # Get the concatenated string from the buffer
            concatenated_string = buffer.getvalue()
        return concatenated_string

    def get_items_dataframe(self, dias: int = 7) -> DataFrame:
        return_df = DataFrame(columns=["Listo?", "Clase", "Elemento", "Porcion"])
        ratio = dias / 7
        for attr_name, attr_value in vars(self).items():
            if isinstance(attr_value, Porcion):
                # Caso 1: Si el valor de la porcion es una lista
                if isinstance(attr_value.porciones, list):
                    for i in range(len(attr_value.porciones)):
                        new_row = {
                            "Listo?": False,
                            "Clase": attr_name.capitalize(),
                            "Elemento": attr_value.nombres[i],
                            "Porcion": f"{attr_value.porciones[i]*ratio:.2f} gr",
                        }
                        return_df.loc[len(return_df)] = new_row
                # Caso 2: Si el valor de la porcion es un valor único pero tiene una lista de nombres
                elif isinstance(attr_value.nombres, list):
                    new_row = {
                        "Listo?": False,
                        "Clase": attr_name.capitalize(),
                        "Elemento": ", ".join(attr_value.nombres),
                        "Porcion": f"{attr_value.porciones*ratio:.2f} gr",
                    }
                    return_df.loc[len(return_df)] = new_row
                else:
                    new_row = {
                        "Listo?": False,
                        "Clase": attr_name.capitalize(),
                        "Elemento": attr_value.nombres,
                        "Porcion": f"{attr_value.porciones*ratio:.2f} gr",
                    }
                    return_df.loc[len(return_df)] = new_row
        return return_df

    def proporciones_especificas(self):
        return {
            "muscular": round(self.muscular.total / self.total_semana, 2) * 100,
            "visceral": round(self.visceral.total / self.total_semana, 2) * 100,
            "hueso": round(self.hueso.total / self.total_semana, 2) * 100,
            "arroz": round(self.arroz.total / self.total_semana, 2) * 100,
            "vegetales": round(self.vegetales.total / self.total_semana, 2) * 100,
            "frutas": round(self.frutas.total / self.total_semana, 2) * 100,
        }

    def proporciones(self):
        return_string = f"""Proteina: {round((self.muscular.total + self.visceral.total + self.hueso.total)/ self.total_semana,2)*100}%
Carbohidratos: {round((self.arroz.total + self.vegetales.total + self.frutas.total )/ self.total_semana,2)*100}%"""
        return return_string
