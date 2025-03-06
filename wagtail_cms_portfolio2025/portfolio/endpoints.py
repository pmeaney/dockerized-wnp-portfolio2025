from wagtail.api.v2.views import PagesAPIViewSet
from wagtail.api.v2.serializers import PageSerializer
from rest_framework import serializers
from .models import PortfolioItemPage

# Custom API endpoint for portfolio items
class PortfolioAPIViewSet(PagesAPIViewSet):
    # Only serve PortfolioItemPage pages
    model = PortfolioItemPage

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
        # Update these fields to match your model
        # If you don't have 'date' and 'intro' fields in your new model,
        # you should remove them or replace them with fields that exist
        'description',  # Changed from 'intro'
    ]

    # Custom fields to add to the API response
    body_fields = PagesAPIViewSet.body_fields + [
        'featured_image',  # Changed from 'thumbnail'
        'main_button_text',  # Changed from 'main_button_left_text'
        'secondary_button_text',  # Changed from 'secondary_button_right_text'
        'secondary_button_url',  # Changed from 'secondary_button_right_url'
    ]

    # Add portfolio tags to the API response
    def get_serializer(self, *args, **kwargs):
        serializer = super().get_serializer(*args, **kwargs)
        
        if kwargs.get('many', False):
            # This is a list serializer
            return serializer
            
        # Add a method field for tags
        serializer.fields['tags'] = serializers.SerializerMethodField()
        return serializer
        
    def get_tags(self, obj):
        tags = []
        for tag in obj.tags.all():
            tag_type = tag.tag_type
            type_name = tag_type.name if tag_type else 'default'
            
            tags.append({
                'tagValue': tag.name,
                'tagType': type_name,
                'tagCategory': tag_type.category_type if tag_type else 'default'  # Added this field
            })
            
        return tags