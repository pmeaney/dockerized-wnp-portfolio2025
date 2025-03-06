from django.db import models
from django import forms
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.snippets.models import register_snippet

# =========== Tag Models ===========

@register_snippet
class TagType(models.Model):
    """
    Model representing categories for portfolio tags.
    """
    name = models.CharField(max_length=255, help_text="Name of the tag type")
    slug = models.SlugField(unique=True, max_length=255, help_text="Unique identifier used in URLs")
    
    # Predefined categories to choose from
    CATEGORY_CHOICES = [
        ('year', 'Year'),
        ('language', 'Programming Language'),
        ('framework', 'Framework'),
        ('topic', 'Topic'),
        ('subtopic', 'Subtopic'),
        ('default', 'Default'),
    ]
    
    category_type = models.CharField(
        max_length=50, 
        choices=CATEGORY_CHOICES,
        default='default',
        help_text="The type of category this represents"
    )
    
    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
        FieldPanel('category_type'),
    ]
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Tag Type"
        verbose_name_plural = "Tag Types"
        ordering = ['name']


@register_snippet
class PortfolioTag(models.Model):
    """
    Model representing tags that can be applied to portfolio items.
    Each tag belongs to a specific tag type.
    """
    name = models.CharField(max_length=255, help_text="Name of the tag")
    slug = models.SlugField(unique=True, max_length=255, help_text="Unique identifier used in URLs")
    
    # Link to the tag type
    tag_type = models.ForeignKey(
        'TagType',
        on_delete=models.CASCADE,
        related_name='tags',
        help_text="The tag type this tag belongs to"
    )
    
    panels = [
        FieldPanel('name'),
        FieldPanel('slug'),
        FieldPanel('tag_type'),
    ]
    
    def __str__(self):
        return f"{self.name} ({self.tag_type.name})"
    
    class Meta:
        verbose_name = "Portfolio Tag"
        verbose_name_plural = "Portfolio Tags"
        ordering = ['tag_type', 'name']


# =========== Page Models ===========

class PortfolioItemPage(Page):
    """
    Individual portfolio project page with updated button fields.
    """
    description = RichTextField(blank=True)
    
    # Featured image
    featured_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    
    # Updated button fields
    main_button_text = models.CharField(
        max_length=50,
        blank=False,  # Making it required
        help_text="Text for the main call-to-action button"
    )
    
    # Secondary button fields with renamed names
    secondary_button_text = models.CharField(
        max_length=50,
        blank=True,
        help_text="Text for the secondary button (optional)"
    )
    
    secondary_button_url = models.URLField(
        blank=True,
        help_text="URL for the secondary button"
    )
    
    # Tags field to connect with portfolio tags
    tags = models.ManyToManyField(
        'PortfolioTag',
        blank=True,
        related_name='portfolio_pages'
    )
    
    content_panels = Page.content_panels + [
        FieldPanel('description'),
        FieldPanel('featured_image'),
        MultiFieldPanel([
            FieldPanel('main_button_text'),
            FieldPanel('secondary_button_text'),
            FieldPanel('secondary_button_url'),
        ], heading="Buttons"),
        FieldPanel('tags', widget=forms.CheckboxSelectMultiple),
    ]
    
    def get_main_button_url(self):
        """Returns the page slug to use as the main button URL"""
        return self.slug
    
    def get_context(self, request):
        context = super().get_context(request)
        # Add the main button URL to the context
        context['main_button_url'] = self.get_main_button_url()
        return context
    
    class Meta:
        verbose_name = "Portfolio Item"
        verbose_name_plural = "Portfolio Items"
