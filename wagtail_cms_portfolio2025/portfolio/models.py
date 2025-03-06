from django.db import models
from django import forms
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, MultiFieldPanel
from wagtail.snippets.models import register_snippet
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

# =========== Tag Models ===========
# testing
@register_snippet
class TagCategory(models.Model):
    """
    Model for tag categories in the portfolio system.
    Each tag will belong to one of these predefined categories.
    """
    name = models.CharField(max_length=100, help_text="Display name for this tag category")
    
    # Predefined categories
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
        help_text="The category this tag represents"
    )
    
    panels = [
        FieldPanel('name'),
        FieldPanel('category_type'),
    ]
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Tag Category"
        verbose_name_plural = "Tag Categories"


@register_snippet
class PortfolioTag(models.Model):
    """
    Tags that can be applied to portfolio items.
    Each tag belongs to a specific category.
    """
    name = models.CharField(max_length=255, help_text="The tag name/value")
    
    # Link to the tag category
    category = models.ForeignKey(
        'TagCategory',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='tags',
        help_text="The category this tag belongs to"
    )
    
    panels = [
        FieldPanel('name'),
        FieldPanel('category'),
    ]
    
    def __str__(self):
        category_type = self.category.category_type if self.category else "default"
        return f"{self.name} ({category_type})"
    
    class Meta:
        verbose_name = "Portfolio Tag"
        verbose_name_plural = "Portfolio Tags"


# =========== Portfolio Item Model ===========

class PortfolioItem(Page):
    """
    Individual portfolio project page with updated button fields.
    """
    date = models.DateField("Post date")
    intro = models.CharField(max_length=250)
    body = RichTextField(blank=True)
    
    # Featured image (thumbnail)
    thumbnail = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    
    # Button fields
    main_button_text = models.CharField(
        max_length=50,
        blank=False,  # Making it required
        help_text="Text for the main call-to-action button"
    )
    
    secondary_button_text = models.CharField(
        max_length=50,
        blank=True,
        help_text="Text for the secondary button (optional)"
    )
    
    secondary_button_url = models.URLField(
        blank=True,
        help_text="URL for the secondary button"
    )
    
    # Tags - using ParentalManyToManyField to simplify the relationship
    tags = models.ManyToManyField(
        'PortfolioTag',
        blank=True,
        through='PortfolioTagItem',
        related_name='portfolio_items'
    )
    
    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('intro'),
        FieldPanel('body'),
        FieldPanel('thumbnail'),
        MultiFieldPanel([
            FieldPanel('main_button_text'),
            FieldPanel('secondary_button_text'),
            FieldPanel('secondary_button_url'),
        ], heading="Buttons"),
        FieldPanel('tags', widget=forms.CheckboxSelectMultiple),
    ]
    
    # This restricts where this page type can be created
    parent_page_types = ['portfolio.PortfolioIndexPage']
    
    # This prevents any page types from being created beneath portfolio items
    subpage_types = []

    def get_main_button_url(self):
        """Returns the page slug to use as the main button URL"""
        return self.slug
    
    class Meta:
        verbose_name = "Portfolio Item"
        verbose_name_plural = "Portfolio Items"


class PortfolioTagItem(models.Model):
    """
    The through model for linking tags to portfolio items.
    """
    tag = models.ForeignKey(
        'PortfolioTag',
        on_delete=models.CASCADE,
        related_name='+'
    )
    
    portfolio_item = ParentalKey(
        'PortfolioItem',
        on_delete=models.CASCADE,
        related_name='portfolio_tags'
    )
    
    panels = [
        FieldPanel('tag'),
    ]
    
    class Meta:
        unique_together = ('tag', 'portfolio_item')


# =========== Portfolio Index Page ===========

class PortfolioIndexPage(Page):
    """
    Index page for listing portfolio items.
    """
    intro = RichTextField(blank=True)
    
    content_panels = Page.content_panels + [
        FieldPanel('intro')
    ]

    # This restricts what page types can be created beneath this index page
    subpage_types = ['portfolio.PortfolioItem']
    
    
    
    class Meta:
        verbose_name = "Portfolio Index Page"
        verbose_name_plural = "Portfolio Index Pages"
    
    def get_context(self, request):
        context = super().get_context(request)
        context['portfolio_items'] = PortfolioItem.objects.child_of(self).live().order_by('-date')
        return context