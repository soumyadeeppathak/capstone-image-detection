import cv2
import pytesseract
import glob
import os
pytesseract.pytesseract.tesseract_cmd = 'c:\\Users\\soumy\\AppData\\Local\\Tesseract-OCR\\tesseract'

#Quick sort
def partition(arr,low,high): 
    i = ( low-1 )         
    pivot = arr[high]    
  
    for j in range(low , high): 
        if   arr[j] < pivot: 
            i = i+1 
            arr[i],arr[j] = arr[j],arr[i] 
  
    arr[i+1],arr[high] = arr[high],arr[i+1] 
    return ( i+1 ) 

def quickSort(arr,low,high): 
    if low < high: 
        pi = partition(arr,low,high) 
  
        quickSort(arr, low, pi-1) 
        quickSort(arr, pi+1, high)
        
    return arr
 
#Binary search   
def binarySearch (arr, l, r, x): 
  
    if r >= l: 
        mid = l + (r - l) // 2
        if arr[mid] == x: 
            return mid 
        elif arr[mid] > x: 
            return binarySearch(arr, l, mid-1, x) 
        else: 
            return binarySearch(arr, mid + 1, r, x) 
    else: 
        return -1
    

print("HELLO!!")
print("Welcome to the Number Plate Detection System.\n")

array=[]

dir = os.path.dirname(__file__)

for img in glob.glob(dir+"/Images/*.jpeg") :
    # Read the image file
    image = cv2.imread(img)
    cv2.imshow("Original",image)
    # Convert to Grayscale Image
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    #Canny Edge Detection
    canny_edge = cv2.Canny(gray_image, 170, 200)

    # Find contours based on Edges
    contours, new  = cv2.findContours(canny_edge.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours=sorted(contours, key = cv2.contourArea, reverse = True)[:30]

    # Initialize license Plate contour and x,y,w,h coordinates
    contour_with_license_plate = None
    license_plate = None
    x = None
    y = None
    w = None
    h = None

    # Find the contour with 4 potential corners and create ROI around it
    for contour in contours:
            # Find Perimeter of contour and it should be a closed contour
            perimeter = cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, 0.01 * perimeter, True)
            if len(approx) == 4:                                            #see whether it is a Rect
                contour_with_license_plate = approx
                x, y, w, h = cv2.boundingRect(contour)
                license_plate = gray_image[y:y + h, x:x + w]
                break
    (thresh, license_plate) = cv2.threshold(license_plate, 127, 255, cv2.THRESH_BINARY)
    cv2.imshow("plate",license_plate)
    # Removing Noise from the detected image, before sending to Tesseract
    license_plate = cv2.bilateralFilter(license_plate, 11, 17, 17)
    (thresh, license_plate) = cv2.threshold(license_plate, 150, 180, cv2.THRESH_BINARY)

    #Text Recognition
    text = pytesseract.image_to_string(license_plate)