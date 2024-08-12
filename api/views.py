from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Bundle, Product
from .serializers import ProductDataSerializer
from .serializers import ProductListSerializer
from .ai_service import ProductBundleGenerator


@api_view(['GET'])
def recommend_bundles(request):
    static_products_data = {
            "products": [
                {
                    "id": 1,
                    "name": "Organic Avocado",
                    "description": "Fresh organic avocado from local farms.",
                    "price": "1.50",
                    "image_url": "http://example.com/images/avocado.jpg"
                },
                {
                    "id": 2,
                    "name": "Almond Butter",
                    "description": "Creamy almond butter, perfect for spreads and recipes.",
                    "price": "4.99",
                    "image_url": "http://example.com/images/almond_butter.jpg"
                },
                {
                    "id": 3,
                    "name": "Whole Wheat Bread",
                    "description": "Healthy whole wheat bread baked daily.",
                    "price": "2.79",
                    "image_url": "http://example.com/images/whole_wheat_bread.jpg"
                },
                {
                    "id": 4,
                    "name": "Greek Yogurt",
                    "description": "Rich and creamy Greek yogurt, high in protein.",
                    "price": "1.99",
                    "image_url": "http://example.com/images/greek_yogurt.jpg"
                },
                {
                    "id": 5,
                    "name": "Fresh Spinach",
                    "description": "Organic fresh spinach, perfect for salads and cooking.",
                    "price": "3.49",
                    "image_url": "http://example.com/images/fresh_spinach.jpg"
                },
                {
                    "id": 6,
                    "name": "Cage-Free Eggs",
                    "description": "Dozen cage-free eggs from free-range hens.",
                    "price": "2.99",
                    "image_url": "http://example.com/images/cage_free_eggs.jpg"
                },
                {
                    "id": 7,
                    "name": "Granola Bars",
                    "description": "Healthy granola bars with mixed nuts and dried fruit.",
                    "price": "5.49",
                    "image_url": "http://example.com/images/granola_bars.jpg"
                },
                {
                    "id": 8,
                    "name": "Almond Milk",
                    "description": "Unsweetened almond milk, a great dairy alternative.",
                    "price": "3.29",
                    "image_url": "http://example.com/images/almond_milk.jpg"
                },
                {
                    "id": 9,
                    "name": "Brown Rice",
                    "description": "Whole grain brown rice, ideal for a healthy diet.",
                    "price": "2.89",
                    "image_url": "http://example.com/images/brown_rice.jpg"
                },
                {
                    "id": 10,
                    "name": "Mixed Berries",
                    "description": "Frozen mixed berries, perfect for smoothies and desserts.",
                    "price": "4.29",
                    "image_url": "http://example.com/images/mixed_berries.jpg"
                }
            ]
    }

    products_data = static_products_data['products']
    generator = ProductBundleGenerator()

    try:
        # Generate recommended bundles using the AI model
        ai_bundles = generator.generate_bundles(products_data)

        if 'error' in ai_bundles:
            return Response(ai_bundles['error'], status=status.HTTP_400_BAD_REQUEST)

        return Response({'bundles': ai_bundles}, status=200)

    except Exception as e:
        return Response({'error': str(e)}, status=500)
