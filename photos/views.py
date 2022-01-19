from django.shortcuts import render, redirect
from .models import Photo
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile


def gallery(request):
    # category = request.GET.get('category')

    # if category == None:
    #     photos = Photo.objects.all()
    # else:
    #     photos = Photo.objects.filter(category__name__contains=category)

    # categories = Category.objects.all()
    # context = {'categories': categories, 'photos': photos}
    photos = Photo.objects.all()
    context = {'photos': photos}
    return render(request, 'photos/gallery.html', context)


def viewPhoto(request, pk):
    photo = Photo.objects.get(id=pk)
    return render(request, 'photos/photo.html', {'photo': photo})


def addPhoto(request):
    # categories = Category.objects.all()

    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('image')

        # if data['category'] != 'none':
        #     category = Category.objects.get(id=data['category'])
        # elif data['category_new'] != '':
        #     category, created = Category.objects.get_or_create(
        #         name=data['category_new'])
        # else:
        #     category = None

        # compress the image here and then save it
        i = Image.open(image)
        i = i.convert('RGB')
        thumb_io = BytesIO()
        i.thumbnail((500, 500))
        i.save(thumb_io, format='JPEG', quality=50)
        inmemory_uploaded_file = InMemoryUploadedFile(
            thumb_io, None, 'foo.jpg', 'image/jpeg', thumb_io.tell(), None)

        photo = Photo.objects.create(
            # category=category,
            description=data['description'],
            # image=image,
            image=inmemory_uploaded_file
        )
        return redirect('gallery')

    # context = {'categories': categories}
    return render(request, 'photos/add.html')
