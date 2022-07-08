# Children Literacy Software

### OCR recognition app for Children (Backend)

Softwares: Django, MySQL, Elastic Compute Service(Ali Cloud), Pycharm

Tools and Techniques: TensorFlow (tesseract), OpenCV, Web Crawler, Optical Character Recognition(OCR), Apache + mod_wsgi. 

### product orientation

It is evident that Chinese is hard to learn. Not only for people from other countries but also for Chinese children. This product is based on OCR to help Children to learn Chinese characters. 



# Back-End Main Work

### Back-End WorkFlow

*  The whole project is deployed on ECS through Apache and Mod_wsgi.
* Django is the main framework for the whole project. All back-end algorithms are designed on Django.
* MySQL is used to store all data.
* The interfaces are designed in RESTful style.
<img width="937" alt="image-20220708035321519" src="https://user-images.githubusercontent.com/32299390/177946251-5e0dc01c-9f5c-47a2-ad73-1773b80415bc.png">

### OCR WorkFlow:

1. Front-End sends the whole picture and specific location to the Back-End.

2. The server uses OpenCV to preprocess the pictures containing the target Chinese characters.
3. Then the server sends the processed pictures to the tesseract library for Chinese character recognition.
4. Finally, the identified Chinese characters are retrieved from the local database, and the details of the target Chinese characters are sent to the Front-End in JSON form in response to the request of the front end. 
<img width="756" alt="image-20220707220758954" src="https://user-images.githubusercontent.com/32299390/177946324-eebfc50e-ccce-48a7-af07-1a4eeaeef9d0.png">

## Image Preprocessing

The following is the workflow of image preprocessing. 
<img width="881" alt="image-20220707222241673" src="https://user-images.githubusercontent.com/32299390/177946441-8748f62b-7c29-4ad6-9c58-1af0512e8e8e.png">

#### Image Slicer

The picture received from the Front-End is usually large and contains all kinds of information. For us, character recognition in the server image process only needs a small piece of the image which includes the identified target characters. So as to improve the efficiency of processing pictures and recognizing Chinese characters, we need to cut the image.

In image cutting, the coordinates of the red point are first obtained, and then a picture of 200*200 pixels is taken with the coordinates of the red point as the center point. 

<img width="532" alt="image-20220707222502845" src="https://user-images.githubusercontent.com/32299390/177946490-2ca05f51-bcf6-4f44-9d1b-d0b7d7ae089d.png">

#### Expansion

- To determine whether the red dot clicks the character.
- Chinese characters are thin, we need to expand the character.
<img width="697" alt="image-20220707223530588" src="https://user-images.githubusercontent.com/32299390/177946579-7a9662bc-2e13-4cf4-bda6-b8d8923f0614.png">

#### Anti-interference

* Grey Processing

  - The original cut image may contain rich colors.
  - Remove the color from the image, leaving only black and white.

* noise reduction

  * Image noise will make some random, discrete, and isolated pixels appear on the image. 
  * One is produced during filming, and the other is produced during transmission.

* binarization

  * The multi-value digital image is extracted from the target object to form binarization. 
  * The useless object will be set as 0 and the target object as 1.

  

#### Distance Filed

In the Image Slicer, we get the image by setting the red point as the center and cutting the image through 200*200 pixels.

So sometimes we may get two Characters in one picture.

1. **Boundary:** the original image is expanded, and then the boundary map of the expanded image is drawn.
2. **Distance field:** Then, we do distance field processing for the pictures containing Chinese character boundaries after boundary processing. （The two brightest points of light represent two characters）

<img width="889" alt="image-20220707225224387" src="https://user-images.githubusercontent.com/32299390/177946630-3e3a5da9-a56f-444e-b511-e29d93c74e9f.png">

#### WaterShed

* Points of light in different distance fields are defined as different pixel values

* Different Chinese characters have different pixel values in the region.

<img width="846" alt="image-20220707225747688" src="https://user-images.githubusercontent.com/32299390/177946692-023dc565-2620-4d59-bb14-c4bba47755d9.png">

#### Pixel Filling

* The coordinates of the red dots were compared with the images after the watershed.
* Assuming that the red dot is in the right area, fill all the other areas with white pixels.

<img width="673" alt="image-20220707225951073" src="https://user-images.githubusercontent.com/32299390/177946735-bc61804e-44f6-4736-aa81-69625e972a27.png">



## Database System Design

The following is the E-R graph of the database.

* The web crawler collects the information for the Word and the Books Table. 

<img width="787" alt="image-20220708032605762" src="https://user-images.githubusercontent.com/32299390/177946774-b4745897-026f-45b3-8dc1-bd1efe0f7d29.png">




