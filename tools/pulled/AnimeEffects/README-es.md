# AnimeEffects

## Descargas

|                                                                                                                                                              Estable (v1.6)                                                                                                                                                               |                                                                                                                                                                                     Nocturno                                                                                                                                                                                     |                                          Código fuente                                          |
| :---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: | :------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------: | :---------------------------------------------------------------------------------------------: |
| [Windows](https://github.com/AnimeEffectsDevs/AnimeEffects/releases/download/v1.6/AnimeEffects-Installer-Windows.exe) - [MacOS](https://github.com/AnimeEffectsDevs/AnimeEffects/releases/download/v1.6/AnimeEffects-MacOS.zip) - [Linux](https://github.com/AnimeEffectsDevs/AnimeEffects/releases/download/v1.6/AnimeEffects-Linux.zip) | [Windows](https://nightly.link/AnimeEffectsDevs/AnimeEffects/workflows/build-windows.yaml/master/AnimeEffects-Windows-x64.zip) - [MacOS](https://nightly.link/AnimeEffectsDevs/AnimeEffects/workflows/build_mac_intel.yaml/master/AnimeEffects-MacOS.zip) - [Linux](https://nightly.link/AnimeEffectsDevs/AnimeEffects/workflows/build_linux.yaml/master/AnimeEffects-Linux.zip) | [Descargar ZIP](https://github.com/AnimeEffectsDevs/AnimeEffects/archive/refs/heads/master.zip) |

## 🌐 LÉEME 🌐

[English](./README.md) - Up-to-date <br>
[日本語](./README-ja.md) - 時代遅れ <br>
[简体中文](./README-zh.md) - 最新 <br>
[正體中文](./README-zh-t.md) - 尚未提供 <br>
[Español](./README-es.md) - Actualizado <br>

## Descripción

Herramienta de animación 2D que no requiere planificación detallada, simplifica la creación de animaciones mediante diversas funciones basadas en deformación de mallas poligonales.<br>
Desarrollado originalmente por hidefuku, actualmente mantenido y mejorado por la comunidad.

- Sitio web oficial:<br>

  - <https://animeeffectsdevs.github.io/>

- Redes sociales oficiales:<br>

  - Discord: <a href='https://discord.gg/sKp8Srm'>AnimeEffects</a> (cortesía de [José Moreno](https://github.com/Jose-Moreno))<br>
  - X (Twitter): <a href='https://x.com/anime_effects'>@anime_effects</a> (cortesía de [p_yukusai](https://github.com/p-yukusai))<br>
  - Reddit: <a href='https://www.reddit.com/r/AnimeEffects/'>r/AnimeEffects</a> (cortesía de [visterical](https://www.tumblr.com/visterical))<br>

- Puedes apoyar el proyecto mediante:<br><br>
  [![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/V7V04YLC3) &nbsp;&nbsp; <a href="https://yukusai.itch.io/animeeffects" target="_blank"> <img src="https://static.itch.io/images/badge-color.svg" alt="itch.io" style="width:100px" /> </a>

Nota: Actualmente pueden realizarse cambios incompatibles entre versiones, los cuales se comunicarán en los lanzamientos correspondientes.<br>
**_Si tienes algún problema o deseas sugerir nuevas funciones, ¡no dudes en comunicarte con nosotros en nuestras redes sociales!_**

## Lanzamientos

AnimeEffects te notificará automáticamente cuando haya nuevas versiones estables disponibles.

- Nuestras versiones estables están disponibles [aquí](https://github.com/AnimeEffectsDevs/AnimeEffects/releases).<br>
- Versiones inestables disponibles [aquí](https://github.com/p-yukusai/AnimeEffects/releases).<br>
- Versiones nocturnas disponibles [aquí](https://github.com/AnimeEffectsDevs/AnimeEffects/actions).

## Requisitos

- Windows/Linux/Mac
  - Ver versiones compatibles más abajo
- Procesador: CPU de 64 bits
- RAM: 4 GB
- Tarjeta gráfica: GPU/iGPU compatible con OpenGL 4.0 o superior
- [FFmpeg](https://ffmpeg.org/download.html) (Necesario para la exportación de vídeo. Puede colocarlo en su PATH o copiarlo en la carpeta "/tools" - cree esta carpeta junto al ejecutable si no existe)

## Sistemas Operativos objetivos

#### Versiones donde probamos y compilamos el software. Puede funcionar en versiones anteriores pero no es recomendable

- Windows 10 o superior
- Ubuntu LTS o distribuciones equivalentes
- MacOS Big Sur o más reciente

## Requisitos para el desarrollo

- Qt 6.6.X
- Encabezados de Vulkan
- CMake 3.16 o posterior
- MSVC/GCC/CLang (64-bit)

## Linux (Debian)

### Compilación y creación de AppImage

- La mayoría de estas dependencias son innecesarias, ya que vienen con su distribución, así que compruebe sus propios paquetes:

```
sudo apt update && sudo apt upgrade -y
sudo apt install -y software-properties-common g++ make cmake ninja-build wget rsync build-essential libglib2.0-0
sudo apt install -y libgl1-mesa-dev file libvulkan-dev openssl python3 python3-pip libxcb-cursor0 libxrandr2 wget
pip install -U pip
pip install aqtinstall
aqt install-qt linux desktop 6.6.2 gcc_64 -m qtimageformats qtmultimedia qt5compat
git clone https://github.com/AnimeEffectsDevs/AnimeEffects
cd AnimeEffects
cmake -S . -B build -G "Ninja Multi-Config"
cmake --build build --config Release
cd build/src/gui/Release
mkdir -p appdir
cp AnimeEffects appdir
cp -R ../data appdir/data
cp -R ../../../../dist appdir/dist
cp ../../../../dist/AnimeEffects.png appdir
find appdir/
export APPIMAGE_EXTRACT_AND_RUN=1
wget -c -nv "https://github.com/p-yukusai/linuxdeployqt/releases/download/continuous/linuxdeployqt-continuous-x86_64.AppImage"
chmod a+x linuxdeployqt-continuous-x86_64.AppImage
./linuxdeployqt-continuous-x86_64.AppImage appdir/dist/AnimeEffects.desktop -extra-plugins=imageformats,multimedia,core5compat -appimage -verbose=2
chmod a+x AnimeEffects-x86_64.AppImage
```

## Windows

### Compilación y creación de carpetas

- Los pasos de instalación asumen que has instalado todos los requisitos mediante sus instaladores y los tienes en tu PATH

```powershell
git clone https://github.com/AnimeEffectsDevs/AnimeEffects
cd AnimeEffects
cmake -S . -B build -G "Ninja Multi-Config"
cmake --build build --config Release
cd build/src/gui/Release
mkdir .\AnimeEffects-Windows-x64
windeployqt --dir .\AnimeEffects-Windows-x64 .\AnimeEffects.exe
Copy-Item -Path "..\data" -Destination ".\AnimeEffects-Windows-x64\" -recurse -Force
Copy-Item ".\AnimeEffects.exe" ".\AnimeEffects-Windows-x64\"
```

## MacOS

### Compilación y creación de .app

- Estos pasos asumen que tienes instalados: xcode, brew, wget, python 3 y pip

```bash
brew install cmake ninja vulkan-headers
pip install -U pip
pip install aqtinstall
aqt install-qt mac desktop 6.6.2 clang_64 -m qtimageformats qtmultimedia qt5compat
git clone https://github.com/AnimeEffectsDevs/AnimeEffects
cd AnimeEffects
cmake -S . -B build -G "Ninja Multi-Config"
cmake --build build --config Release
cd build/src/gui/Release
mkdir -p appdir/usr/lib
cp -R AnimeEffects.app appdir/AnimeEffects.app
cp -R ../data appdir/data
cp -R ../../../../dist appdir/dist
find appdir/
cd appdir
macdeployqt AnimeEffects.app
wget https://raw.githubusercontent.com/OpenZWave/ozw-admin/master/scripts/macdeployqtfix.py && chmod a+x macdeployqtfix.py
./macdeployqtfix.py AnimeEffects.app /usr/local/Cellar/qt/*/
```
