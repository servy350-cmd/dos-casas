@echo off
cd /d "%~dp0"
echo Abriendo DOS CASAS en el navegador...
echo (Deja esta ventana negra abierta mientras mires la pagina. Para cerrar todo, cerra esta ventana.)
start "" http://localhost:8888
npx -y serve -l 8888 .
