declare module '*.json' {
  const value: any;
  export default value;
}

declare module '../data/cms1.json' {
  interface Noticia {
    text: string;
    image_url: string;
  }
  const noticias: Noticia[];
  export default noticias;
}

declare module '../data/cms2.json' {
  interface NoticiaCMS2 {
    fecha: string;
    texto: string;
    imagen: string;
    link: string;
  }
  interface CMS2Data {
    sitio_web: string;
    url: string;
    fecha_scraping: string;
    total_noticias: number;
    noticias: NoticiaCMS2[];
  }
  const cms2Data: CMS2Data;
  export default cms2Data;
}

declare module '../../data/cms1.json' {
  interface Noticia {
    text: string;
    image_url: string;
  }
  const noticias: Noticia[];
  export default noticias;
}
