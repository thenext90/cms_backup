#!/usr/bin/env python3
"""
Archivo de configuración para el scraper de noticias ISO en Chile
Modifica estos parámetros según tus necesidades específicas
"""

# Configuración general
CONFIG = {
    'output_directory': r'C:\Users\jp200\Downloads\newsjp_phyton',
    'days_back': 45,  # Días hacia atrás para buscar noticias
    'max_articles_detailed': 10,  # Máximo de artículos para extraer contenido completo
    'delay_between_requests': 2,  # Segundos de pausa entre requests
    'timeout_seconds': 10,  # Timeout para requests HTTP
}

# Consultas de búsqueda personalizables
SEARCH_QUERIES = [
    # Búsquedas generales sobre ISO
    'normativas ISO Chile',
    'certificación ISO Chile',
    'normas ISO aprobadas Chile',
    
    # Búsquedas específicas por institución
    'INN Instituto Nacional Normalización',
    'ISP Instituto Salud Pública ISO',
    
    # Búsquedas por tipos de norma ISO específicos
    'ISO 9001 Chile certificación',
    'ISO 14001 Chile medio ambiente',
    'ISO 45001 Chile seguridad ocupacional',
    'ISO 50001 Chile eficiencia energética',
    'ISO 27001 Chile seguridad información',
    
    # Búsquedas por sectores
    'Bureau Veritas Chile ISO',
    'certificación ISO minería Chile',
    'ISO puertos Chile',
    'sistema gestión calidad Chile',
    'acreditación laboratorio Chile ISO',
    
    # Búsquedas específicas para julio 2025 (personalizable por mes)
    'normas aprobadas julio 2025 Chile',
    'certificación ISO julio 2025 Chile',
]

# Palabras clave para filtrar relevancia ISO
ISO_KEYWORDS = [
    # Normas ISO específicas
    'ISO 9001', 'ISO 14001', 'ISO 45001', 'ISO 50001', 'ISO 27001',
    'ISO 22000', 'ISO 37001', 'ISO 56001', 'ISO 17025', 'ISO 17043',
    'ISO 16745', 'ISO 37161', 'ISO 6887', 'ISO 16140',
    
    # Términos generales ISO
    'norma ISO', 'certificación ISO', 'acreditación ISO',
    'sistema de gestión ISO', 'auditoría ISO',
    
    # Instituciones y organismos
    'INN', 'Instituto Nacional de Normalización',
    'Bureau Veritas', 'SGS', 'AENOR', 'ENAC',
    'ISP', 'Instituto de Salud Pública',
    
    # Conceptos relacionados
    'normalización', 'certificación', 'acreditación',
    'sistema de gestión', 'calidad', 'medio ambiente',
    'seguridad ocupacional', 'eficiencia energética',
    'seguridad de la información', 'metrología',
    'ensayos de aptitud', 'materiales de referencia',
    
    # Sectores específicos
    'minería', 'portuario', 'alimentario', 'construcción',
    'salud', 'laboratorio', 'industrial'
]

# Fuentes conocidas y confiables
KNOWN_SOURCES = {
    'inn': {
        'name': 'Instituto Nacional de Normalización',
        'base_url': 'https://www.inn.cl',
        'priority': 10,  # Prioridad alta
        'search_patterns': [
            '/normas-aprobadas-',
            '/noticias/',
            '/comunicados/'
        ]
    },
    'isp': {
        'name': 'Instituto de Salud Pública',
        'base_url': 'https://www.ispch.gob.cl',
        'priority': 9,
        'search_patterns': [
            '/noticia/',
            '/comunicados/'
        ]
    },
    'mineria_chilena': {
        'name': 'Minería Chilena',
        'base_url': 'https://www.mch.cl',
        'priority': 8,
        'search_patterns': [
            '/negocios-industria/',
            '/noticias/'
        ]
    },
    'empresa_oceano': {
        'name': 'Empresa Océano',
        'base_url': 'https://www.empresaoceano.cl',
        'priority': 7,
        'search_patterns': [
            '/noticias/',
            '/puertos/'
        ]
    },
    'diario_oficial': {
        'name': 'Diario Oficial',
        'base_url': 'https://www.diariooficial.interior.gob.cl',
        'priority': 9,
        'search_patterns': [
            '/publicaciones/'
        ]
    },
    'bcn': {
        'name': 'Biblioteca del Congreso Nacional',
        'base_url': 'https://www.bcn.cl',
        'priority': 8,
        'search_patterns': [
            '/leychile/'
        ]
    }
}

# Configuración de filtros
FILTERS = {
    'min_relevance_score': 1,  # Mínimo score de relevancia para incluir artículo
    'exclude_domains': [
        'facebook.com',
        'twitter.com',
        'instagram.com',
        'linkedin.com',
        'youtube.com'
    ],
    'required_keywords_any': [  # Al menos una de estas palabras debe estar presente
        'ISO', 'norma', 'certificación', 'acreditación', 'INN'
    ],
    'exclude_keywords': [  # Excluir si contiene estas palabras
        'deportes', 'fútbol', 'música', 'entretenimiento'
    ]
}

# Configuración de salida JSON
JSON_OUTPUT = {
    'indent': 2,
    'ensure_ascii': False,
    'include_content': True,  # Incluir contenido completo de artículos
    'include_metadata': True,  # Incluir metadatos de búsqueda
    'generate_summary': True,  # Generar archivo resumen adicional
}

# Configuración de logging
LOGGING = {
    'level': 'INFO',  # DEBUG, INFO, WARNING, ERROR
    'format': '%(asctime)s - %(levelname)s - %(message)s',
    'save_to_file': True,
    'log_file': 'iso_scraper.log'
}

# Configuración de User-Agent para requests
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
]

# Configuración de selectores CSS para extracción de contenido
CSS_SELECTORS = {
    'title': [
        'h1', '.title', '.headline', '.entry-title', 
        '.article-title', '.post-title', 'title'
    ],
    'content': [
        '.content', '.article-content', '.entry-content',
        '.post-content', '.main-content', 'article',
        '.article-body', '.story-body', '.text-content'
    ],
    'date': [
        '.date', '.published', '.post-date', 'time', 
        '.entry-date', '.publication-date', '.article-date'
    ],
    'author': [
        '.author', '.by-author', '.post-author', 
        '.writer', '.byline', '.article-author'
    ]
}

# Configuración específica por mes (personalizable)
MONTHLY_CONFIGS = {
    'julio_2025': {
        'additional_queries': [
            'normas aprobadas julio 2025 Chile',
            'certificación ISO julio 2025 Chile',
            'INN julio 2025',
            'nuevas normas julio Chile'
        ],
        'date_filters': {
            'from': '2025-07-01',
            'to': '2025-07-31'
        }
    },
    'agosto_2025': {
        'additional_queries': [
            'normas aprobadas agosto 2025 Chile',
            'certificación ISO agosto 2025 Chile'
        ],
        'date_filters': {
            'from': '2025-08-01',
            'to': '2025-08-31'
        }
    }
}

# Función para obtener configuración personalizada
def get_config_for_month(month_year: str) -> dict:
    """
    Obtiene configuración específica para un mes
    
    Args:
        month_year (str): Mes y año en formato 'mes_año' (ej: 'julio_2025')
        
    Returns:
        dict: Configuración personalizada
    """
    base_config = {
        'queries': SEARCH_QUERIES.copy(),
        'keywords': ISO_KEYWORDS.copy(),
        'sources': KNOWN_SOURCES.copy(),
        'filters': FILTERS.copy()
    }
    
    if month_year in MONTHLY_CONFIGS:
        monthly = MONTHLY_CONFIGS[month_year]
        base_config['queries'].extend(monthly.get('additional_queries', []))
        base_config['date_filters'] = monthly.get('date_filters', {})
    
    return base_config

# Configuración de ejemplo para uso
EXAMPLE_USAGE = {
    'basic_search': {
        'days_back': 30,
        'max_articles': 5,
        'queries': ['ISO Chile', 'certificación ISO Chile']
    },
    'comprehensive_search': {
        'days_back': 60,
        'max_articles': 20,
        'queries': SEARCH_QUERIES
    },
    'monthly_report': {
        'days_back': 31,
        'max_articles': 15,
        'queries': get_config_for_month('julio_2025')['queries']
    }
}

