#!/usr/bin/env python3
"""
Conversation Analyzer - Extract product recommendations from text
"""
import re
from typing import List

class ConversationAnalyzer:
    BRANDS = [
        'zara', 'h&m', 'hm', 'mango', 'nike', 'adidas', 'levi', "levi's",
        'uniqlo', 'gap', 'forever 21', 'asos', 'sephora', 'ulta',
        'anthropologie', 'everlane', 'allbirds', 'glossier'
    ]
    
    PRODUCT_TYPES = [
        'shirt', 'blouse', 'top', 'dress', 'skirt', 'pants', 'jeans',
        'jacket', 'blazer', 'coat', 'sweater', 'hoodie',
        'shoes', 'sneakers', 'boots', 'heels', 'sandals',
        'bag', 'purse', 'backpack', 'jewelry', 'necklace', 'earrings',
        'sunglasses', 'belt', 'scarf', 'hat', 'watch', 'bracelet'
    ]
    
    RECOMMENDATION_PHRASES = [
        'recommend', 'suggest', 'try', 'check out', 'perfect', 'love',
        'great option', 'obsessed', 'favorite', 'you should', 'go for',
        'pair with', 'from', 'at', 'looking for', 'need', 'want'
    ]
    
    @staticmethod
    def extract_products(conversation_text: str) -> List[str]:
        """Extract product search queries from conversation."""
        products = []
        lines = conversation_text.split('\n')
        
        for line in lines:
            line_lower = line.lower()
            
            # Check if line contains recommendation language or shopping intent
            has_recommendation = any(phrase in line_lower for phrase in ConversationAnalyzer.RECOMMENDATION_PHRASES)
            
            if not has_recommendation:
                continue
            
            # Extract brand
            found_brand = next((brand for brand in ConversationAnalyzer.BRANDS if brand in line_lower), None)
            
            # Extract product types
            found_products = [ptype for ptype in ConversationAnalyzer.PRODUCT_TYPES if ptype in line_lower]
            
            # Create search queries
            if found_brand and found_products:
                for product in found_products:
                    query = f"{found_brand} {product}"
                    if query not in products:
                        products.append(query)
            elif found_products:
                # Just product type without brand
                for product in found_products:
                    if product not in products:
                        products.append(product)
        
        return products[:10]  # Limit to 10 products
    
    @staticmethod
    def should_create_ministore(conversation_text: str, min_recommendations: int = 3) -> bool:
        """Check if conversation has enough product recommendations to create a ministore."""
        products = ConversationAnalyzer.extract_products(conversation_text)
        return len(products) >= min_recommendations
