import { defineCollection, z } from 'astro:content';
import { glob } from 'astro/loaders';

const areas = defineCollection({
  loader: glob({ pattern: '*.md', base: './contenido/areas' }),
  schema: z.object({
    titulo: z.string(),
    slug: z.string(),
    orden: z.number().default(99),
    descripcion: z.string(),
    alcance: z.string().optional(),
    diplomado_modulo: z.string().optional().nullable(),
  }),
});

const publicaciones = defineCollection({
  loader: glob({ pattern: '[^_]*.md', base: './contenido/publicaciones' }),
  schema: z.object({
    titulo: z.string(),
    autores: z.array(z.string()).default([]),
    anio: z.number().optional().nullable(),
    doi: z.string().optional().nullable(),
    enlace: z.string().optional().nullable(),
    publicado_en: z.string().optional().nullable(),
    area: z.string(),
    tipo: z.enum(['propio', 'colaboracion', 'comentada', 'sugerencia']),
    fuente_ficha: z.string().optional().nullable(),
    revisado_por_pares: z.boolean().optional().nullable(),
    institucion: z.string().optional().nullable(),
    destacado: z.boolean().default(false),
  }),
});

const vigilancia = defineCollection({
  loader: glob({ pattern: '*.md', base: './contenido/vigilancia' }),
  schema: z.object({
    titulo: z.string(),
    fecha: z.coerce.date(),
    area: z.string(),
    autor: z.string().optional().nullable(),
    paises: z.array(z.string()).default([]),
    fuentes: z.array(z.string()).default([]),
  }),
});

const webinars = defineCollection({
  loader: glob({ pattern: '[^_]*.md', base: './contenido/webinars' }),
  schema: z.object({
    titulo: z.string(),
    fecha_evento: z.coerce.date(),
    panelistas: z.array(z.string()).default([]),
    area: z.string().optional().nullable(),
    grabacion: z.string().optional().nullable(),
    materiales: z.array(z.string()).default([]),
  }),
});

export const collections = { areas, publicaciones, vigilancia, webinars };
