// Textos de la interfaz en español e inglés. El contenido editorial (fichas,
// notas, webinars) vive en contenido/ y se traduce aparte; aquí solo van los
// textos fijos del sitio: menú, botones, pie de página.

export const idiomas = { es: 'Español', en: 'English', pt: 'Português' } as const;
export const locales = { es: 'es-CL', en: 'en-US', pt: 'pt-BR' } as const;
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
  pt: {
    'sitio.nombre': 'Observatório de IA e Inovação nos Negócios',
    'sitio.nombreCorto': 'Observatório de IA e Inovação',
    'sitio.institucion': 'Departamento de Administração · FEN · Universidade do Chile',
    'menu.inicio': 'Início',
    'menu.actividades': 'Eventos',
    'menu.noticias': 'Notícias',
    'menu.investigacion': 'Pesquisa',
    'menu.datos': 'Dados',
    'menu.recursos': 'Recursos',
    'menu.nosotros': 'Sobre nós',
    'menu.principal': 'Menu principal',
    'tema.claro': 'Mudar para o modo claro',
    'tema.oscuro': 'Mudar para o modo escuro',
    'idioma.cambiar': 'Idioma',
    'pie.areas': 'Áreas',
    'pie.contacto': 'Contato',
    'pie.procedencia': 'Cada peça declara sua procedência e o status de revisão de sua fonte.',
    'pie.metodo': 'Como trabalhamos',
    'pie.derechos': 'Faculdade de Economia e Negócios, Universidade do Chile',
    'aviso.soloEspanol': 'Este conteúdo está disponível apenas em espanhol.',
    'inicio.verTodo': 'Ver tudo',
    'inicio.destacado': 'Evento em destaque',
    'inicio.proximas': 'Próximas atividades',
    'inicio.porConfirmar': 'Data a confirmar',
    'inicio.agenda': 'Agenda completa',
    'inicio.medios': 'O Observatório na mídia',
    'inicio.noticias': 'Notícias de IA e inovação',
    'inicio.analisis': 'Análise do Observatório',
    'inicio.radar': 'Radar da semana',
    'inicio.radarTodo': 'As {n} manchetes da semana',
    'inicio.investigacion': 'Pesquisa em destaque',
    'inicio.podcast': 'Videopodcast',
    'inicio.spotify': 'Ouvir no Spotify',
    'inicio.episodio': 'Episódio',
    'inicio.dato': 'Dado da região',
    'inicio.indicadores': 'Todos os indicadores',
    'inicio.verEvento': 'Ver o seminário',
  },
} as const;

export type Clave = keyof (typeof ui)['es'];

export function idiomaDe(url: URL): Idioma {
  const [, primero] = url.pathname.split('/');
  return primero === 'en' || primero === 'pt' ? primero : 'es';
}

export function t(idioma: Idioma, clave: Clave): string {
  return ui[idioma][clave] ?? ui.es[clave];
}

// Antepone /en o /pt a una ruta interna cuando corresponde.
export function ruta(idioma: Idioma, camino: string): string {
  return idioma === 'es' ? camino : `/${idioma}${camino}`;
}

// Paginas que existen en los tres idiomas. Las demas (fichas y notas
// individuales) estan solo en español: el selector de idioma lleva entonces
// a la portada de la seccion correspondiente.
export const rutasTraducidas = [
  '/', '/observatorio/', '/datos/', '/publicaciones/', '/recursos/',
  '/novedades/', '/radar/', '/webinars/', '/prensa/', '/metodo/',
];

// La misma pagina en otro idioma.
export function rutaEn(url: URL, destino: Idioma): string {
  const base = url.pathname.replace(/^\/(en|pt)(?=\/|$)/, '') || '/';
  const conBarra = base.endsWith('/') ? base : `${base}/`;
  if (destino === 'es' || rutasTraducidas.includes(conBarra)) return ruta(destino, conBarra);
  // Ruta de detalle: se va a la seccion madre si esta traducida.
  const seccion = `/${conBarra.split('/')[1]}/`;
  return ruta(destino, rutasTraducidas.includes(seccion) ? seccion : '/');
}
