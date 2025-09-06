#!/usr/bin/env python3
import sys
import os
sys.path.append('scripts')

from iso_news_scraper_enhanced import ISONewsScraperEnhanced
import json

def debug_news():
    print('🔍 Debugging ISO News Scraper...')
    
    # Crear instancia del scraper
    scraper = ISONewsScraperEnhanced()
    
    # Verificar si hay noticias INN
    print('\n📰 Obteniendo noticias del INN...')
    inn_articles = scraper.scrape_inn_news()
    print(f'✅ Encontradas {len(inn_articles)} noticias del INN')
    
    # Mostrar primeras 3 noticias
    print('\n📋 Primeras 3 noticias del INN:')
    for i, article in enumerate(inn_articles[:3]):
        print(f'{i+1}. {article["title"]}')
        print(f'   🔗 URL: {article["url"]}')
        print(f'   📅 Fecha: {article["date"]}')
        print(f'   📝 Resumen: {article["summary"][:100]}...')
        print()
    
    # Verificar archivo actual
    json_file = 'src/data/iso_news.json'
    if os.path.exists(json_file):
        with open(json_file, 'r', encoding='utf-8') as f:
            current_data = json.load(f)
        print(f'\n📁 Archivo actual tiene {len(current_data.get("articles", []))} artículos')
        print(f'📅 Generado: {current_data.get("metadata", {}).get("generated_at", "N/A")}')
        
        # Mostrar primeros 3 artículos del archivo
        print('\n📋 Primeros 3 artículos del archivo actual:')
        for i, article in enumerate(current_data.get("articles", [])[:3]):
            title = article.get("title", "Sin título")
            source = article.get("source", {})
            source_name = source.get("name", source) if isinstance(source, dict) else str(source)
            print(f'{i+1}. {title}')
            print(f'   🏢 Fuente: {source_name}')
            print()

if __name__ == "__main__":
    debug_news()
