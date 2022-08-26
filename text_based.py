from PIL import Image
import pytesseract
import os
import image_preprocessor

class TextBasedRec:
    def __init__(self, path_to_tesseract="tesseract"):
        self.CLASSES_TEXT = {
            0: ["счет-фактура", "исправление №", 'счет_фак"ура', "счет-фактура №", "счет_фактура", "счет - фактура", "счет_фа'п‚ура"], # Class 0 - Factura
            1: ["счет на оплату", "счёт на оплату", "счет действителен в течении", "счет №", "всего наименований", "срок оплаты", "в т.ч. ндс", "оплата по договору", "вт.ч. ндс", "без налога", "в том числе ндс", "итого к оплате", "на оплату №"] # Class 1 - Oplata
            #"в том числе ндс", "итого позиций", "счет №", 
        }
        pytesseract.pytesseract.tesseract_cmd = r'tesseract'

    def recognzie(self, image):
        text_on_image = pytesseract.image_to_string(image, lang="rus", config="").lower()
        uniq_matches = {0: [], 1: []}
        if not "акт об оказании услуг" in text_on_image and not "акт сдачи-приемки предоставленных услуг" in text_on_image and not "сдачи-приемки выполненных работ" in text_on_image and not "акт приемки-передачи товара" in text_on_image and not "акт сдачи" in text_on_image and not "приемки-передачи товара" in text_on_image and not "форму акта" in text_on_image:
            for keyphrase in self.CLASSES_TEXT[0]:
                if keyphrase in text_on_image:
                    if keyphrase not in uniq_matches[0]:
                        uniq_matches[0].append(keyphrase)
            for keyphrase in self.CLASSES_TEXT[1]:
                if keyphrase in text_on_image:
                    if keyphrase not in uniq_matches[1]:
                        uniq_matches[1].append(keyphrase)
        
        
            #print(uniq_matches)
            #print(text_on_image)
            matches_class_0 = len(uniq_matches[0])
            matches_class_1 = len(uniq_matches[1])
            if matches_class_0 > matches_class_1:
                return 0
            elif matches_class_0 < matches_class_1:
                return 1
            return -1
        else:
            return -1
        
if __name__ == "__main__":
    # Strange: inv-0018.jpg
    print("Tetsing library...")
    recognizer = TextBasedRec()
    #image = Image.open("./Oplata/inv-0018.jpg")
    #img_class = recognizer.recognzie(image)
    #print(img_class)
    
    #PATH = "../"
    #files = os.listdir(PATH)
    #print(files)
    #files = ['scan_18.jpg']
    #files = ["scan_36.jpg"]
    img = Image.open(f"scan_18.jpg")
    img = image_preprocessor.process(img)
    img_class = recognizer.recognzie(img)
    print(img_class)
    '''tests_success = 0
    expected_class = 1
    test_failed = []
    for img_path in files:
        img = Image.open(f"{PATH}/{img_path}")
        img = image_preprocessor.process(img)
        img_class = recognizer.recognzie(img)
        if img_class != expected_class:
            print("Error, output:", img_class)
            print(img_path)
            test_failed.append(img_path)
        else:
            tests_success += 1
            print("Success", tests_success)
    
    print("Failed:", test_failed)
    print("Success cnt:", tests_success)'''
    
