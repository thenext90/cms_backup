#!/usr/bin/env python3
"""
Script para búsqueda de noticias sobre normativas ISO en español usando NewsAPI
Busca noticias del mundo en español, con prioridad en Chile
"""

import requests
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import time
import logging

class ISONewsScraperEnhanced:
    def __init__(self, output_dir: str = r"src/data"):
        """
        Inicializa el scraper de noticias ISO usando NewsAPI
        """
        self.output_dir = output_dir
        self.session = requests.Session()
        
        # NewsAPI Configuration
        self.newsapi_key = os.getenv('NEWSAPI_KEY', 'a5b0b5d5ed814c2b9b1f8a8c8e8f8e8f')  # Placeholder
        self.newsapi_base_url = "https://newsapi.org/v2"
        
        # Configurar logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        
        # Crear directorio de salida
        os.makedirs(output_dir, exist_ok=True)
        
        # Términos de búsqueda para normas ISO en español
        self.search_terms = [
            "ISO 9001", "ISO 14001", "ISO 45001", "ISO 27001", 
            "ISO 22000", "normas ISO", "certificación ISO",
            "calidad ISO", "gestión ISO", "sistema ISO"
        ]
        
        # Fuentes en español preferidas
        self.spanish_sources = [
            'el-mundo', 'el-pais', 'abc-es', 'marca', 'la-nacion',
            'clarin', 'infobae', 'ole', 'pagina12'
        ]
        
        # Dominios chilenos específicos para filtrar
        self.chilean_domains = [
            'emol.com', 'latercera.com', 'lun.com', 'df.cl',
            'cooperativa.cl', 'biobiochile.cl', 'adnradio.cl',
            'cnnchile.com', 't13.cl', 'meganoticias.cl'
        ]

    def search_newsapi(self, query: str, language: str = 'es', days_back: int = 30) -> List[Dict[str, Any]]:
        """
        Busca noticias usando NewsAPI
        """
        articles = []
        
        # Fecha desde hace X días
        from_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
        
        # Parámetros de búsqueda
        params = {
            'q': query,
            'language': language,
            'from': from_date,
            'sortBy': 'publishedAt',
            'pageSize': 20,
            'apiKey': self.newsapi_key
        }
        
        try:
            # Buscar en everything endpoint (más amplio)
            response = self.session.get(f"{self.newsapi_base_url}/everything", params=params)
            
            if response.status_code == 200:
                data = response.json()
                articles.extend(data.get('articles', []))
                self.logger.info(f"Encontradas {len(articles)} noticias para '{query}'")
            else:
                self.logger.warning(f"Error en NewsAPI para '{query}': {response.status_code}")
                
        except Exception as e:
            self.logger.error(f"Error buscando '{query}': {str(e)}")
        
        return articles

    def search_chilean_sources(self, query: str) -> List[Dict[str, Any]]:
        """
        Busca específicamente en fuentes chilenas usando NewsAPI
        """
        articles = []
        
        # Términos específicos para Chile
        chilean_query = f"{query} Chile OR Chile {query}"
        
        # Buscar en fuentes generales con filtro de Chile
        general_articles = self.search_newsapi(chilean_query)
        
        # Filtrar artículos que mencionen Chile o tengan dominios chilenos
        for article in general_articles:
            url = article.get('url', '')
            title = article.get('title', '').lower()
            description = article.get('description', '').lower()
            
            # Verificar si es relevante para Chile
            is_chilean = (
                any(domain in url for domain in self.chilean_domains) or
                'chile' in title or 'chile' in description or
                'chileno' in title or 'chileno' in description or
                'chilena' in title or 'chilena' in description
            )
            
            if is_chilean:
                articles.append(article)
        
        return articles

    def get_iso_news_from_api(self) -> List[Dict[str, Any]]:
        """
        Obtiene noticias ISO de múltiples fuentes usando NewsAPI
        """
        all_articles = []
        
        # Buscar por cada término
        for term in self.search_terms:
            self.logger.info(f"Buscando noticias para: {term}")
            
            # Búsqueda general en español
            general_articles = self.search_newsapi(term)
            all_articles.extend(general_articles)
            
            # Búsqueda específica en fuentes chilenas
            chilean_articles = self.search_chilean_sources(term)
            all_articles.extend(chilean_articles)
            
            # Pausa entre búsquedas para respetar límites de API
            time.sleep(1)
        
        # Eliminar duplicados basándose en URL
        unique_articles = {}
        for article in all_articles:
            url = article.get('url')
            if url and url not in unique_articles:
                unique_articles[url] = article
        
        return list(unique_articles.values())

    def process_newsapi_articles(self, articles: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Procesa artículos de NewsAPI al formato esperado
        """
        processed_articles = []
        
        for article in articles:
            try:
                # Extraer información básica
                title = article.get('title', 'Sin título')
                url = article.get('url', '')
                source_name = article.get('source', {}).get('name', 'Fuente desconocida')
                published_at = article.get('publishedAt', '')
                description = article.get('description', '')
                image_url = article.get('urlToImage', '')
                content = article.get('content', '')
                
                # Formatear fecha
                try:
                    if published_at:
                        date_obj = datetime.strptime(published_at, '%Y-%m-%dT%H:%M:%SZ')
                        formatted_date = date_obj.strftime('%d/%m/%Y')
                    else:
                        formatted_date = datetime.now().strftime('%d/%m/%Y')
                except:
                    formatted_date = datetime.now().strftime('%d/%m/%Y')
                
                # Crear resumen
                summary = description if description else (content[:200] + '...' if content and len(content) > 200 else content)
                
                # Determinar si es de Chile
                is_chilean = any(domain in url for domain in self.chilean_domains)
                
                processed_article = {
                    'title': title,
                    'url': url,
                    'source': f"{source_name}{'🇨🇱' if is_chilean else '🌍'}",
                    'date': formatted_date,
                    'summary': summary,
                    'image_url': image_url,
                    'full_content': content,
                    'content_length': len(content) if content else 0,
                    'scraped_at': datetime.now().isoformat(),
                    'scraping_success': True,
                    'is_chilean_source': is_chilean,
                    'published_at': published_at
                }
                
                processed_articles.append(processed_article)
                
            except Exception as e:
                self.logger.warning(f"Error procesando artículo: {str(e)}")
                continue
        
        return processed_articles
    
    def save_results_json(self, data: List[Dict[str, Any]], filename: str) -> str:
        """
        Guarda los resultados en formato JSON
        """
        filepath = os.path.join(self.output_dir, filename)
        
        output_data = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "data_source": self.inn_news_url,
                "total_articles": len(data),
                "successful_scrapes": len([a for a in data if a.get('scraping_success', False)]),
                "failed_scrapes": len([a for a in data if not a.get('scraping_success', True)])
            },
            "articles": data
        }

        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(output_data, f, ensure_ascii=False, indent=2)
            
            self.logger.info(f"Resultados guardados en: {filepath}")
            return filepath
            
        except Exception as e:
            self.logger.error(f"Error guardando resultados: {str(e)}")
            raise
    
    def run_complete_analysis(self) -> Dict[str, str]:
        """
        Ejecuta el scraping, lo combina con artículos hardcodeados y genera el archivo JSON
        """
        self.logger.info("Iniciando el scraping de noticias ISO Chile")
        
        # 1. Obtener la lista de artÃ­culos de INN
        inn_articles = self.scrape_inn_news()
        
        # 2. Combinar con artÃ­culos hardcodeados y de-duplicar
        combined_articles = {article['url']: article for article in inn_articles}
        for article in self.hardcoded_articles:
            if article['url'] not in combined_articles:
                combined_articles[article['url']] = article

        articles_to_scrape = list(combined_articles.values())

        # 3. Extraer contenido para todos los artÃ­culos
        self.logger.info(f"Se procesarÃ¡n {len(articles_to_scrape)} artÃ­culos Ãºnicos.")
        final_articles = self.scrape_direct_urls(articles_to_scrape)

        files_generated = {}
        
        # Use a canonical filename instead of a timestamped one
        canonical_filename = 'iso_news.json'
        
        files_generated['articles'] = self.save_results_json(
            final_articles, canonical_filename
        )
        
        return files_generated


def main():
    """FunciÃ³n principal del script"""
    print("ðŸš€ Iniciando scraper de noticias ISO en Chile desde INN")
    print("=" * 60)
    
    scraper = ISONewsScraperEnhanced()
    
    try:
        generated_files = scraper.run_complete_analysis()
        
        print("\nâœ… Scraping completado exitosamente!")
        print(f"\nðŸ“ Archivo JSON generado:")
        
        for file_type, filepath in generated_files.items():
            filename = os.path.basename(filepath)
            print(f"   â€¢ {file_type.replace('_', ' ').title()}: {filename}")
        
    except Exception as e:
        print(f"âŒ Error durante la ejecuciÃ³n: {str(e)}")
        raise


if __name__ == "__main__":
    main()

