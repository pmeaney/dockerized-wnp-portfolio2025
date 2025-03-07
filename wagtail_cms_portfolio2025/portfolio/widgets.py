from django import forms
from django.utils.safestring import mark_safe
from wagtail.admin.widgets import BaseChooser

class TagCreationWidget(forms.Widget):
    """
    A custom widget that provides a simplified tag creation workflow
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def render(self, name, value, attrs=None, renderer=None):
        # Import here to avoid circular import
        from .models import Tag
        
        # Check if any tags exist
        tags = Tag.objects.exists()
        
        if not tags:
            # No tags exist - provide guidance to create first tag
            return mark_safe(f'''
                <div class="tag-creation-guidance">
                    <p class="help">
                        <strong>Create Your First Tag</strong>
                    </p>
                    <div class="help-block">
                        <p>You need to create a tag before adding portfolio items.</p>
                        <a href="/admin/snippets/portfolio/tag/add/" 
                           class="button button-small button-primary"
                           data-wagtail-modal="true">
                            Create First Tag
                        </a>
                    </div>
                </div>
            ''')
        
        # If tags exist, render a custom multiple select widget
        if attrs is None:
            attrs = {}
        
        # Prepare the select element
        final_attrs = self.build_attrs(attrs, {
            'name': name, 
            'multiple': 'multiple',
            'class': 'w-input w-select'
        })
        
        # Generate options grouped by category
        category_types = dict(Tag.CATEGORY_CHOICES)
        options_html = []
        
        for category_type, category_label in category_types.items():
            # Get tags for this category type
            category_tags = Tag.objects.filter(category=category_type)
            
            if category_tags.exists():
                group_options = []
                
                for tag in category_tags:
                    is_selected = value and tag.pk in value
                    group_options.append(
                        f'<option value="{tag.pk}" {"selected" if is_selected else ""}>{tag.value}</option>'
                    )
                
                # Add option group if there are tags
                if group_options:
                    options_html.append(
                        f'<optgroup label="{category_label}">' + 
                        ''.join(group_options) + 
                        '</optgroup>'
                    )
        
        # Construct the full select HTML
        select_html = f'''
            <select {' '.join(f'{k}="{v}"' for k, v in final_attrs.items())}>
                {''.join(options_html)}
            </select>
            <div class="tag-action-buttons" style="margin-top: 10px;">
                <a href="/admin/snippets/portfolio/tag/add/" 
                   class="button button-small button-primary"
                   data-wagtail-modal="true">
                    Add New Tag
                </a>
            </div>
        '''
        
        return mark_safe(select_html)
    
    def value_from_datadict(self, data, files, name):
        """
        Custom method to handle multiple select values
        """
        return data.getlist(name)