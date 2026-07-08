# DOS CASAS — Landing

Landing page de e-commerce de DOS CASAS: perfumes + medicina natural de hongos (SETASOULS).
Sitio estático, sin dependencias ni build: HTML + CSS + JS puros.

## Estructura

```
index.html          página principal (~57 KB)
css/style.css       estilos
js/main.js          lógica: catálogo de perfumes, carrito, ritual, WhatsApp
assets/video/       video de fondo del hero
assets/img/         imágenes (logo, hongos, botella, poster)
tools/              scripts Python usados para extraer los assets del HTML original
```

Los pedidos se envían por WhatsApp al número configurado en `js/main.js`
(constante `WA` al inicio del archivo).

## Correr localmente

**No abras `index.html` con doble clic (file://)** — el video de fondo y algunas
funciones necesitan un servidor HTTP. Desde esta carpeta:

```
npx serve
```

y abrí la URL que muestra (normalmente http://localhost:3000).

## Desplegar

### Netlify (lo más fácil)
1. Entrá a https://app.netlify.com/drop
2. Arrastrá esta carpeta completa a la página.
3. Listo — te da una URL pública al instante.

### Vercel
1. Entrá a https://vercel.com/new
2. Conectá el repo de GitHub (o usá `npx vercel` desde esta carpeta).
3. No necesita configuración: es un sitio estático, Vercel lo detecta solo.
