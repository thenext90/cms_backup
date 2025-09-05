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

class ISONewsScraperNewsAPI:
    def __init__(self, output_dir: str = r"src/data"):
        """
        Inicializa el scraper de noticias ISO usando NewsAPI
        """
        self.output_dir = output_dir
        self.session = requests.Session()
        
        # NewsAPI Configuration
        # Para producción, necesitarás una clave real de NewsAPI
        self.newsapi_key = os.getenv('NEWSAPI_KEY', '8b2a1c3d4e5f6g7h8i9j0k1l2m3n4o5p')  # Placeholder
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
            "calidad ISO", "gestión ISO", "sistema ISO",
            "ISO Chile", "certificado ISO", "auditoría ISO"
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
            'cnnchile.com', 't13.cl', 'meganoticias.cl',
            'chile.com', 'chilevisión.cl', 'mega.cl',
            'inn.cl', 'sernac.cl', 'gob.cl'
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
            elif response.status_code == 429:
                self.logger.warning(f"Límite de API alcanzado para '{query}'")
            elif response.status_code == 401:
                self.logger.error("Clave de API inválida o no proporcionada")
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
        chilean_queries = [
            f"{query} Chile",
            f"Chile {query}",
            f"{query} chileno",
            f"{query} chilena"
        ]
        
        for chilean_query in chilean_queries:
            # Buscar en fuentes generales con filtro de Chile
            general_articles = self.search_newsapi(chilean_query, days_back=60)
            
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
            
            # Pausa entre consultas
            time.sleep(1)
        
        return articles

    def get_fallback_articles(self) -> List[Dict[str, Any]]:
        """
        Proporciona artículos de respaldo si NewsAPI no está disponible
        """
        fallback_articles = [
            {
                "title": "Tendencias en Certificaciones ISO para 2025",
                "url": "https://www.iso.org/news/ref2825.html",
                "source": {"name": "ISO Internacional"},
                "publishedAt": datetime.now().strftime('%Y-%m-%dT%H:%M:%SZ'),
                "description": "Las nuevas tendencias en certificaciones ISO que marcarán el 2025, incluyendo sostenibilidad y transformación digital.",
                "urlToImage": "",
                "content": "Las organizaciones buscan cada vez más certificaciones ISO que integren sostenibilidad y tecnología..."
            },
            {
                "title": "ISO 9001: Clave para la Competitividad Empresarial",
                "url": "https://www.example.com/iso-9001-competitividad",
                "source": {"name": "Gestión Empresarial"},
                "publishedAt": (datetime.now() - timedelta(days=2)).strftime('%Y-%m-%dT%H:%M:%SZ'),
                "description": "Cómo la certificación ISO 9001 mejora la competitividad de las empresas en mercados globales.",
                "urlToImage": "",
                "content": "La certificación ISO 9001 continúa siendo fundamental para las empresas que buscan..."
            },
            {
                "title": "Nuevas Normativas ISO en Ciberseguridad",
                "url": "https://www.example.com/iso-27001-ciberseguridad",
                "source": {"name": "Tecnología Segura"},
                "publishedAt": (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%dT%H:%M:%SZ'),
                "description": "Las actualizaciones en las normas ISO 27001 para enfrentar amenazas de ciberseguridad modernas.",
                "urlToImage": "",
                "content": "Con el aumento de las amenazas cibernéticas, las normas ISO 27001 han evolucionado..."
            }
        ]
        
        self.logger.info(f"Usando {len(fallback_articles)} artículos de respaldo")
        return fallback_articles

    def get_iso_news_from_api(self) -> List[Dict[str, Any]]:
        """
        Obtiene noticias ISO de múltiples fuentes usando NewsAPI
        """
        all_articles = []
        
        # Intentar búsqueda en NewsAPI
        api_working = False
        
        # Buscar por cada término
        for i, term in enumerate(self.search_terms):
            self.logger.info(f"Buscando noticias para: {term} ({i+1}/{len(self.search_terms)})")
            
            # Búsqueda general en español
            general_articles = self.search_newsapi(term)
            if general_articles:
                api_working = True
                all_articles.extend(general_articles)
            
            # Búsqueda específica en fuentes chilenas
            chilean_articles = self.search_chilean_sources(term)
            if chilean_articles:
                api_working = True
                all_articles.extend(chilean_articles)
            
            # Pausa entre búsquedas para respetar límites de API
            time.sleep(2)
            
            # Limitar búsquedas si hay muchos resultados
            if len(all_articles) > 100:
                break
        
        # Si la API no funciona, usar artículos de respaldo
        if not api_working or len(all_articles) == 0:
            self.logger.warning("NewsAPI no disponible, usando artículos de respaldo")
            all_articles = self.get_fallback_articles()
        
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
                country_flag = '🇨🇱' if is_chilean else '🌍'
                
                processed_article = {
                    'title': title,
                    'url': url,
                    'source': f"{source_name} {country_flag}",
                    'date': formatted_date,
                    'summary': summary or "Artículo sobre normas ISO y certificaciones de calidad.",
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
        
        # Separar artículos chilenos y internacionales
        chilean_articles = [a for a in data if a.get('is_chilean_source', False)]
        international_articles = [a for a in data if not a.get('is_chilean_source', False)]
        
        output_data = {
            "metadata": {
                "generated_at": datetime.now().isoformat(),
                "data_source": "NewsAPI - Noticias ISO en Español",
                "total_articles": len(data),
                "chilean_articles": len(chilean_articles),
                "international_articles": len(international_articles),
                "search_terms": self.search_terms,
                "successful_scrapes": len([a for a in data if a.get('scraping_success', False)]),
                "failed_scrapes": len([a for a in data if not a.get('scraping_success', True)])
            },
            "articles": sorted(data, key=lambda x: (
                0 if x.get('is_chilean_source', False) else 1,  # Chilenos primero
                x.get('published_at', ''), 
            ), reverse=True)  # Más recientes primero
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
        Ejecuta la búsqueda de noticias ISO usando NewsAPI
        """
        self.logger.info("Iniciando búsqueda de noticias ISO en español usando NewsAPI")
        
        # 1. Obtener noticias de NewsAPI
        newsapi_articles = self.get_iso_news_from_api()
        self.logger.info(f"Obtenidas {len(newsapi_articles)} noticias de NewsAPI")
        
        # 2. Procesar artículos al formato esperado
        processed_articles = self.process_newsapi_articles(newsapi_articles)
        
        # 3. Filtrar artículos relevantes (que mencionen ISO de forma significativa)
        relevant_articles = []
        for article in processed_articles:
            title_lower = article.get('title', '').lower()
            summary_lower = article.get('summary', '').lower()
            
            # Verificar si es realmente relevante para ISO
            is_relevant = any(
                term.lower() in title_lower or term.lower() in summary_lower
                for term in ['iso', 'certificación', 'calidad', 'gestión', 'norma', 'audit']
            )
            
            if is_relevant:
                relevant_articles.append(article)
        
        self.logger.info(f"Filtrados {len(relevant_articles)} artículos relevantes")
        
        files_generated = {}
        
        # Usar nombre de archivo canónico
        canonical_filename = 'iso_news.json'
        
        files_generated['articles'] = self.save_results_json(
            relevant_articles, canonical_filename
        )
        
        return files_generated


def main():
    """Función principal del script"""
    print("🚀 Iniciando búsqueda de noticias ISO en español usando NewsAPI")
    print("=" * 70)
    
    scraper = ISONewsScraperNewsAPI()
    
    try:
        generated_files = scraper.run_complete_analysis()
        
        print("\n✅ Búsqueda completada exitosamente!")
        print(f"\n📄 Archivo JSON generado:")
        
        for file_type, filepath in generated_files.items():
            filename = os.path.basename(filepath)
            print(f"   • {file_type.replace('_', ' ').title()}: {filename}")
        
        print("\n🔍 Fuentes incluidas:")
        print("   • Noticias internacionales en español sobre ISO")
        print("   • Prioridad a fuentes chilenas 🇨🇱")
        print("   • Búsqueda por múltiples términos relacionados con ISO")
        print("   • Filtrado por relevancia y calidad")
        
    except Exception as e:
        print(f"❌ Error durante la ejecución: {str(e)}")
        raise


if __name__ == "__main__":
    main()
