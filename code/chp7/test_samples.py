import os
from PIL import Image
from csv import reader
from chp7.register import ocr
from chp7.image_processing import img_to_bw

SAMPLES_DIR = os.path.join(
    os.path.dirname(os.path.realpath(__file__)),
    '..', '..', 'data', 'captcha_samples')


def get_rdr(samples_folder=SAMPLES_DIR):
    return reader(open(os.path.join(samples_folder, 'samples.csv')))


def test_samples(samples_folder=SAMPLES_DIR):
    rdr = get_rdr(samples_folder=samples_folder)
    results = {'correct': 0, 'incorrect': 0}
    for fname, txt in rdr:
        img = Image.open(os.path.join(samples_folder, fname))
        captcha = ocr(img)
        if captcha == txt:
            results['correct'] += 1
        else:
            results['incorrect'] += 1
    print('accuracy: {}%'.format(results['correct'] / 100.0))
    print('results: ', results)
    return results

if __name__ == '__main__':
    test_samples()
