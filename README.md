To run the sample python code, just type:

```
python3 devil_pichu.py example.jpg
```

# a1-Report

### Injection :

We have achieved this through QR code generation. We read the correct answers text file and converted it into a QR code image using the QR code library. We take this image and inject the QR image in the right-most corner of the blank form by first shrinking it into a size 180 x 180. This size was experimented with and was the best to yield results despite any translations/variations the test images might have. This form with the injected QR is something that the students cannot decode to get the hint of correct answers. An example is given as such below :

![injected_form](https://media.github.iu.edu/user/24623/files/2d711b83-acb8-450e-93fd-d0de31875b8e)

### Extraction :

We get the answer form with the answers marked by the students. First, the QR code is extracted, which is straightforward as the QR code is injected with a hardcoded value of the size of the QR. This QR code is now decoded and extracted in an output text file.
Here is an example of the QR code extracted and the comparison of the ground truth file and the extracted text file from the QR :

![qr_code_ss](https://media.github.iu.edu/user/24623/files/8c8af06b-b0e6-48d9-af01-646a45742f8e)
![text_comparison](https://media.github.iu.edu/user/24623/files/b503a489-7a69-41c9-baaa-252d47858637)

## Experimented methods :

* Added codes in experimentation folder. File name corresponding to the methods mentioned inside the brackets.

### Detection : (avi_exp_devil_pichu.py)

Used contour detection using OpenCV, but avoided that method as it used openCV library.

Preprocessed the image using mean filter to reduce noise in the image and get rid of unncecessary artificats caused due to shading.
Used contour detection using PIL library to get the contours and formed sort of a bounding box kind of measure using some experimented thresholds to detect the shaded region. It did not turn out to be very accurate.

Sample Image as follows :

<img width="411" alt="detection_ss" src="https://media.github.iu.edu/user/24623/files/2f9232f6-9a5e-4fac-a277-b2474dc6b10e">

### Injection & Extraction : (avi_exp_inject_extract.py)

It was initially assumed that, somehow, the student sneaks into a QR code reader.
So, I tried to encrypt the file and put the encrypted text into the QR code, extract the QR code, extract the encrypted text, and decrypt it into the file.

Ground Truth File -> (encrypt) -> encrypted text -> (QR code generation) -> QR code -> (QR code reading) -> encrypted text -> (decrypt) -> we get the original file

Did not work out.
The encrypted text may not be in a QR-compatible format.
Verified that the encryption and decryption were working, and the QR generation was also working, but the decryption did not yield correct results.


## Contribution :

Avishmita :
* Tried some methods to do the detection.
* Able to do injection and extraction.


