from wagtail.api.v2.views import PagesAPIViewSet
from wagtail.api.v2.serializers import PageSerializer
from rest_framework import serializers
from .models import PortfolioItem

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
        'thumbnail',
        'main_button_text',
        'secondary_button_text',
        'secondary_button_url',
    ]

    # Add portfolio tags to the API response
    def get_serializer(self, *args, **kwargs):
        serializer = super().get_serializer(*args, **kwargs)
        
        # Check if this is a list serializer or child serializer
        if hasattr(serializer, 'child'):
            # This is a list serializer, add field to the child serializer
            child = serializer.child
            child.fields['tags'] = serializers.SerializerMethodField()
            
            # Add the method to the child serializer class
            child.__class__.get_tags = self.get_tags
        elif hasattr(serializer, 'fields'):
            # This is a detail serializer, add field directly
            serializer.fields['tags'] = serializers.SerializerMethodField()
            
            # Add the method to the serializer class
            serializer.__class__.get_tags = self.get_tags
            
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