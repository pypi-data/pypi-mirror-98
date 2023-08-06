import pytest

from opennsfw_standalone import OpenNSFWInferenceRunner


@pytest.fixture(scope='session')
def inference_runner():
    return OpenNSFWInferenceRunner.load()


@pytest.mark.parametrize('image_path,nsfw_score', [
    ('./tests/data/sexy-1.jpg', 0.7386876),
    ('./tests/data/sexy-2.jpg', 0.3232846),
    ('./tests/data/sexy-3.jpg', 0.22978094),
    ('./tests/data/nude-1.jpg', 0.9975794),
    ('./tests/data/porn-1.jpg', 0.99944717),
    ('./tests/data/porn-2.jpg', 0.9273726),
    ('./tests/data/porn-3.jpg', 0.82202727),
    ('./tests/data/porn-4.jpg', 0.7710848),
    ('./tests/data/penis-1.jpg', 0.9059724),
    ('./tests/data/penis-2.jpg', 0.9972377),
    ('./tests/data/car-1.jpg', 0.00003827),
    ('./tests/data/car-2.jpg', 0.015770115),
    ('./tests/data/house-1.jpg', 0.00086330017),
    ('./tests/data/house-2.jpg', 0.06844018),
    ('./tests/data/phone-1.jpg', 0.00029372462),
    ('./tests/data/headphones-1.jpg', 0.0021593997),
    ('./tests/data/person-1.jpg', 0.000976563),
])
def test_inference_runner(image_path, nsfw_score, inference_runner):
    with open(image_path, 'rb') as fp:
        assert inference_runner.infer(fp.read()) == pytest.approx(nsfw_score, rel=1e-3)
