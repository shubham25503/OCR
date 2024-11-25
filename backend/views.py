import easyocr,os
import cv2
from django.conf import settings
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage

class HomePage(TemplateView):
    template_name = 'index.html'

def upload_image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        uploaded_image = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(uploaded_image.name, uploaded_image)
        uploaded_file_url = fs.url(filename)
        request.session['image_url'] = uploaded_file_url  # Store in session
        return redirect('show_image')  # Redirect to the page that displays the image

    return render(request, 'index.html')

class ShowImageView(TemplateView):
    template_name = 'show_image.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        image_url = self.request.session.get('image_url')

        # Convert web URL to local file path
        image_path = os.path.join(settings.MEDIA_ROOT, image_url.replace(settings.MEDIA_URL, ''))

        # Load the image using OpenCV and resize
        img = cv2.imread(image_path)

        # Perform OCR on the resized image using EasyOCR
        reader = easyocr.Reader(['en'])
        ocr_results = reader.readtext(img)
        # print(ocr_results)
        recognized_text = [(result[1], result[2]) for result in ocr_results]
        context['image_url'] = image_url
        context['recognized_text'] = recognized_text

        # Draw rectangles around the detected text regions
        for result in ocr_results:
            # print(result)
            coords = result[0]
            x1, y1 = map(int, coords[0])  # Top-left corner
            x2, y2 = map(int, coords[2])  # Bottom-right corner
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)

        # Print the shape of the image
        print("Image shape:", img.shape)
        # Save the image with rectangles (optional)
        rect_image_path = os.path.join(settings.MEDIA_ROOT, 'rect_' + os.path.basename(image_path))
        cv2.imwrite(rect_image_path, img)

        context['rect_image_url'] = settings.MEDIA_URL + os.path.basename(rect_image_path)

        return context
