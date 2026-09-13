import pyreadstat
import duckdb

## 1. RUTA DE LOS ARCHIVOS

df_poblacion, _ = pyreadstat.read_dta(
    r"C:/Users/LENOVO/Downloads/Amazonas/cpv2017_pob01.dta",
    encoding="latin1"
)

df_vivienda, _ = pyreadstat.read_dta(
    r"C:/Users/LENOVO/Downloads/Amazonas/cpv2017_viv01.dta",
    encoding="latin1"
)

## 2. CONEXIÓN A DUCKSDB

con = duckdb.connect()

con.register("poblacion", df_poblacion)
con.register("vivienda", df_vivienda)

print("Datos cargados correctamente.")
print("Población:", len(df_poblacion))
print("Viviendas:", len(df_vivienda))


# 3. CREAR BASE DE ANÁLISIS
# Solo Amazonas y viviendas ocupadas con personas presentes

con.execute("""
CREATE OR REPLACE VIEW datos_censo AS
SELECT
    p.*,
    v.c2_p2,
    v.c2_p10
FROM poblacion p
INNER JOIN vivienda v
    ON p.id_viv_imp_f = v.id_viv_imp_f
WHERE p.ccdd = '01'
  AND v.ccdd = '01'
  AND v.c2_p2 = 1
""")

print("Base de análisis creada correctamente.")

## para comprobar 
resultado = con.execute("""
SELECT COUNT(*) AS total_personas
FROM datos_censo
""").fetchone()

print("Personas presentes en Amazonas:", resultado[0])

# 4. INDICADOR 1
# Niños de 0 a 5 años sin conexión a la red pública de desagüe

resultado_1 = con.execute("""
SELECT
    COUNT(*) AS total_ninos,
    SUM(
        CASE
            WHEN c2_p10 NOT IN (1, 2) THEN 1
            ELSE 0
        END
    ) AS ninos_sin_red_publica,
    ROUND(
        100.0 * SUM(
            CASE
                WHEN c2_p10 NOT IN (1, 2) THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS porcentaje
FROM datos_censo
WHERE c5_p4_1 >= 0
  AND c5_p4_1 < 5
""").fetchone()

print("\nINDICADOR 1")
print("Total de niños de 0 a 5 años:", resultado_1[0])
print("Niños sin red pública de desagüe:", resultado_1[1])
print("Porcentaje:", resultado_1[2], "%")


# 5. INDICADOR 2
# Crear grupos etarios y calcular afiliación a algún seguro de salud

con.execute("""
CREATE OR REPLACE VIEW datos_censo_grupos AS
SELECT
    *,
    CASE
        WHEN c5_p4_1 >= 0 AND c5_p4_1 < 5 THEN '0 - 5 años'
        WHEN c5_p4_1 >= 5 AND c5_p4_1 < 15 THEN '5 - 15 años'
        WHEN c5_p4_1 >= 15 AND c5_p4_1 < 35 THEN '15 - 35 años'
        WHEN c5_p4_1 >= 35 AND c5_p4_1 < 65 THEN '35 - 65 años'
        WHEN c5_p4_1 >= 65 THEN '65 + años'
    END AS grupo_etario,

    CASE
        WHEN c5_p8_1 = 1
          OR c5_p8_2 = 1
          OR c5_p8_3 = 1
          OR c5_p8_4 = 1
          OR c5_p8_5 = 1
        THEN 1
        ELSE 0
    END AS tiene_seguro

FROM datos_censo
WHERE c5_p4_1 >= 0
""")

resultado_2 = con.execute("""
SELECT
    grupo_etario,
    COUNT(*) AS total_personas,
    SUM(tiene_seguro) AS afiliados,
    ROUND(
        100.0 * SUM(tiene_seguro) / COUNT(*),
        2
    ) AS porcentaje_afiliacion
FROM datos_censo_grupos
GROUP BY grupo_etario
ORDER BY
    CASE grupo_etario
        WHEN '0 - 5 años' THEN 1
        WHEN '5 - 15 años' THEN 2
        WHEN '15 - 35 años' THEN 3
        WHEN '35 - 65 años' THEN 4
        WHEN '65 + años' THEN 5
    END
""").fetchall()

print("\nINDICADOR 2")
print("Afiliación a algún seguro de salud por grupo etario")

for fila in resultado_2:
    print(
        fila[0],
        "| Total:", fila[1],
        "| Afiliados:", fila[2],
        "| Porcentaje:", fila[3], "%"
    )


# 6. INDICADOR 3
# Tasa de empleo según el Censo
# Población en edad de trabajar: 15 a 64 años

resultado_3 = con.execute("""
SELECT
    COUNT(*) AS poblacion_15_64,

    SUM(
        CASE
            WHEN c5_p16 = 1 THEN 1

            WHEN c5_p16 = 2
                 AND c5_p17 IN (1, 2, 3, 4, 5)
            THEN 1

            ELSE 0
        END
    ) AS poblacion_empleada,

    ROUND(
        100.0 * SUM(
            CASE
                WHEN c5_p16 = 1 THEN 1

                WHEN c5_p16 = 2
                     AND c5_p17 IN (1, 2, 3, 4, 5)
                THEN 1

                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS tasa_empleo

FROM datos_censo

WHERE c5_p4_1 >= 15
  AND c5_p4_1 < 65
""").fetchone()

print("\nINDICADOR 3")
print("Tasa de empleo")

print("Población de 15 a 64 años:", resultado_3[0])
print("Población empleada:", resultado_3[1])
print("Tasa de empleo:", resultado_3[2], "%")


