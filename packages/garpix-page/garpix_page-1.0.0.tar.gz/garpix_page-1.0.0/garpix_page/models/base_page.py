from django.utils.functional import cached_property
from django.db import models
from django.utils import translation
from django.conf import settings
from django.utils.module_loading import import_string
from django.contrib.sites.models import Site
from django.contrib.sites.managers import CurrentSiteManager
from garpix_page.utils.get_file_path import get_file_path
from polymorphic_tree.models import PolymorphicMPTTModel, PolymorphicTreeForeignKey, PolymorphicMPTTModelManager


class GCurrentSiteManager(CurrentSiteManager):
    use_in_migrations = False


class BasePage(PolymorphicMPTTModel):
    """
    Базовая страница, на основе которой создаются все прочие страницы.
    """
    title = models.CharField(max_length=255, verbose_name='Название')
    is_active = models.BooleanField(default=True, verbose_name='Включено')
    display_on_sitemap = models.BooleanField(default=True, verbose_name='Отображать в карте сайта')
    slug = models.SlugField(max_length=150, verbose_name='ЧПУ', blank=True, default='')
    sites = models.ManyToManyField(Site, verbose_name='Сайты для отображения')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    seo_title = models.CharField(max_length=250, verbose_name='SEO заголовок страницы (title)', blank=True, default='')
    seo_keywords = models.CharField(max_length=250, verbose_name='SEO ключевые слова (keywords)', blank=True,
                                    default='')
    seo_description = models.TextField(verbose_name='SEO описание (description)', blank=True, default='')
    seo_author = models.CharField(max_length=250, verbose_name='SEO автор (author)', blank=True, default='')
    seo_og_type = models.CharField(max_length=250, verbose_name='SEO og:type', blank=True, default="website")
    seo_image = models.FileField(upload_to=get_file_path, blank=True, null=True, verbose_name='SEO изображение')
    parent = PolymorphicTreeForeignKey('self', null=True, blank=True, related_name='children',
                                       db_index=True, verbose_name='Родительская страница', on_delete=models.SET_NULL,
                                       limit_choices_to={})
    page_type = models.CharField(default='DEFAULT', max_length=25, verbose_name='Тип страницы',
                                 choices=settings.CHOICES_PAGE_TYPES)

    # objects = models.Manager()
    objects = PolymorphicMPTTModelManager()
    on_site = GCurrentSiteManager()

    class Meta(PolymorphicMPTTModel.Meta):
        verbose_name = 'Структура страниц'
        verbose_name_plural = 'Структура страниц'
        ordering = ('created_at', 'title',)

    def __str__(self):
        return self.title

    def get_verbose_model_name(self):
        return self._meta.verbose_name

    get_verbose_model_name.short_description = 'Название модели'

    def get_absolute_url(self):
        return self.absolute_url

    get_absolute_url.short_description = 'URL'

    @cached_property
    def absolute_url(self):
        current_language_code_url_prefix = translation.get_language()
        try:
            use_default_prefix = settings.USE_DEFAULT_LANGUAGE_PREFIX
        except:  # noqa
            use_default_prefix = True
        if not use_default_prefix and current_language_code_url_prefix == settings.LANGUAGE_CODE:
            current_language_code_url_prefix = ''
        elif current_language_code_url_prefix is None:
            current_language_code_url_prefix = ''
        else:
            current_language_code_url_prefix = '/' + current_language_code_url_prefix

        if self.slug:
            obj = self
            url_arr = [self.slug]
            while obj.parent is not None:
                obj = obj.parent
                if obj.slug:
                    url_arr.insert(0, obj.slug)
            return "{}/{}".format(current_language_code_url_prefix, '/'.join(url_arr))
        return "{}".format(current_language_code_url_prefix) if len(current_language_code_url_prefix) > 1 else '/'

    absolute_url.short_description = 'URL'

    @cached_property
    def get_sites(self):
        res = 'n/a'
        if self.sites.all().count() > 0:
            res = ''
            for site in self.sites.all():
                res += f'{site.domain} '
        return res

    get_sites.short_description = 'Sites'

    @cached_property
    def template(self):
        return settings.PAGE_TYPES[self.page_type]['template']

    def get_context(self, request=None, *args, **kwargs):
        context_function = import_string(settings.PAGE_TYPES[self.page_type]['context'])
        return context_function(request, *args, **kwargs)

    @classmethod
    def is_for_page_view(cls):
        return True

    def get_breadcrumbs(self):
        result = []
        obj = self
        result.append(obj)
        while obj.parent is not None:
            result.insert(0, obj.parent)
            obj = obj.parent
        return result
