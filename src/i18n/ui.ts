// Textos de la interfaz en español e inglés. El contenido editorial (fichas,
// notas, webinars) vive en contenido/ y se traduce aparte; aquí solo van los
// textos fijos del sitio: menú, botones, pie de página.

export const idiomas = { es: 'Español', en: 'English' } as const;
export type Idioma = keyof typeof idiomas;
export const idiomaPorDefecto: Idioma = 'es';

export const ui = {
  es: {
    'sitio.nombre': 'Observatorio de IA e Innovación en los Negocios',
    'sitio.nombreCorto': 'Observatorio de IA e Innovación',
    'sitio.institucion': 'Departamento de Administración · FEN · Universidad de Chile',
    'menu.inicio': 'Inicio',
    'menu.actividades': 'Actividades',
    'menu.noticias': 'Noticias',
    'menu.investigacion': 'Investigación',
    'menu.datos': 'Datos',
    'menu.recursos': 'Recursos',
    'menu.nosotros': 'Nosotros',
    'menu.principal': 'Menú principal',
    'tema.claro': 'Cambiar a modo claro',
    'tema.oscuro': 'Cambiar a modo oscuro',
    'idioma.cambiar': 'Read in English',
    'pie.areas': 'Áreas',
    'pie.contacto': 'Contacto',
    'pie.procedencia': 'Cada pieza declara su procedencia y el estatus de revisión de su fuente.',
    'pie.metodo': 'Cómo trabajamos',
    'pie.derechos': 'Facultad de Economía y Negocios, Universidad de Chile',
    'aviso.soloEspanol': 'Este contenido está disponible solo en español.',
    'inicio.verTodo': 'Ver todo',
    'inicio.destacado': 'Evento destacado',
    'inicio.proximas': 'Próximas actividades',
    'inicio.porConfirmar': 'Fecha por confirmar',
    'inicio.agenda': 'Agenda completa',
    'inicio.medios': 'El Observatorio en los medios',
    'inicio.noticias': 'Noticias de IA e innovación',
    'inicio.analisis': 'Análisis del Observatorio',
    'inicio.radar': 'Radar de la semana',
    'inicio.radarTodo': 'Los {n} titulares de la semana',
    'inicio.investigacion': 'Investigación destacada',
    'inicio.podcast': 'Videopodcast',
    'inicio.spotify': 'Escuchar en Spotify',
    'inicio.episodio': 'Episodio',
    'inicio.dato': 'Dato de la región',
    'inicio.indicadores': 'Todos los indicadores',
    'inicio.verEvento': 'Ver el seminario',
  },
  en: {
    'sitio.nombre': 'Observatory of AI and Innovation in Business',
    'sitio.nombreCorto': 'Observatory of AI and Innovation',
    'sitio.institucion': 'Department of Management · FEN · University of Chile',
    'menu.inicio': 'Home',
    'menu.actividades': 'Events',
    'menu.noticias': 'News',
    'menu.investigacion': 'Research',
    'menu.datos': 'Data',
    'menu.recursos': 'Resources',
    'menu.nosotros': 'About',
    'menu.principal': 'Main menu',
    'tema.claro': 'Switch to light mode',
    'tema.oscuro': 'Switch to dark mode',
    'idioma.cambiar': 'Leer en español',
    'pie.areas': 'Areas',
    'pie.contacto': 'Contact',
    'pie.procedencia': 'Every piece states its provenance and the review status of its source.',
    'pie.metodo': 'How we work',
    'pie.derechos': 'School of Economics and Business, University of Chile',
    'aviso.soloEspanol': 'This content is available in Spanish only.',
    'inicio.verTodo': 'See all',
    'inicio.destacado': 'Featured event',
    'inicio.proximas': 'Upcoming',
    'inicio.porConfirmar': 'Date to be confirmed',
    'inicio.agenda': 'Full agenda',
    'inicio.medios': 'The Observatory in the media',
    'inicio.noticias': 'AI and innovation news',
    'inicio.analisis': 'Observatory analysis',
    'inicio.radar': 'This week\'s radar',
    'inicio.radarTodo': 'All {n} headlines this week',
    'inicio.investigacion': 'Featured research',
    'inicio.podcast': 'Videopodcast',
    'inicio.spotify': 'Listen on Spotify',
    'inicio.episodio': 'Episode',
    'inicio.dato': 'Regional figure',
    'inicio.indicadores': 'All indicators',
    'inicio.verEvento': 'See the seminar',
  },
} as const;

export type Clave = keyof (typeof ui)['es'];

export function idiomaDe(url: URL): Idioma {
  const [, primero] = url.pathname.split('/');
  return primero === 'en' ? 'en' : 'es';
}

export function t(idioma: Idioma, clave: Clave): string {
  return ui[idioma][clave] ?? ui.es[clave];
}

// Antepone /en a una ruta interna cuando corresponde.
export function ruta(idioma: Idioma, camino: string): string {
  return idioma === 'en' ? `/en${camino === '/' ? '/' : camino}` : camino;
}

// Paginas que existen en ambos idiomas. Las demas (fichas y notas
// individuales) estan solo en español: el boton de idioma lleva entonces a
// la portada de la seccion correspondiente.
export const rutasBilingues = [
  '/', '/observatorio/', '/datos/', '/publicaciones/', '/recursos/',
  '/novedades/', '/radar/', '/webinars/', '/prensa/', '/metodo/',
];

export function rutaAlterna(url: URL): string {
  const idioma = idiomaDe(url);
  const base = idioma === 'en' ? url.pathname.replace(/^\/en(?=\/|$)/, '') || '/' : url.pathname;
  const conBarra = base.endsWith('/') ? base : `${base}/`;
  const destino = idioma === 'en' ? 'es' : 'en';
  if (rutasBilingues.includes(conBarra)) return ruta(destino, conBarra);
  // Ruta de detalle: se vuelve a la seccion madre si existe en ambos idiomas.
  const seccion = `/${conBarra.split('/')[1]}/`;
  return ruta(destino, rutasBilingues.includes(seccion) ? seccion : '/');
}
