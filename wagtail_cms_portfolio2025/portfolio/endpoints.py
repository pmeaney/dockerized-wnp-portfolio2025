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
        'main_button_left_text',
        'main_button_left_url',
        'secondary_button_right_text',
        'secondary_button_right_url',
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
        # Add regular tags
        for tag in obj.tags.all():
            tags.append({
                'name': tag.name,
                'style': 'is-default',
                'url': None
            })
        
        # Add portfolio-specific tags with styles
        for portfolio_tag in obj.portfolio_tags.all():
            tag_obj = portfolio_tag.tag
            tag_type = tag_obj.tag_type
            style = tag_type.style if tag_type else 'is-default'
            
            tags.append({
                'name': tag_obj.name,
                'style': style, 
                'url': None
            })
            
        return tags