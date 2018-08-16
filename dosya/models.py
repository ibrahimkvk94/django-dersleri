from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from ckeditor.fields import RichTextField

# Create your models here.

class Dosya(models.Model):
    user = models.ForeignKey('auth.User', verbose_name="Yazar", related_name='dosyas')
    baslik = models.CharField(max_length=120, verbose_name='Başlık')
    tarih = models.DateField(verbose_name='Tarih',auto_now_add=True)
    slug = models.SlugField(unique=True,editable=False,max_length=130)
    look = models.IntegerField(verbose_name="like",default =1)

    def __str__(self):
        return self.baslik

    def get_absolute_url(self):
        return reverse('dosya:detay', kwargs={'slug': self.slug})

    def get_unique_slug(self):
        slug = slugify(self.baslik.replace('ı','i'))
        unique_slug = slug
        counter = 1
        while Dosya.objects.filter(slug=unique_slug).exists():
            unique_slug = '{}-{}'.format(slug,counter)
            counter +=1
        return unique_slug

    def save(self, *args,**kwargs):
        self.slug = self.get_unique_slug()
        return super(Dosya, self).save(*args,**kwargs)

    class Meta:
        ordering =['-tarih', '-id']
