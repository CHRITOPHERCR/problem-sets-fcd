# SQL Analítico + Indicadores — Censo 2017 Amazonas

## Descripción

Este proyecto desarrolla indicadores estadísticos utilizando los datos del **Censo Nacional de Población y Vivienda 2017** de la región Amazonas, mediante **Python, DuckDB y consultas SQL**.

Se utilizan las bases:

* `cpv2017_pob01.dta` — población.
* `cpv2017_viv01.dta` — vivienda.

Las bases se relacionan mediante `id_viv_imp_f` y se consideran únicamente los registros de **Amazonas (`ccdd = '01'`)** correspondientes a **viviendas ocupadas con personas presentes (`c2_p2 = 1`)**.

## Indicadores

### 1. Niños sin conexión a red pública de desagüe

Se calcula el porcentaje de niños de 0 a 5 años cuyo baño no está conectado a la red pública de desagüe.

**Resultado: 62.23 %**

### 2. Afiliación a algún seguro de salud

Se crean los grupos etarios:

* 0 - 5 años
* 5 - 15 años
* 15 - 35 años
* 35 - 65 años
* 65+ años

Resultados:

| Grupo etario | Afiliación |
| ------------ | ---------: |
| 0 - 5 años   |    93.52 % |
| 5 - 15 años  |    93.16 % |
| 15 - 35 años |    82.82 % |
| 35 - 65 años |    82.90 % |
| 65+ años     |    84.03 % |

### 3. Tasa de empleo

Se considera como población en edad de trabajar a las personas de **15 a 64 años**. Se incluyen quienes trabajaron y quienes, aunque no trabajaron durante la semana, se encontraban en alguna de las situaciones laborales indicadas por el Censo.

**Resultado: 52.00 %**

## Ejecución

Para ejecutar el análisis pegamos lo siguiente en la terminal:

```powershell
python .\analisis_censo.py
```


