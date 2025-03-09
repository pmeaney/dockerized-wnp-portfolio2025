from wagtail.api.v2.views import PagesAPIViewSet
from wagtail.api.v2.serializers import PageSerializer
from rest_framework import serializers
from wagtail.images.models import Image
from .models import PortfolioItem
import re
import logging

# Get logger
logger = logging.getLogger(__name__)

# Custom API endpoint for portfolio items
class PortfolioAPIViewSet(PagesAPIViewSet):
    # Only serve PortfolioItem pages
    model = PortfolioItem

    # Add custom fields
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['portfolio_list'] = True
        return context

    # Additional filters
    filter_backends = PagesAPIViewSet.filter_backends + [
        # Add any custom filters here
    ]

    # Custom meta fields
    meta_fields = PagesAPIViewSet.meta_fields + [
        'date',
        'intro',
    ]

    # Custom fields to add to the API response
    body_fields = PagesAPIViewSet.body_fields + [
        'body',
        'thumbnail',
        'main_button_text',
        'secondary_button_text',
        'secondary_button_url',
    ]

    # Extract image IDs from rich text content
    def extract_image_ids(self, rich_text):
        # Use regex to find all embed tags with embedtype="image"
        pattern = r'<embed\s+embedtype="image".*?id="(\d+)".*?>'
        return [int(id) for id in re.findall(pattern, rich_text)]

    # Add portfolio tags and embedded images to the API response
    def get_serializer(self, *args, **kwargs):
        serializer = super().get_serializer(*args, **kwargs)
        
        if hasattr(serializer, 'child'):
            # This is a list serializer
            child = serializer.child
            child.fields['tags'] = serializers.SerializerMethodField()
            child.fields['embedded_images'] = serializers.SerializerMethodField()
            
            # Add methods to the child serializer class
            child.__class__.get_tags = self.get_tags
            child.__class__.get_embedded_images = self.get_embedded_images
        elif hasattr(serializer, 'fields'):
            # This is a detail serializer
            serializer.fields['tags'] = serializers.SerializerMethodField()
            serializer.fields['embedded_images'] = serializers.SerializerMethodField()
            
            # Add methods to the serializer class
            serializer.__class__.get_tags = self.get_tags
            serializer.__class__.get_embedded_images = self.get_embedded_images
            
        return serializer
        
    def get_tags(self, obj):
        tags = []
        for portfolio_tag in obj.portfolio_tags.all():
            tag_obj = portfolio_tag.tag
            tag_type = tag_obj.tag_type
            
            type_name = tag_type.name if tag_type else 'default'
            style_class = tag_type.style if tag_type else 'is-info'
            
            tags.append({
                'tagValue': tag_obj.name,
                'tagType': type_name,
                'tagStyle': style_class
            })
            
        return tags
    
    def get_embedded_images(self, obj):
        # Get the rich text content
        rich_text = obj.body
        
        # Skip if body is empty
        if not rich_text:
            return []
            
        # Extract image IDs
        image_ids = self.extract_image_ids(rich_text)
        
        # Fetch image objects
        images = []
        for image_id in image_ids:
            try:
                # First check if the image exists in the database
                image = Image.objects.get(id=image_id)
                
                # Then try to access the file safely
                try:
                    original_url = image.get_rendition('original').url
                    thumbnail_url = image.get_rendition('fill-300x200').url
                    
                    # Success - add complete image data
                    image_data = {
                        'id': image_id,
                        'title': image.title,
                        'width': image.width,
                        'height': image.height,
                        'url': original_url,
                        'thumbnail': thumbnail_url,
                        'status': 'ok'
                    }
                except Exception as file_error:
                    # Image record exists but file is missing
                    logger.warning(f"Image file missing for ID {image_id}: {str(file_error)}")
                    image_data = {
                        'id': image_id,
                        'title': image.title,
                        'width': image.width if hasattr(image, 'width') else 0,
                        'height': image.height if hasattr(image, 'height') else 0,
                        'url': None,
                        'thumbnail': None,
                        'status': 'file_missing',
                        'error': 'Image file not found'
                    }
            except Image.DoesNotExist:
                # Image record doesn't exist in database
                logger.warning(f"Image with ID {image_id} not found in database")
                image_data = {
                    'id': image_id,
                    'title': 'Unknown Image',
                    'width': 0,
                    'height': 0,
                    'url': None,
                    'thumbnail': None,
                    'status': 'not_found',
                    'error': 'Image not found in database'
                }
            
            # Add the image data to our results
            images.append(image_data)
                
        return images