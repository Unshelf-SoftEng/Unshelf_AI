from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Bundle, Product
from .ai_service import generate_bundles
from .serializers import BundleSerializer
from .serializers import ProductListSerializer


@api_view(['POST'])
def recommend_bundles(request):
    serializer = ProductListSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=400)

    products_data = serializer.validated_data['products']

    if not products_data:
        return Response({'error': 'Product data is required'}, status=400)

    try:
        # Generate recommended bundles using the AI model
        ai_bundles = generate_bundles(products_data)

        # Create or update bundles in the database
        recommended_bundles = []
        for bundle_data in ai_bundles:
            bundle_id = bundle_data['bundle_id']
            bundle_name = bundle_data['name']

            bundle, created = Bundle.objects.update_or_create(
                id=bundle_id,
                defaults={
                    'name': bundle_name,
                    'description': bundle_data['description'],
                    'discount_percentage': bundle_data['discount_percentage']
                }
            )

            for product_data in bundle_data['products']:
                product, _ = Product.objects.update_or_create(
                    id=product_data['id'],
                    defaults={
                        'name': product_data['name'],
                        'description': product_data['description'],
                        'price': product_data['price'],
                        'image_url': product_data['image_url']
                    }
                )
                bundle.products.add(product)

            recommended_bundles.append(bundle)

        serializer = BundleSerializer(recommended_bundles, many=True)
        return Response(serializer.data)
    except Exception as e:
        return Response({'error': str(e)}, status=500)