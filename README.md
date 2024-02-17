# B657 Assignment 1: Image Processing and Recognition Basics

## Grading
```
python3 grade.py form.jpg output.txt
```
### Initial Attempts
To detect the answers from an exam sheet, the initial idea was to use Hough Transform. The idea was to perform egde detection first then scan through the image until edges are found in order to extract the coordinates of different answer boxes. The Hough Transform method was a bit slow since it was scanning the image almost pixel by pixel. It also resulted in overlapping lines as it was sensitive to colored answer boxes and to the proximity of the boxes. Another attempt was to estimate coordinates/lines within which the answer boxes fall. However, this approach was too static and standard as it was sensitive to noisy edges and to variations in scanned exam sheets. 

### Grading Solution
The adopted solution involves extracting answers out of each individual question instance on the sheet. After running edge detection on the exam sheet, thresholding was used to identify the horizontal and vertical sections encompassing questions and their corresponding answer boxes. Erosion and dilation were used make the sections more pronounced. The point of crossing between the horizontal and vertical sections spots and segregates answer boxes. Starting from the coordinates of the top left point, the coordinates of the three question regions of the exam sheet as well as the x-coordinates of the answer boxes were identified. To account for variations and slight transformations across the scanned exam sheets and also for scribbling, if any, prior to questions, safety margins were kept around each region. Note that the approximation process of the coordinates of the different regions was based on trial-and-error and testing. This implies that the exam sheets being scanned for grading should have comparable orientation and dimensions to the images used for testing.  
With the question regions and the answer boxes' coordinates in place, from every region's row, a question and its answer boxes are highlighted. A vertical filter of ones is used to create patches; if a the result of the convolution along a column of pixels is not black, it is part of the patch. This allows to capture any scribling prior to questions as well as the answer boxes. Finally, the intensities of the answer patches are evaluated to detect marked answers.  

#### Accuracy
Assuming that the provided test images encompass all the variances the grader would have to handle, its performance on the images is very good. The **grader_accuracy** program assesses its accuracy on 5 test images. It is 99.76% accurate.

#### Future work
As the current solution is tailored to a particular type of exam sheets resembling the provided test images, a more robust approach is desirable to handle variations and noise effectively. Employing OpenCV or neural networks for answer detection and extraction would constitute a stronger and more versatile solution.

## Answer Injection and Extraction
### Injection

We have achieved this through QR code generation. We read the correct answers text file and converted it into a QR code image using the QR code library. We take this image and inject the QR image in the right-most corner of the blank form by first shrinking it into a size 180 x 180. This size was experimented with and was the best to yield results despite any translations/variations the test images might have. This form with the injected QR is something that the students cannot decode to get the hint of correct answers. An example is given as such below :

![injected_form](https://media.github.iu.edu/user/24623/files/2d711b83-acb8-450e-93fd-d0de31875b8e)

### Extraction

We get the answer form with the answers marked by the students. First, the QR code is extracted, which is straightforward as the QR code is injected with a hardcoded value of the size of the QR. This QR code is now decoded and extracted in an output text file.
Here is an example of the QR code extracted and the comparison of the ground truth file and the extracted text file from the QR :

![qr_code_ss](https://media.github.iu.edu/user/24623/files/8c8af06b-b0e6-48d9-af01-646a45742f8e)
![text_comparison](https://media.github.iu.edu/user/24623/files/b503a489-7a69-41c9-baaa-252d47858637)

### Experimented methods

* Added codes in experimentation folder. File name corresponding to the methods mentioned inside the brackets.

### Detection: (avi_exp_devil_pichu.py)

Used contour detection using OpenCV, but avoided that method as it used openCV library.

Preprocessed the image using mean filter to reduce noise in the image and get rid of unncecessary artificats caused due to shading.
Used contour detection using PIL library to get the contours and formed sort of a bounding box kind of measure using some experimented thresholds to detect the shaded region. It did not turn out to be very accurate.

Sample Image as follows :

<img width="411" alt="detection_ss" src="https://media.github.iu.edu/user/24623/files/2f9232f6-9a5e-4fac-a277-b2474dc6b10e">

### Injection & Extraction: (avi_exp_inject_extract.py)

It was initially assumed that, somehow, the student sneaks into a QR code reader.
So, I tried to encrypt the file and put the encrypted text into the QR code, extract the QR code, extract the encrypted text, and decrypt it into the file.

Ground Truth File -> (encrypt) -> encrypted text -> (QR code generation) -> QR code -> (QR code reading) -> encrypted text -> (decrypt) -> we get the original file

Did not work out.
The encrypted text may not be in a QR-compatible format.
Verified that the encryption and decryption were working, and the QR generation was also working, but the decryption did not yield correct results.


#### grid.py
Using matplotlib, this code scans an image and applies a grid overlay with dx and dy pixel spacing. Then, it performs Optical Character Recognition (OCR) on each grid cell to retrieve text using the Pytesseract package. Matplotlib is used to display the altered image with the grid overlay; the grid crossings are indicated by red dots. By uncommenting the print statement, the OCR results can be printed even though they are not shown in the output. We were thinking of using grids to locate the marked answers, question numbers and text in front of questions using the text in grids in the OMR sheet.

#### img_seg.py
When the idea of grid did not work we tried doing image segmentation(marking the marked options by red). If an image is in color, this code reads it and turns it to grayscale. After that, it uses Otsu's thresholding to produce a binary image, and it cleans it up by doing morphological closing and border clearing. After the image has been cleaned, each identified region is labeled, and bounding boxes are created around it using regionprops. Matplotlib is used to display the original image with bounding boxes superimposed, and the number of detected regions is printed. The segmented areas of the image are highlighted by the red bounding boxes.

#### overlay.py
We thought of overlaying the OMR marked by student and Blank_form injected with the correct answer. Using this image to grade(in percentage), but we scrapped the idea as it was not required by the question.

After implementing grids and image segmentation we moved to other method to solve the grading part.

#### barcode_encode.py
We tried to use a barcode to inject a URL into the barcode after uploading the image to imgur.

#### barcode_decode.py
We tried to extract the information from the barcode(URL) using selenium. It then uses the requests library and PIL (Python Imaging Library) to fetch and display the image from the extracted URL. The code runs the WebDriver in headless mode, meaning it operates without opening a visible browser window. This did not work due to difficulty in retrieving the image so we used QR code.

#### inject.py
Injecting correct answers into the blank form. This code extracts the right answers for an OMR-based test from a text file and an image of a blank OMR sheet. The correct_bubble function, which uses the question number, response letter, and other parameters to find and fill the correct bubble in black, is then used to mark the correct bubbles on the OMR sheet. After that, the completed OMR sheet is saved as a new image and seen with matplotlib. The code can handle questions with one or more right answers. This method was not upto the mark because the method was


## Contributions

The assignment was realized on the grounds of great collaborative effort from all teammates.

Ismail:
* Worked mostly on **grade.py**; extracting answers from an exam sheet to an ouput file.

Avishmita:
* Tried some methods to do the detection.
* Able to do injection and extraction.

Onkar Saudagar(osaudaga) :
* Was responsible for trying different methods.
* Coded grid.py, img_seg.py, barcode_encode.py, barcode_decode.py, overlay.py and inject.py.
* Helped other team members to complete the code.
