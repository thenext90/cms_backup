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

declare module '../../data/cms1.json' {
  interface Noticia {
    text: string;
    image_url: string;
  }
  const noticias: Noticia[];
  export default noticias;
}
