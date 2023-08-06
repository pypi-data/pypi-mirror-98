import numpy as np
import pkg_resources
import tensorflow as tf

from tensorflow.python.saved_model import signature_constants, tag_constants


class OpenNSFWInferenceRunner:
    """Performs inference against Yahoo's OpenNSFW model."""

    def __init__(self, model) -> None:
        self._model = model
        self._infer = model.signatures[signature_constants.DEFAULT_SERVING_SIGNATURE_DEF_KEY]

    @classmethod
    def load(
        cls,
        model_path: str = pkg_resources.resource_filename(__name__, "model/"),
    ):
        """Initialzies the classifier by loading the model from disk and
        preparing it for inference."""

        model = tf.saved_model.load(model_path, tags=[tag_constants.SERVING])
        return cls(model)

    def infer(self, image_data: bytes) -> float:
        """Classifies the the specified image.

        Arguments:
            image_data:
                JPEG/PNG/BMP/WEBP data to classify.

        Returns:
            A tuple of SFW/NSFW score.
        """

        image = self._preprocess_image(image_data)

        outputs = self._infer(tf.constant(image))
        scores = tf.get_static_value(outputs[signature_constants.PREDICT_OUTPUTS])

        return scores[0][1]

    @staticmethod
    def _preprocess_image(image_data: bytes) -> np.array:
        """Loads and and pre-processes the specified image for the model.

        Approximation of: https://github.com/yahoo/open_nsfw/blob/a4e13931465f4380742545932657eeea0a10aa48/classify_nsfw.py#L40
        """

        image = tf.image.decode_image(image_data)
        image = tf.image.convert_image_dtype(image, tf.float32, saturate=True)
        image = tf.image.resize(image, (256, 256), method=tf.image.ResizeMethod.BILINEAR)
        image = tf.image.convert_image_dtype(image, tf.uint8, saturate=True)

        image = tf.image.encode_jpeg(
            image,
            format="",
            quality=75,
            progressive=False,
            optimize_size=False,
            chroma_downsampling=True,
            density_unit=None,
            x_density=None,
            y_density=None,
            xmp_metadata=None,
        )

        image = tf.image.decode_jpeg(
            image, channels=3, fancy_upscaling=False, dct_method="INTEGER_ACCURATE"
        )

        image = tf.cast(image, dtype=tf.float32)
        image = tf.image.crop_to_bounding_box(image, 16, 16, 224, 224)
        image = tf.reverse(image, axis=[2])

        # Extracted from: https://github.com/yahoo/open_nsfw/blob/79f77bcd45076b000df71742a59d726aa4a36ad1/classify_nsfw.py#L114
        image -= [104, 117, 123]

        return np.expand_dims(image.numpy(), axis=0)
