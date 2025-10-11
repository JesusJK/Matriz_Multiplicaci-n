# Calculadora de Multiplicación de Matrices (GUI)

## Descripción del Proyecto

Aplicación con interfaz gráfica en Python (Tkinter) para realizar:
- Multiplicación Matriz × Matriz (A×B)
- Multiplicación Escalar × Matriz (s·A) y Matriz × Escalar (A·s)

Incluye validaciones de entradas, manejo de dimensiones y una pestaña de documentación integrada que explica el proceso y ejemplos.

## Objetivos

- Permitir operaciones de multiplicación entre matrices y escalares de forma intuitiva.
- Validar dimensiones y tipos de datos de forma segura.
- Proveer documentación integrada sobre el fundamento y el uso.

## Fundamento Matemático

### Multiplicación por Escalar
Sea un escalar real `s` y una matriz `A = [a_ij]`. Entonces:
```
s · A = [s · a_ij]
```
Cada elemento de la matriz se multiplica por el escalar.

### Multiplicación de Matrices
Sean `A` de tamaño `m×n` y `B` de tamaño `n×p`. El producto `C = A×B` existe si y solo si `columnas(A) = filas(B)` y resulta en `C` de tamaño `m×p`:
```
C[i,j] = Σ_{k=1..n} A[i,k] · B[k,j]
```

## Instalación

### Requisitos del Sistema
- Python 3.8 o superior
- Sistema operativo: Windows, macOS o Linux
- Tkinter (incluido por defecto en la instalación estándar de Python desde python.org)

### Paso 1: Obtener el proyecto
Puedes descargar el directorio o clonarlo desde tu repositorio. Si usas este ejemplo local:
```
C:\Users\USUARIO\CascadeProjects\MatrixCalcGUI\
```

### Paso 2: Instalar dependencias
Esta app no requiere paquetes externos.
Si deseas usar `pip` de todos modos:
```bash
pip install -r requirements.txt
```

### Paso 3: Ejecutar la aplicación
```bash
python app.py
```

## Manual de Usuario

### Interfaz de la Aplicación (Pestañas)

La aplicación cuenta con 2 pestañas principales:

#### 1. Calculadora
- **Operación**: Selecciona `A×B`, `Escalar×A` o `A×Escalar`.
- **Matriz A / Matriz B**: Ajusta `Filas` y `Columnas` (hasta 10×10) e ingresa valores.
- **Escalar**: Campo visible solo si la operación involucra un escalar.
- **Acciones**:
  - `Calcular`: Ejecuta la operación seleccionada.
  - `Limpiar`: Borra el panel de resultado.
- **Resultado**: Muestra la matriz resultante con formato legible.

#### 2. Documentación
- Explica el proceso matemático para `s·A` y `A×B`, condiciones de dimensiones, validaciones, y ejemplos.

### Validaciones y Restricciones
- Entradas numéricas: se aceptan enteros, decimales con punto y notación científica (por ejemplo, `-2.5`, `3.14`, `1e-3`).
- `A×B` requiere que `columnas(A) = filas(B)`. De lo contrario, se muestra un error.
- Dimensiones máximas configurables por UI: hasta `10×10`.

### Ejemplo Paso a Paso
1. Elige `A×B`.
2. Configura `A` como `2×3` y `B` como `3×2`.
3. Ingresa valores en las celdas.
4. Presiona `Calcular`.
5. Observa la matriz `C (2×2)` en el panel de resultado.

## Interpretación de Resultados
- En `s·A`: cada elemento de `A` se escala por `s`.
- En `A×B`: cada entrada `C[i,j]` es la suma ponderada por columnas/filas correspondiente.
- Los resultados se formatean de manera compacta (por ejemplo, `2` en lugar de `2.0` cuando aplica).

## Solución de Problemas
- **"Dimensiones incompatibles"**: Ajusta filas/columnas para cumplir `columnas(A) = filas(B)`.
- **"Entrada no numérica"**: Revisa que todos los campos tengan números válidos.
- **Separador decimal**: Usa punto (`.`). Si prefieres coma, se puede habilitar.

## Estructura del Proyecto
```
MatrixCalcGUI/
├─ app.py              # Aplicación principal Tkinter
├─ requirements.txt    # Dependencias (sin paquetes externos)
└─ README.md           # Este documento
```

## Licencia
Este proyecto se distribuye con fines educativos. Ajusta la licencia según tus necesidades.
