import streamlit as st

from data import maggie_data, pandora_data
from model import Perrito

maggie = Perrito(**maggie_data)
pandora = Perrito(**pandora_data)

perrito_database = {"Maggie": maggie, "Pandora": pandora}
st.header("Preparacion de alimentos caninos")


preparacion_tab, info_tab = st.tabs(["Preparacion", "Informacion Semanal"])

with preparacion_tab:
    st.write("Aqui va la preparacion de alimentos")
    option = st.selectbox(
        "Seleccione un perrito", [maggie.nombre, pandora.nombre], key="preparacion"
    )
    if option:
        perrito = perrito_database[option]
        col1, col2 = st.columns(2)
        dias_preparar = col1.number_input(
            "Dias a preparar", min_value=1, max_value=14, value=7
        )
        porciones_diarias = col2.number_input(
            "Porciones diarias", min_value=1, max_value=3, value=1
        )
        st.data_editor(
            perrito.get_items_dataframe(dias_preparar),
            use_container_width=True,
            hide_index=True,
            disabled=["Clase", "Elemento", "porcion"],
        )
    dosis_diaria = perrito.total_dia / porciones_diarias
    col1, col2 = st.columns(2)
    col1.write(f"Dosis diaria: {dosis_diaria:.2f} gr")
    col1.write(f"Dosis semanal: {perrito.total_semana:.2f} gr")
    col2.write(
        f"Proporciones entre proteina y carbohidratos\n\n{perrito.proporciones()}"
    )
    st.write("----")
    with st.expander("Como usarlo?", expanded=False):
        st.write("1. Selecciona un perrito")
        st.write("2. Selecciona la cantidad de dias a preparar")
        st.write("3. Selecciona la cantidad de porciones diarias")
        st.write(
            "4. Mira en la tabla el valor de cada elemento a cocinar,\
                cada seccion debe ser agregada a la mezcla final. Puedes hacer\
                click en cada una de ellas para no perderte en la preparacion."
        )
        st.write("5. Cocina y mezcla todo")

with info_tab:
    option = st.selectbox("Seleccione un perrito", [maggie.nombre, pandora.nombre])
    if option:
        perrito = perrito_database[option]
        st.write(f"**Nombre**: {perrito.nombre}")
        st.write(f"**Peso**: {perrito.peso}")
        st.write(f"**Muscular**: {perrito.muscular.listar_elementos()}")
        st.write(f"**Visceral**: {perrito.visceral.listar_elementos()}")
        st.write(f"**Hueso**: {perrito.hueso.listar_elementos()}")
        st.write(f"**Arroz**: {perrito.arroz.listar_elementos()}")
        st.write(f"**Vegetales**: {perrito.vegetales.listar_elementos()}")
        st.write(f"**Frutas**: {perrito.frutas.listar_elementos()}")
        st.write(f"**Total Semanal**: {perrito.total_semana}")
        st.write(f"**Total Diario**: {perrito.total_dia}")
        st.write("----")
