# BellaGlow

Sistema en Python para el control de productos y ventas de *Bella Glow*, un negocio de maquillaje y belleza a domicilio.

## Descripción

Este proyecto corresponde al primer incremento del sistema. Permite a la dueña del negocio registrar los productos de maquillaje que tiene disponibles y registrar cada venta, de modo que el stock se descuente automáticamente.

## Funcionalidades

- Registrar productos con nombre, marca, precio y cantidad disponible (HU-01).
- Buscar un producto por su nombre.
- Consultar el inventario.
- Registrar una venta y descontar el stock automáticamente (HU-02).
- Avisar cuando no hay unidades suficientes para vender.

## Tecnologías

- Python 3
- SQLite
- Programación orientada a objetos
- Git y GitHub

## Archivos principales

| Archivo | Descripción |
|---|---|
| bella_glow.py | Programa principal con el menú, las clases y la conexión a la base de datos |
| bella_glow.db | Base de datos SQLite con productos de ejemplo |
| test_bella_glow.py | Pruebas básicas del registro de productos y de ventas |

## Cómo ejecutarlo


python bella_glow.py


## Autora

Ana María Díaz – Metodologías y Requerimientos de Software – Uniempresarial, 2026.
