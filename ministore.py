#!/usr/bin/env python3
"""
Ministore Generator - Create shopping ministores with product recommendations
"""
import os
import requests
import mysql.connector
from typing import List, Dict, Optional
from datetime import datetime

class MinistoreGenerator:
    def __init__(self):
        self.serper_api_key = os.getenv('SERPER_API_KEY')
        self.base_url = os.getenv('BASE_URL', 'https://www.deanna2u.com')
        
        self.db_config = {
            'host': os.getenv('DB_HOST'),
            'user': os.getenv('DB_USERNAME'),
            'password': os.getenv('DB_PASSWORD'),
            'database': os.getenv('DB_DATABASE')
        }
        self.connection = None
    
    def connect(self):
        """Connect to MySQL database."""
        self.connection = mysql.connector.connect(**self.db_config)
        print('✓ Connected to database')
    
    def disconnect(self):
        """Disconnect from database."""
        if self.connection:
            self.connection.close()
            print('✓ Disconnected from database')
    
    def search_products(self, query: str, num_results: int = 10) -> List[Dict]:
        """Search for products using SerperDev API."""
        url = 'https://google.serper.dev/shopping'
        headers = {
            'X-API-KEY': self.serper_api_key,
            'Content-Type': 'application/json'
        }
        payload = {
            'q': query,
            'num': num_results,
            'gl': 'us'
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            products = []
            for item in data.get('shopping', []):
                products.append({
                    'title': item.get('title', ''),
                    'price': item.get('price', ''),
                    'link': item.get('link', ''),
                    'thumbnail': item.get('imageUrl', ''),
                    'source': item.get('source', '')
                })
            
            return products
        except Exception as e:
            print(f'Error searching products: {e}')
            return []
    
    def create_ministore(self, title: str, product_queries: List[str]) -> Optional[Dict]:
        """Create a ministore with products."""
        try:
            print(f'[MINISTORE] Starting creation: {title}')
            print(f'[MINISTORE] Product queries: {product_queries}')
            
            if not self.connection:
                print('[MINISTORE] Connecting to database...')
                self.connect()
            
            print('[MINISTORE] Database connected')
            cursor = self.connection.cursor(dictionary=True)
            
            # Create book (ministore)
            book_query = """
                INSERT INTO cliperest_book (name, created, modified, privacy, slug, rendered, version, addEnd, sharing, coverColor, dollarsGiven, type, numLikers, numClips, numViews, user_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # Generate unique slug (URL-safe: only letters, numbers, hyphens)
            import uuid
            import re
            slug_base = re.sub(r'[^a-z0-9]+', '-', title.lower()).strip('-')
            slug = f"{slug_base}-{uuid.uuid4().hex[:8]}"[:128]
            cursor.execute(book_query, (title, now, now, 0, slug, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 237))
            self.connection.commit()
            
            book_id = cursor.lastrowid
            print(f'[MINISTORE] ✓ Created ministore book/{book_id}')
            
            # Search and add products
            all_products = []
            for query in product_queries[:5]:  # Limit to 5 queries
                print(f'[MINISTORE] Searching: {query}')
                products = self.search_products(query, num_results=3)
                print(f'[MINISTORE] Found {len(products)} products for {query}')
                
                for product in products:
                    # Create clipping (product)
                    clipping_query = """
                        INSERT INTO cliperest_clipping 
                        (book_id, url, caption, text, thumbnail, created, modified, useThumbnail, type, num, migratedS3)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    note = f"Price: {product['price']}\nSource: {product['source']}"
                    
                    cursor.execute(clipping_query, (
                        book_id,
                        product['link'],
                        product['title'],
                        note,
                        product['thumbnail'],
                        now,
                        now,
                        1,
                        0,
                        len(all_products),
                        0
                    ))
                    all_products.append(product)
                
                self.connection.commit()
            
            # Update numClips count
            print(f'[MINISTORE] Updating numClips to {len(all_products)}')
            cursor.execute("UPDATE cliperest_book SET numClips = %s WHERE id = %s", (len(all_products), book_id))
            self.connection.commit()
            
            cursor.close()
            
            # Use username format with underscores
            username = "sofia_claudia_san_jose_bonoan"
            ministore_url = f"{self.base_url}/user/{username}/book/{slug}"
            
            return {
                'book_id': book_id,
                'url': ministore_url,
                'title': title,
                'num_products': len(all_products),
                'products': all_products
            }
            
        except Exception as e:
            print(f'[MINISTORE] ERROR: {type(e).__name__}: {str(e)}')
            import traceback
            print(f'[MINISTORE] Traceback:\n{traceback.format_exc()}')
            return None
