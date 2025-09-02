#!/usr/bin/env python3
"""
Script mejorado para bÃºsqueda de noticias sobre normativas ISO en Chile
Incluye datos reales encontrados y capacidad de scraping directo
"""

import requests
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import time
from bs4 import BeautifulSoup
import re
from urllib.parse import urljoin, urlparse
import logging

class ISONewsScraperEnhanced:
    def __init__(self, output_dir: str = r"src/data/iso_news"):
        """
        Inicializa el scraper mejorado de noticias ISO para Chile
        """
        self.output_dir = output_dir
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Configurar logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.logger = logging.getLogger(__name__)
        
        # Crear directorio de salida
        os.makedirs(output_dir, exist_ok=True)
        
        self.news_data = []
        self.inn_news_url = "https://www.inn.cl/noticias"
        self.hardcoded_articles = [
            {
                "title": "Normas Aprobadas Julio 2025",
                "url": "https://www.inn.cl/normas-aprobadas-julio-2025",
                "source": "Instituto Nacional de Normalización (INN)",
                "date": "30/07/2025",
                "summary": "8 nuevas normas ISO aprobadas por el INN en julio 2025, incluyendo microbiología alimentaria, sostenibilidad en edificios y transporte inteligente"
            },
            {
                "title": "CMP certifica su Modelo GRP con tres normas internacionales ISO",
                "url": "https://www.mch.cl/negocios-industria/cmp-certifica-su-modelo-grp-con-tres-normas-internacionales-iso/",
                "source": "Minería Chilena",
                "date": "30/07/2025",
                "summary": "CMP logra certificación triple ISO tras auditoría a 69 procesos en el Valle de Copiapó"
            },
            {
                "title": "San Antonio Terminal Internacional renueva certificaciones ISO 9001 e ISO 14001",
                "url": "https://www.empresaoceano.cl/san-antonio-terminal-internacional-renueva-certificaciones-iso-9001-e",
                "source": "Empresa Océano",
                "date": "25/07/2025",
                "summary": "STI renueva certificaciones ISO 9001 e ISO 14001, manteniendo también ISO 45001 e ISO 50001"
            },
            {
                "title": "ISP recibe al Instituto Nacional de Normalización (INN) para verificar capacidades técnicas del Laboratorio de Metrología",
                "url": "https://www.ispch.gob.cl/noticia/isp-recibe-al-instituto-nacional-de-normalizacion-inn-para-verificar-capacidades-tecnicas-del-laboratorio-de-metrologia/",
                "source": "Instituto de Salud Pública",
                "date": "25/07/2025",
                "summary": "Visita técnica del INN al ISP para verificar capacidades de la Red Nacional de Metrología"
            },
            {
                "title": "AdClean obtiene la certificación ISO 9001 otorgada por Bureau Veritas",
                "url": "https://www.adclean.cl/blogs/noticias/certificacion-iso-9001",
                "source": "Bureau Veritas",
                "date": "21/11/2023",
                "summary": "AdClean obtiene la certificación ISO 9001 otorgada por Bureau Veritas, reflejando el compromiso con la calidad y la excelencia."
            }
        ]

    def scrape_inn_news(self) -> List[Dict[str, str]]:
        """
        Extrae las noticias directamente de la página de noticias del INN.
        """
        self.logger.info(f"Extrayendo noticias de: {self.inn_news_url}")
        articles = []
        try:
            response = self.session.get(self.inn_news_url, timeout=15)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')

            news_rows = soup.select('table.views-table tbody tr')
            for row in news_rows:
                date_cell = row.select_one('td.views-field-created')
                title_cell = row.select_one('td.views-field-title a')

                if date_cell and title_cell:
                    date = date_cell.get_text(strip=True)
                    title = title_cell.get_text(strip=True)
                    url = urljoin(self.inn_news_url, title_cell['href'])
                    articles.append({'title': title, 'url': url, 'date': date, 'source': 'INN'})
        except Exception as e:
            self.logger.error(f"Error extrayendo noticias del INN: {e}")

        return articles

    def scrape_direct_urls(self, articles_to_scrape: List[Dict[str, str]]) -> List[Dict[str, Any]]:
        """
        Extrae contenido directamente de una lista de URLs de artÃ­culos.
        """
        scraped_articles = []

        for news_item in articles_to_scrape:
            try:
                self.logger.info(f"Extrayendo contenido de: {news_item['title'][:50]}...")

                # Nota: verify=False se aÃ±ade para omitir errores de SSL en sitios con certificados mal configurados (ej. ispch.gob.cl)
                response = self.session.get(news_item['url'], timeout=15, verify=False)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                
                # Extraer contenido completo
                content_text = ''
                content_selectors = [
                    'div.field-item', '.content', '.article-content', '.entry-content',
                    '.post-content', '.main-content', 'article',
                    '.article-body', '.story-body'
                ]
                
                for selector in content_selectors:
                    content_elem = soup.select_one(selector)
                    if content_elem:
                        # Remover scripts y estilos
                        for script in content_elem(["script", "style"]):
                            script.decompose()
                        content_text = content_elem.get_text(strip=True, separator=' ')
                        break
                
                # Si no encontramos contenido especÃ­fico, usar todo el texto
                if not content_text:
                    content_text = soup.get_text(strip=True, separator=' ')
                
                # Extraer imagen principal (og:image o primera imagen relevante)
                image_url = None
                og_image = soup.select_one('meta[property="og:image"]')
                if og_image:
                    image_url = urljoin(news_item['url'], og_image['content'])
                else:
                    # Fallback a buscar una imagen en el contenido
                    content_img = soup.select_one('.content img, .entry-content img, .article-body img')
                    if content_img and content_img.get('src'):
                        image_url = urljoin(news_item['url'], content_img['src'])

                # Crear artÃ­culo completo
                summary = content_text[:200] + '...' if len(content_text) > 200 else content_text
                complete_article = {
                    'title': news_item['title'],
                    'url': news_item['url'],
                    'source': news_item['source'],
                    'date': news_item['date'],
                    'summary': summary,
                    'image_url': image_url,
                    'full_content': content_text[:10000],  # Limitar a 10k caracteres
                    'content_length': len(content_text),
                    'scraped_at': datetime.now().isoformat(),
                    'scraping_success': True
                }
                
                scraped_articles.append(complete_article)
                time.sleep(1)  # Pausa entre requests
                
            except Exception as e:
                self.logger.warning(f"Error extrayendo {news_item['url']}: {str(e)}")
                # Agregar artÃ­culo sin contenido completo
                error_article = {
                    'title': news_item['title'],
                    'url': news_item['url'],
                    'source': news_item['source'],
                    'date': news_item['date'],
                    'full_content': '',
                    'content_length': 0,
                    'scraped_at': datetime.now().isoformat(),
                    'scraping_success': False,
                    'error': str(e)
                }
                scraped_articles.append(error_article)
        
        return scraped_articles
    
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
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        files_generated['articles'] = self.save_results_json(
            final_articles, f'iso_news_articulos_{timestamp}.json'
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

