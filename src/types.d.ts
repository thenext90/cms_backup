declare module '*.json' {
  const value: any;
  export default value;
}

declare module '../data/noticias.json' {
  interface Noticia {
    text: string;
    image_url: string;
  }
  const noticias: Noticia[];
  export default noticias;
}

declare module '../../data/noticias.json' {
  interface Noticia {
    text: string;
    image_url: string;
  }
  const noticias: Noticia[];
  export default noticias;
}
