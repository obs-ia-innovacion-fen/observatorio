// Acceso al contenido con el filtro de borradores.
//
// Una pieza con `borrador: true` en su ficha no aparece en el sitio
// publicado (rama main). Sí aparece en las vistas previas de Cloudflare de
// cualquier otra rama, marcada como borrador, para poder revisarla tal como
// quedará. Si no se sabe en qué rama se está construyendo, se asume que es
// producción y los borradores se ocultan.
import { getCollection as coleccionCompleta } from 'astro:content';

const rama = process.env.CF_PAGES_BRANCH;
export const esVistaPrevia = process.env.MOSTRAR_BORRADORES === '1' || (!!rama && rama !== 'main');
export const ramaActual = rama ?? null;

export async function getCollection(nombre: any, filtro?: (e: any) => boolean): Promise<any[]> {
  const todas = await coleccionCompleta(nombre);
  return todas.filter((e: any) => (esVistaPrevia || !e.data?.borrador) && (!filtro || filtro(e)));
}
