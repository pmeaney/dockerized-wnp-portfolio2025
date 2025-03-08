from django import forms
from django.utils.safestring import mark_safe

class TagCreationWidget(forms.Widget):
    """
    A custom widget that provides a modal-based tag creation workflow
    """
    template_name = 'wagtailadmin/widgets/tag_creation_widget.html'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    def render(self, name, value, attrs=None, renderer=None):
        # Import here to avoid circular import
        from .models import Tag
        
        # Check if any tags exist
        tags = Tag.objects.exists()
        
        # Prepare final attributes
        if attrs is None:
            attrs = {}
            
        final_attrs = self.build_attrs(attrs, {
            'name': name, 
            'multiple': 'multiple',
            'class': 'w-input w-select'
        })
        
        # Convert attributes to a string
        attrs_str = ' '.join(f'{k}="{v}"' for k, v in final_attrs.items())
        
        # Use the custom modal view URL
        tag_create_url = '/portfolio/tag-modal/'
        
        if not tags:
            # No tags exist - provide guidance to create first tag
            html = f"""
                <div class="tag-creation-guidance">
                    <p class="help">
                        <strong>Create Your First Tag</strong>
                    </p>
                    <div class="help-block">
                        <p>You need to create a tag before adding portfolio items.</p>
                        <button type="button" 
                                class="button button-small button-primary"
                                data-url="{tag_create_url}"
                                id="tag-add-button">
                            Create First Tag
                        </button>
                    </div>
                </div>
                <script>
                    document.addEventListener('DOMContentLoaded', function() {{
                        const addButton = document.getElementById('tag-add-button');
                        if (addButton) {{
                            addButton.addEventListener('click', function() {{
                                const url = this.getAttribute('data-url');
                                window.ModalWorkflow({{
                                    url: url,
                                    onload: {{
                                        'success': function(responseData) {{
                                            location.reload();
                                        }}
                                    }},
                                    responses: {{
                                        'success': function(responseData) {{
                                            location.reload();
                                        }}
                                    }}
                                }});
                            }});
                        }}
                    }});
                </script>
            """
            return mark_safe(html)
        
        # Generate options grouped by category
        category_types = dict(Tag.CATEGORY_CHOICES)
        options_html = ""
        
        for category_type, category_label in category_types.items():
            # Get tags for this category type
            category_tags = Tag.objects.filter(category=category_type)
            
            if category_tags.exists():
                group_options = ""
                
                for tag in category_tags:
                    is_selected = value and str(tag.pk) in [str(v) for v in value]
                    selected_attr = " selected" if is_selected else ""
                    group_options += f'<option value="{tag.pk}"{selected_attr}>{tag.value}</option>'
                
                # Add option group if there are tags
                if group_options:
                    options_html += f'<optgroup label="{category_label}">{group_options}</optgroup>'
        
        # Construct the full select HTML
        select_html = f"""
            <select {attrs_str}>
                {options_html}
            </select>
            <div class="tag-action-buttons" style="margin-top: 10px;">
                <button type="button" 
                        class="button button-small button-primary"
                        data-url="{tag_create_url}"
                        id="tag-add-button">
                    Add New Tag
                </button>
            </div>
            <script>
                document.addEventListener('DOMContentLoaded', function() {{
                    const addButton = document.getElementById('tag-add-button');
                    if (addButton) {{
                        addButton.addEventListener('click', function() {{
                            const url = this.getAttribute('data-url');
                            window.ModalWorkflow({{
                                url: url,
                                onload: {{
                                    'success': function(responseData) {{
                                        location.reload();
                                    }}
                                }},
                                responses: {{
                                    'success': function(responseData) {{
                                        location.reload();
                                    }}
                                }}
                            }});
                        }});
                    }}
                    
                    // Listen for messages from the modal iframe
                    window.addEventListener('message', function(event) {{
                        if (event.data && event.data.success && event.data.tag_id) {{
                            // Reload the page to show the newly created tag
                            location.reload();
                        }}
                    }});
                }});
            </script>
        """
        
        return mark_safe(select_html)
    
    def value_from_datadict(self, data, files, name):
        """
        Custom method to handle multiple select values
        """
        if isinstance(data, dict):
            return data.getlist(name)
        return []