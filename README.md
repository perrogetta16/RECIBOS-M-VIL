FjordReceipts - Build instructions

Resumen
- Este repo contiene `impresoranoruega.py`, una app Kivy que registra pagos y puede imprimir por Bluetooth usando `pyjnius`.

Opción A: Compilar localmente en Windows usando WSL2 (recomendado)
1. Instalar WSL2 y Ubuntu (PowerShell admin):

```powershell
wsl --install
```

2. Abrir Ubuntu y actualizar:

```bash
sudo apt update; sudo apt upgrade -y
```

3. Instalar dependencias del sistema:

```bash
sudo apt install -y git python3-pip python3-venv openjdk-11-jdk unzip build-essential autoconf libtool pkg-config zlib1g-dev
```

4. Crear entorno virtual e instalar buildozer:

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install buildozer==1.4.7
```

5. Colocar `impresoranoruega.py` en la carpeta del proyecto (donde está `buildozer.spec`) y ejecutar:

```bash
buildozer android debug
```

6. El APK resultante estará en `bin/` (por ejemplo `bin/fjordreceipts-0.1-debug.apk`).

Opción B: Compilar en CI (GitHub Actions)
- He incluido un workflow en `.github/workflows/build-apk.yml`. Simplemente crea un repo en GitHub, sube todos los archivos y abre la pestaña Actions; al hacer push a `main` o ejecutar manualmente el workflow, Actions intentará construir el APK y guardarlo como artefacto descargable.

Presplash
- Si ya tienes `icon.png`, no es necesario duplicarla: `buildozer.spec` ya usa `icon.png` como `presplash`.

Notas importantes
- Buildozer y p4a necesitan Linux (por eso WSL2 o CI). En Windows puro no funciona bien.
- Asegúrate de incluir `pyjnius` en `requirements` (ya lo añadí al `buildozer.spec`).
- Permisos de Bluetooth y runtime permissions (Android 12+) pueden requerir manejo adicional en la app.

Siguientes pasos que puedo hacer por ti
- Ajustar `buildozer.spec` (iconos, versión, package.domain).
- Preparar un Dockerfile para compilación local sin WSL.
- Mejorar la gestión de permisos Bluetooth en la app (solicitar permisos en tiempo de ejecución).
- Generar el APK en mi entorno si me das acceso al repo (no disponible desde este entorno).
