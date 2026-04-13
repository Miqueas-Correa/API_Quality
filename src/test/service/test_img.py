import io
import numpy as np
from PIL import Image
from src.service.img_service import quality_image

class TestQualityImage:
    def test_quality_image_returns_bytes(self, test_image_file):
        result = quality_image(test_image_file, 'png')
        assert isinstance(result, bytes)
        assert len(result) > 0

    def test_quality_image_doubles_dimensions(self, test_image_file):
        test_image_file.seek(0)
        original_img = Image.open(test_image_file)
        original_width, original_height = original_img.size

        test_image_file.seek(0)
        result = quality_image(test_image_file, 'png')
        result_img = Image.open(io.BytesIO(result))
        result_width, result_height = result_img.size

        assert result_width == original_width * 2
        assert result_height == original_height * 2

    def test_quality_image_jpeg_extension(self, test_image_file):
        test_image_file.seek(0)
        result = quality_image(test_image_file, 'jpeg')
        result_img = Image.open(io.BytesIO(result))
        assert result_img.format == 'JPEG'

    def test_quality_image_png_extension(self, test_image_file):
        test_image_file.seek(0)
        result = quality_image(test_image_file, 'png')
        result_img = Image.open(io.BytesIO(result))
        assert result_img.format == 'PNG'

    def test_quality_image_jpg_extension(self, test_image_file):
        test_image_file.seek(0)
        result = quality_image(test_image_file, 'jpg')
        result_img = Image.open(io.BytesIO(result))
        assert result_img.format == 'JPEG'

    def test_quality_image_webp_extension(self, test_image_file):
        test_image_file.seek(0)
        result = quality_image(test_image_file, 'webp')
        result_img = Image.open(io.BytesIO(result))
        assert result_img.format == 'WEBP'

    def test_quality_image_small_image(self):
        img = Image.new('RGB', (10, 10), color='green')
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        result = quality_image(buffer, 'png')
        assert isinstance(result, bytes)
        assert len(result) > 0

    def test_quality_image_color_adjustments(self):
        img = Image.new('RGB', (50, 50), color=(100, 150, 200))
        buffer = io.BytesIO()
        img.save(buffer, format='PNG')
        buffer.seek(0)
        result = quality_image(buffer, 'png')
        result_img = Image.open(io.BytesIO(result))
        result_array = np.array(result_img)
        assert result_array.shape == (100, 100, 3)