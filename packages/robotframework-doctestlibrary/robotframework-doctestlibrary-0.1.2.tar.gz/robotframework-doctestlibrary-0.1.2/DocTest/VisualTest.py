from DocTest.CompareImage import CompareImage
from skimage import metrics
import imutils
import cv2
import time
import pytesseract
import shutil
import os
import uuid
import numpy as np
from pathlib import Path
from robot.libraries.BuiltIn import BuiltIn
from DocTest.PdfDoc import PdfDoc
import re
from concurrent import futures
from robot.api.deco import keyword, library

@library
class VisualTest(object):

    ROBOT_LIBRARY_VERSION = 0.1
    BORDER_FOR_MOVE_TOLERANCE_CHECK = 50
    DPI = 200
    WATERMARK_WIDTH = 25
    WATERMARK_HEIGHT = 30
    WATERMARK_CENTER_OFFSET = 3/100
    FONT = cv2.FONT_HERSHEY_SIMPLEX
    BOTTOM_LEFT_CORNER_OF_TEXT = (20,60)
    FONT_SCALE = 0.7
    FONT_COLOR = (255,0,0)
    LINE_TYPE = 2
    REFERENCE_LABEL = "Expected Result (Reference)"
    CANDIDATE_LABEL = "Actual Result (Candidate)"

    def __init__(self, **kwargs):
        self.threshold = kwargs.pop('threshold', 0.0000)
        self.SCREENSHOT_DIRECTORY = Path("screenshots/")
        self.DPI = int(kwargs.pop('DPI', 200))
        self.take_screenshots = bool(kwargs.pop('take_screenshots', False))
        self.show_diff = bool(kwargs.pop('show_diff', False))
        self.screenshot_format = kwargs.pop('screenshot_format', 'jpg')
        if not (self.screenshot_format == 'jpg' or self.screenshot_format == 'png'):
             self.screenshot_format == 'jpg'

        built_in = BuiltIn()
        try:
            self.OUTPUT_DIRECTORY = built_in.get_variable_value('${OUTPUT DIR}')
            self.reference_run = built_in.get_variable_value('${REFERENCE_RUN}', False)
            self.PABOTQUEUEINDEX = built_in.get_variable_value('${PABOTQUEUEINDEX}')
            os.makedirs(self.OUTPUT_DIRECTORY/self.SCREENSHOT_DIRECTORY, exist_ok=True)
        except:
            print("Robot Framework is not running")
            self.OUTPUT_DIRECTORY = Path.cwd()
            self.reference_run = False
            self.PABOTQUEUEINDEX = None
    
    @keyword    
    def compare_images(self, reference_image, test_image, **kwargs):
        """Compares the documents/images ``reference_image`` and ``test_image``.

        ``**kwargs`` can be used to add settings for ``placeholder_file``, ``contains_barcodes``, ``check_text_content``, ``move_tolerance``, ``get_pdf_content``
        
        Result is passed if no visual differences are detected. 
        
        ``reference_image`` and ``test_image`` may be .pdf, .ps, .pcl or image files


        Examples:
        | = Keyword =    |  = reference_image =  | = test_image =       |  = **kwargs = | = comment = |
        | Compare Images | reference.pdf | candidate.pdf |                              | #Performs a pixel comparison of both files |
        | Compare Images | reference.pdf (not existing)  | candidate.pdf |              | #Will always return passed and save the candidate.pdf as reference.pdf |
        | Compare Images | reference.pdf | candidate.pdf | placeholder_file=mask.json   | #Performs a pixel comparison of both files and excludes some areas defined in mask.json |
        | Compare Images | reference.pdf | candidate.pdf | contains_barcodes=${true}    | #Identified barcodes in documents and excludes those areas from visual comparison. The barcode data will be checked instead |
        | Compare Images | reference.pdf | candidate.pdf | check_text_content${true}    | #In case of visual differences, the text content in the affected areas will be identified using OCR. If text content it equal, the test is considered passed |
        | Compare Images | reference.pdf | candidate.pdf | move_tolerance=10            | #In case of visual differences, it is checked if difference is caused only by moved areas. If the move distance is within 10 pixels the test is considered as passed. Else it is failed |
        | Compare Images | reference.pdf | candidate.pdf | check_text_content${true} get_pdf_content=${true} | #In case of visual differences, the text content in the affected areas will be read directly from  PDF (not OCR). If text content it equal, the test is considered passed |
        | Compare Images | reference.pdf | candidate.pdf | move_tolerance=10 get_pdf_content=${true} | #In case of visual differences, it is checked if difference is caused only by moved areas. Move distance is identified directly from PDF data. If the move distance is within 10 pixels the test is considered as passed. Else it is failed |
        
        
        """
        #print("Execute comparison")
        #print('Resolution for image comparison is: {}'.format(self.DPI))

        reference_collection = []
        compare_collection = []
        detected_differences = []

        placeholder_file = kwargs.pop('placeholder_file', None)
        mask = kwargs.pop('mask', None)
        check_text_content = kwargs.pop('check_text_content', False)
        move_tolerance = kwargs.pop('move_tolerance', None)
        contains_barcodes = kwargs.pop('contains_barcodes', False)
        get_pdf_content = kwargs.pop('get_pdf_content', False)
        force_ocr = kwargs.pop('force_ocr', False)
        self.DPI = int(kwargs.pop('DPI', self.DPI))
        ignore_watermarks = kwargs.pop('ignore_watermarks', True)

        compare_options = {'get_pdf_content':get_pdf_content, 'ignore_watermarks':ignore_watermarks,'check_text_content':check_text_content,'contains_barcodes':contains_barcodes, 'force_ocr':force_ocr, 'move_tolerance':move_tolerance}

        if self.reference_run and (os.path.isfile(test_image) == True):
            shutil.copyfile(test_image, reference_image)
            print('A new reference file was saved: {}'.format(reference_image))
            return
            
        if (os.path.isfile(reference_image) is False):
            raise AssertionError('The reference file does not exist: {}'.format(reference_image))

        if (os.path.isfile(test_image) is False):
            raise AssertionError('The candidate file does not exist: {}'.format(test_image))

        with futures.ThreadPoolExecutor(max_workers=2) as parallel_executor:
            reference_future = parallel_executor.submit(CompareImage, reference_image, placeholder_file=placeholder_file, contains_barcodes=contains_barcodes, get_pdf_content=get_pdf_content, DPI=self.DPI, force_ocr=force_ocr, mask=mask)
            candidate_future = parallel_executor.submit(CompareImage, test_image, contains_barcodes=contains_barcodes, get_pdf_content=get_pdf_content, DPI=self.DPI)
            reference_compare_image = reference_future.result()
            candidate_compare_image = candidate_future.result()
        
        tic = time.perf_counter()
        if reference_compare_image.placeholders != []:
            candidate_compare_image.placeholders = reference_compare_image.placeholders
            with futures.ThreadPoolExecutor(max_workers=2) as parallel_executor:
                reference_collection_future = parallel_executor.submit(reference_compare_image.get_image_with_placeholders)
                compare_collection_future = parallel_executor.submit(candidate_compare_image.get_image_with_placeholders)
                reference_collection = reference_collection_future.result()
                compare_collection = compare_collection_future.result()
        else:
            reference_collection = reference_compare_image.opencv_images
            compare_collection = candidate_compare_image.opencv_images

        if len(reference_collection)!=len(compare_collection):
            print("Pages in reference file:{}. Pages in candidate file:{}".format(len(reference_collection), len(compare_collection)))
            for i in range(len(reference_collection)):
                cv2.putText(reference_collection[i],self.REFERENCE_LABEL, self.BOTTOM_LEFT_CORNER_OF_TEXT, self.FONT, self.FONT_SCALE, self.FONT_COLOR, self.LINE_TYPE)
                self.add_screenshot_to_log(reference_collection[i], "_reference_page_" + str(i+1))
            for i in range(len(compare_collection)):
                cv2.putText(compare_collection[i],self.CANDIDATE_LABEL, self.BOTTOM_LEFT_CORNER_OF_TEXT, self.FONT, self.FONT_SCALE, self.FONT_COLOR, self.LINE_TYPE)
                self.add_screenshot_to_log(compare_collection[i], "_candidate_page_" + str(i+1))
            raise AssertionError('Reference File and Candidate File have different number of pages')
        
        with futures.ThreadPoolExecutor(max_workers=8) as parallel_executor:
            for i, (reference, candidate) in enumerate(zip(reference_collection, compare_collection)):
                if get_pdf_content:
                    reference_pdf_content = reference_compare_image.pdf_content[i]
                    candidate_pdf_content = candidate_compare_image.pdf_content[i]
                else:
                    reference_pdf_content = None
                    candidate_pdf_content = None
                parallel_executor.submit(self.check_for_differences, reference, candidate, i, detected_differences, compare_options, reference_pdf_content, candidate_pdf_content)
                #self.check_for_differences(reference, candidate, i, detected_differences, compare_options, reference_pdf_content, candidate_pdf_content)

        if reference_compare_image.barcodes!=[]:
            if reference_compare_image.barcodes!=candidate_compare_image.barcodes:
                detected_differences.append(True)
                print("The barcode content in images is different")
                print("Reference image:\n", reference_compare_image.barcodes)
                print("Candidate image:\n", candidate_compare_image.barcodes)

        for difference in detected_differences:

            if (difference):
                print("The compared images are different")
                raise AssertionError('The compared images are different.')

        print("The compared images are equal")

        toc = time.perf_counter()
        print(f"Visual Image comparison performed in {toc - tic:0.4f} seconds")

    def get_images_with_highlighted_differences(self, thresh, reference, candidate, extension=10):
        
        #thresh = cv2.dilate(thresh, None, iterations=extension)
        thresh = cv2.dilate(thresh, None, iterations=10)
        thresh = cv2.erode(thresh, None, iterations=10)
        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)

        # loop over the contours
        for c in cnts:
            # compute the bounding box of the contour and then draw the
            # bounding box on both input images to represent where the two
            # images differ
            (x, y, w, h) = cv2.boundingRect(c)
            cv2.rectangle(reference, (x, y), (x + w, y + h), (0, 0, 255), 4)
            cv2.rectangle(candidate, (x, y), (x + w, y + h), (0, 0, 255), 4)
        return reference, candidate, cnts

    def get_diff_rectangle(self, thresh):
        points = cv2.findNonZero(thresh)
        (x, y, w, h) = cv2.boundingRect(points)
        return x, y, w, h

    def add_screenshot_to_log(self, image, suffix):
        screenshot_name = str(str(uuid.uuid1()) + suffix + '.{}'.format(self.screenshot_format))
        
        if self.PABOTQUEUEINDEX is not None:
            rel_screenshot_path = str(self.SCREENSHOT_DIRECTORY / '{}-{}'.format(self.PABOTQUEUEINDEX, screenshot_name))
        else:
            rel_screenshot_path = str(self.SCREENSHOT_DIRECTORY / screenshot_name)
            
        abs_screenshot_path = str(self.OUTPUT_DIRECTORY/self.SCREENSHOT_DIRECTORY/screenshot_name)
        
        if self.screenshot_format == 'jpg':
            cv2.imwrite(abs_screenshot_path, image, [int(cv2.IMWRITE_JPEG_QUALITY), 70])
        else:
            cv2.imwrite(abs_screenshot_path, image)

        print("*HTML* "+ "<a href='" + rel_screenshot_path + "' target='_blank'><img src='" + rel_screenshot_path + "' style='width:50%; height: auto;'/></a>")

    def find_partial_image_position(self, img, template, threshold = 0.1):
        print("Find partial image position")
        rectangles = []
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        template_gray = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
        h, w = template.shape[0:2]

        res = cv2.matchTemplate(img_gray,template_gray,cv2.TM_SQDIFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    
        loc = (np.array([min_loc[1],]), np.array([min_loc[0],]))


        # threshold = 0.9
        # loc = np.where( res >= threshold)
        for pt in zip(*loc[::-1]):
            rectangles.append({"pt1":pt,"pt2":(pt[0] + w, pt[1] + h) })
            #cv2.rectangle(img, pt, (pt[0] + w, pt[1] + h), (0,0,255), 2)

        #Determine whether this sub image has been found
        if (min_val < threshold):
            return rectangles
        return

    def overlay_two_images(self, image, overlay, ignore_color=[255,255,255]):
        ignore_color = np.asarray(ignore_color)
        mask = ~(overlay==ignore_color).all(-1)
        # Or mask = (overlay!=ignore_color).any(-1)
        out = image.copy()
        out[mask] = image[mask] * 0.5 + overlay[mask] * 0.5
        return out

    def check_for_differences(self, reference, candidate, i, detected_differences, compare_options, reference_pdf_content=None, candidate_pdf_content=None ):
        pass
        images_are_equal = True
        with futures.ThreadPoolExecutor(max_workers=2) as parallel_executor:
            grayA_future = parallel_executor.submit(cv2.cvtColor, reference, cv2.COLOR_BGR2GRAY)
            grayB_future = parallel_executor.submit(cv2.cvtColor, candidate, cv2.COLOR_BGR2GRAY)
            grayA = grayA_future.result()
            grayB = grayB_future.result()

        # compute the Structural Similarity Index (SSIM) between the two
        # images, ensuring that the difference image is returned
        (score, diff) = metrics.structural_similarity(grayA, grayB, gaussian_weights=True, full=True)
        score = abs(1-score)
        
        if self.take_screenshots:
            # Not necessary to take screenshots for every successful comparison
            self.add_screenshot_to_log(np.concatenate((reference, candidate), axis=1), "_page_" + str(i+1) + "_compare_concat")
            
        if (score > self.threshold):
        
            diff = (diff * 255).astype("uint8")

            thresh = cv2.threshold(diff, 0, 255,
                cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
            
            reference_with_rect, candidate_with_rect , cnts= self.get_images_with_highlighted_differences(thresh, reference.copy(), candidate.copy(), extension=5)
            blended_images = self.overlay_two_images(reference_with_rect, candidate_with_rect)
            
            cv2.putText(reference_with_rect,self.REFERENCE_LABEL, self.BOTTOM_LEFT_CORNER_OF_TEXT, self.FONT, self.FONT_SCALE, self.FONT_COLOR, self.LINE_TYPE)
            cv2.putText(candidate_with_rect,self.CANDIDATE_LABEL, self.BOTTOM_LEFT_CORNER_OF_TEXT, self.FONT, self.FONT_SCALE, self.FONT_COLOR, self.LINE_TYPE)
            
            self.add_screenshot_to_log(np.concatenate((reference_with_rect, candidate_with_rect), axis=1), "_page_" + str(i+1) + "_rectangles_concat")
            self.add_screenshot_to_log(blended_images, "_page_" + str(i+1) + "_blended")

            if self.show_diff:
                self.add_screenshot_to_log(np.concatenate((diff, thresh), axis=1), "_page_" + str(i+1) + "_diff")

            images_are_equal=False

            if compare_options["ignore_watermarks"] == True and len(cnts)==1:
                (x, y, w, h) = cv2.boundingRect(cnts[0])
                diff_center_x = abs((x+w/2)-(reference.shape[1]/2))
                diff_center_y = abs((y+h/2)-(reference.shape[0]/2))
                if (diff_center_x < reference.shape[1] * self.WATERMARK_CENTER_OFFSET) and (w * 25.4 / self.DPI < self.WATERMARK_WIDTH) and (h * 25.4 / self.DPI < self.WATERMARK_HEIGHT):
                    images_are_equal=True
                    return

            if(compare_options["check_text_content"]==True) and images_are_equal is not True:
                if compare_options["get_pdf_content"] is not True:
                    #x, y, w, h = self.get_diff_rectangle(thresh)
                    images_are_equal=True
                    for c in range(len(cnts)):
                        (x, y, w, h) = cv2.boundingRect(cnts[c])
                        diff_area_reference = reference[y:y+h, x:x+w]
                        diff_area_candidate = candidate[y:y+h, x:x+w]

                        self.add_screenshot_to_log(diff_area_reference, "_page_" + str(i+1) + "_diff_area_reference_"+str(c))
                        self.add_screenshot_to_log(diff_area_candidate, "_page_" + str(i+1) + "_diff_area_test_"+str(c))

                        text_reference = pytesseract.image_to_string(diff_area_reference)
                        text_test = pytesseract.image_to_string(diff_area_candidate)
                        if(text_reference==text_test):                           
                            print("Partial text content is the same")
                            print(text_reference)
                        else:
                            images_are_equal=False
                            detected_differences.append(True)
                            print("Partial text content is different")
                            print(text_reference + " is not equal to " + text_test)
                elif compare_options["get_pdf_content"] is True:
                    images_are_equal=True
                    for c in range(len(cnts)):
                        (x, y, w, h) = cv2.boundingRect(cnts[c])
                        diff_area_reference = reference[y:y+h, x:x+w]
                        diff_area_candidate = candidate[y:y+h, x:x+w]

                        self.add_screenshot_to_log(diff_area_reference, "_page_" + str(i+1) + "_diff_area_reference_"+str(c))
                        self.add_screenshot_to_log(diff_area_candidate, "_page_" + str(i+1) + "_diff_area_test_"+str(c))

                        referenceItems = PdfDoc.get_items_in_area(reference_pdf_content, x, y, w, h, self.DPI/72)
                        candidateItems = PdfDoc.get_items_in_area(candidate_pdf_content, x, y, w, h, self.DPI/72)
                        
                        referenceItems = remove_empty_textelements(referenceItems)
                        candidateItems = remove_empty_textelements(candidateItems)

                        if len(referenceItems)!=len(candidateItems):
                            images_are_equal=False
                            detected_differences.append(True)
                            print("The identified pdf layout elements are different", referenceItems, candidateItems)
                        else:

                            for ref_Item, cand_Item in zip(referenceItems, candidateItems):
                                if ref_Item == cand_Item:
                                    pass
                                elif str(ref_Item['text']).strip() != str(cand_Item['text']).strip():
                                    images_are_equal=False
                                    detected_differences.append(True)
                                    print("Partial text content is different")
                                    print(ref_Item['text'], " is not equal to " ,cand_Item['text'])
                            if images_are_equal:
                                print("Partial text content of area is the same")
                                print(referenceItems)


            
            if(compare_options["move_tolerance"]!=None) and images_are_equal is not True:
                move_tolerance=int(compare_options["move_tolerance"])
                images_are_equal=True
                
                if compare_options["get_pdf_content"] is not True:

                
                    for c in range(len(cnts)):
                    
                        (x, y, w, h) = cv2.boundingRect(cnts[c])
                        diff_area_reference = reference[y:y+h, x:x+w]
                        diff_area_candidate = candidate[y:y+h, x:x+w]
                        search_area_candidate = candidate[y - self.BORDER_FOR_MOVE_TOLERANCE_CHECK:y + h + self.BORDER_FOR_MOVE_TOLERANCE_CHECK, x - self.BORDER_FOR_MOVE_TOLERANCE_CHECK:x + w + self.BORDER_FOR_MOVE_TOLERANCE_CHECK]
                        search_area_reference = reference[y - self.BORDER_FOR_MOVE_TOLERANCE_CHECK:y + h + self.BORDER_FOR_MOVE_TOLERANCE_CHECK, x - self.BORDER_FOR_MOVE_TOLERANCE_CHECK:x + w + self.BORDER_FOR_MOVE_TOLERANCE_CHECK]                      

                        positions_in_compare_image = self.find_partial_image_position(search_area_candidate, diff_area_reference)
                        #positions_in_compare_image = self.find_partial_image_position(candidate, diff_area_reference)
                        if (np.mean(diff_area_reference) == 255) or (np.mean(diff_area_candidate) == 255):
                            images_are_equal=False
                            detected_differences.append(True)
                            print("Image section contains only white background")

                            self.add_screenshot_to_log(np.concatenate((cv2.copyMakeBorder(diff_area_reference, top=2, bottom=2, left=2, right=2, borderType=cv2.BORDER_CONSTANT, value=[0,0,0]), cv2.copyMakeBorder(diff_area_candidate, top=2, bottom=2, left=2, right=2, borderType=cv2.BORDER_CONSTANT, value=[0,0,0])), axis=1), "_diff_area_concat")



                            #self.add_screenshot_to_log(np.concatenate((diff_area_reference, diff_area_candidate), axis=1), "_diff_area_concat")

                        else:
                            if positions_in_compare_image:
                                
                                #pt_original = (x, y)
                                pt_original = (self.BORDER_FOR_MOVE_TOLERANCE_CHECK, self.BORDER_FOR_MOVE_TOLERANCE_CHECK)
                                pt_compare = positions_in_compare_image[0]['pt1']                                
                                x_moved = abs(pt_original[0]-pt_compare[0])
                                y_moved = abs(pt_original[1]-pt_compare[1])

                                cv2.arrowedLine(candidate_with_rect, pt_original, pt_compare, (255, 0, 0), 4)
                                if int(x_moved+y_moved)>int(move_tolerance):
                                    print("Image section moved ",x_moved+y_moved, " pixels")
                                    print("This is outside of the allowed range of ",move_tolerance, " pixels")
                                    images_are_equal=False
                                    detected_differences.append(True)
                                    self.add_screenshot_to_log(self.overlay_two_images(search_area_reference, search_area_candidate), "_diff_area_blended")
                                    
                                else:
                                    print("Image section moved ",x_moved+y_moved, " pixels")
                                    print("This is within the allowed range of ",move_tolerance, " pixels")
                                    self.add_screenshot_to_log(self.overlay_two_images(search_area_reference, search_area_candidate), "_diff_area_blended")

                            else:
                                images_are_equal=False
                                detected_differences.append(True)
                                print("The reference image section was not found in test image (or vice versa)")
                                self.add_screenshot_to_log(np.concatenate((cv2.copyMakeBorder(diff_area_reference, top=2, bottom=2, left=2, right=2, borderType=cv2.BORDER_CONSTANT, value=[0,0,0]), cv2.copyMakeBorder(diff_area_candidate, top=2, bottom=2, left=2, right=2, borderType=cv2.BORDER_CONSTANT, value=[0,0,0])), axis=1), "_diff_area_concat")

                elif compare_options["get_pdf_content"] is True:
                    for c in range(len(cnts)):
                        (x, y, w, h) = cv2.boundingRect(cnts[c])
                        diff_area_reference = reference[y:y+h, x:x+w]
                        diff_area_candidate = candidate[y:y+h, x:x+w]
                        search_area_candidate = candidate[y - self.BORDER_FOR_MOVE_TOLERANCE_CHECK:y + h + self.BORDER_FOR_MOVE_TOLERANCE_CHECK, x - self.BORDER_FOR_MOVE_TOLERANCE_CHECK:x + w + self.BORDER_FOR_MOVE_TOLERANCE_CHECK]
                        search_area_reference = reference[y - self.BORDER_FOR_MOVE_TOLERANCE_CHECK:y + h + self.BORDER_FOR_MOVE_TOLERANCE_CHECK, x - self.BORDER_FOR_MOVE_TOLERANCE_CHECK:x + w + self.BORDER_FOR_MOVE_TOLERANCE_CHECK]                      


                        self.add_screenshot_to_log(diff_area_reference, "_page_" + str(i+1) + "_diff_area_reference_"+str(c))
                        self.add_screenshot_to_log(diff_area_candidate, "_page_" + str(i+1) + "_diff_area_test_"+str(c))
                        with futures.ThreadPoolExecutor(max_workers=2) as parallel_executor:
                            referenceItems_future = parallel_executor.submit(PdfDoc.get_items_in_area, reference_pdf_content, x, y, w, h, self.DPI/72)
                            candidateItems_future = parallel_executor.submit(PdfDoc.get_items_in_area, candidate_pdf_content, x, y, w, h, self.DPI/72)
                            referenceItems = referenceItems_future.result()
                            candidateItems = candidateItems_future.result()
                        
                        if len(referenceItems)!=len(candidateItems):
                            images_are_equal=False
                            detected_differences.append(True)
                            print("The identified pdf layout elements are different", referenceItems, candidateItems)
                        else:

                            for ref_Item, cand_Item in zip(referenceItems, candidateItems):
                                if ref_Item == cand_Item:
                                    pass


                                elif str(ref_Item['text']).strip() == str(cand_Item['text']).strip():
                                    left_moved = abs(ref_Item['x']-cand_Item['x'])
                                    top_moved = abs(ref_Item['y']-cand_Item['y'])
                                    right_moved = abs((ref_Item['x']+ref_Item['width'])-(cand_Item['x']+cand_Item['width']))
                                    bottom_moved = abs((ref_Item['y']+ref_Item['height'])-(cand_Item['y']+cand_Item['height']))
                                    print("Checking pdf elements", ref_Item, cand_Item)


                                    if int(left_moved)>int(move_tolerance) or int(top_moved)>int(move_tolerance) or int(right_moved)>int(move_tolerance) or int(bottom_moved)>int(move_tolerance):
                                        print("Image section moved ",left_moved, top_moved, right_moved, bottom_moved, " pixels")
                                        print("This is outside of the allowed range of ",move_tolerance, " pixels")
                                        images_are_equal=False
                                        detected_differences.append(True)
                                        self.add_screenshot_to_log(self.overlay_two_images(search_area_reference, search_area_candidate), "_diff_area_blended")
                                    

                                    else:
                                        print("Image section moved ",left_moved, top_moved, right_moved, bottom_moved, " pixels")
                                        print("This is within the allowed range of ",move_tolerance, " pixels")
                                        self.add_screenshot_to_log(self.overlay_two_images(search_area_reference, search_area_candidate), "_diff_area_blended")

                                else:
                                    images_are_equal=False
                                    detected_differences.append(True)
                                    print("Partial text content is different")
                                    print(ref_Item['text'], " is not equal to " ,cand_Item['text'])
                                

                            if images_are_equal:
                                print("Partial text content of area is the same")
                                print(referenceItems)
            if images_are_equal is not True:
                detected_differences.append(True)



def remove_empty_textelements(lst):
    new_list = []
    for i, dic in enumerate(lst):
        if str(dic['text']).isspace() is not True:
            new_list.append(dic)
    return new_list