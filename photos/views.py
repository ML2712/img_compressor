from django.shortcuts import render, redirect
from .models import Photo
from io import BytesIO
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile


def gallery(request):
    photos = Photo.objects.all()
    context = {'photos': photos}
    return render(request, 'photos/gallery.html', context)


def viewPhoto(request, pk):
    photo = Photo.objects.get(id=pk)
    return render(request, 'photos/photo.html', {'photo': photo})


def addPhoto(request):
    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('image')

        # compress the image and then save it
        i = Image.open(image)
        i = i.convert('RGB')
        thumb_io = BytesIO()
        i.thumbnail((500, 500))
        i.save(thumb_io, format='JPEG', quality=50)
        inmemory_uploaded_file = InMemoryUploadedFile(
            thumb_io, None, 'foo.jpg', 'image/jpeg', thumb_io.tell(), None)

        photo = Photo.objects.create(
            description=data['description'],
            image=inmemory_uploaded_file
        )
        return redirect('gallery')

    return render(request, 'photos/add.html')
