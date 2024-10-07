import os



# แคลที่ต้องใช้
def calculatecaloriesforday(weight,tall,age,sex,activity):
    if sex == "man":
        BMR = 66 + (13.7*weight) + (5*tall)-(6.8*age)
    elif sex == "woman":
        BMR = 665+(9.6*weight) + (1.8*tall)-(4.7*age)
    if activity == "นั่งทำงานอยู่กับที่ และไม่ได้ออกกำลังกายเลย" :
        TDFF = BMR*1.2
    elif activity == "ออกกำลังกายหรือเล่นกีฬาเล็กน้อย ประมาณอาทิตย์ละ 1-3 วัน" :
        TDFF = BMR*1.375
    elif activity == "ออกกำลังกายหรือเล่นกีฬาปานกลาง ประมาณอาทิตย์ละ 3-5 วัน" :
        TDFF = BMR*1.55
    elif activity == "ออกกำลังกายหรือเล่นกีฬาอย่างหนัก ประมาณอาทิตย์ละ 6-7 วัน" :
        TDFF = BMR*1.725
    elif activity == "ออกกำลังกายหรือเล่นกีฬาอย่างหนักทุกวันเช้าเย็น" :
        TDFF = BMR*1.9
    return TDFF

# แคลอรี่ของอาหารแต่ละชนิดต่อจาน
def calculatetotalcalories(listfood): #[9,9,9,8]
    print(listfood)
    number_of_food = {
        '0' : 'French-fries',
        '1' : 'KFC',
        '2' : 'burger', 
        '3' : 'cake' ,
        '4' : 'hot-dog' ,
        '5' : 'pizza' ,
        '6' : 'salad' ,
        '7' : 'spaghetti',
        '8': 'steak',
        '9':'sushi',
    }
    calorie_info = {
        'French-fries': 200,
        'KFC': 250, 
        'burger': 150, 
        'cake'  : 100,
        'hot-dog' : 100,
        'pizza' : 100,
        'salad' : 100,
        'spaghetti' : 150,
        'steak' : 100,
        'sushi' : 100,
    }
    listcal=[]
    for i in listfood:
        i=str(i)
        foodtype = number_of_food[i]
        calorieforone = calorie_info[foodtype]
        listcal.append(calorieforone)
    totalcal=sum(listcal)
    return totalcal



def get_latest_exp_folder():
    runs_dir = 'runs/detect/'
    subdirs = [d for d in os.listdir(runs_dir) if os.path.isdir(os.path.join(runs_dir, d))]
    # ค้นหาโฟลเดอร์ล่าสุดที่เริ่มต้นด้วย 'exp'
    exp_dirs = sorted([d for d in subdirs if d.startswith('exp')], key=lambda x: os.path.getmtime(os.path.join(runs_dir, x)), reverse=True)
    
    if exp_dirs:
        return os.path.join(runs_dir, exp_dirs[0])  # คืนค่าโฟลเดอร์ 'exp' ล่าสุด
    return None
def read_latest_class_indices(image_name):
    latest_exp_folder = get_latest_exp_folder()  # ค้นหาโฟลเดอร์ 'exp' ล่าสุด
    
    if latest_exp_folder:
        # ค้นหาไฟล์ .txt ที่ตรงกับชื่อภาพในโฟลเดอร์ labels
        results_file = os.path.join(latest_exp_folder, 'labels', image_name.replace('.jpg', '.txt'))
        
        class_indices = []
        if os.path.exists(results_file):
            with open(results_file, 'r') as f:
                lines = f.readlines()
                for line in lines:
                    class_index = int(line.split()[0])  # ดึงค่า class_index จากแต่ละบรรทัด
                    class_indices.append(class_index)  # เก็บค่า class_index ใน list
    return class_indices

# print(calculatetotalcalories(read_latest_class_indices('IMG_20241004_200105.jpg')))
def predict_image(image_path):
    weights = 'runs/train/exp36/weights/best.pt'
    img_size = 224
    conf_thresh = 0.25
    data_yaml = 'data.yaml'
    yolov5_path = 'detect.py'

    command = (f"python3 {yolov5_path} --weights {weights} --img {img_size} --conf {conf_thresh}" 
    + f" --source {image_path} --data {data_yaml} --save-txt")
    
    os.system(command) 
        
image_path = "/home/beer/images/pizzaforai.jpg"
weight=int(input("weight :"))
tall=int(input("tall :"))
age=int(input("age :"))
sex=str(input("sex :"))
activity="ออกกำลังกายหรือเล่นกีฬาอย่างหนักทุกวันเช้าเย็น"
image_name='pizzaforai.jpg'

def main(weight,tall,age,sex,activity,image_path,image_name):
    predict_image(image_path)
    totalcal=(calculatetotalcalories(read_latest_class_indices(image_name)))
    needscal=calculatecaloriesforday(weight,tall,age,sex,activity)
    # print(F'Foods_with {totalcal} calories.')
    # print(F'Total Daily Energy Expenditure is {needscal:.2f} calories.')
    return F'Foods_with {totalcal} calories.\nTotal Daily Energy Expenditure is {needscal:.2f} calories.'

print(main(weight,tall,age,sex,activity,image_path,image_name))


    
#"C:\Users\teera\Downloads\kfc.jpg"
#"C:\Users\teera\Downloads\archive\images\hamburger\1567823.jpg"

# import tkinter as tk
# from tkinter import filedialog
    #    # สร้างหน้าต่างเลือกไฟล์
    # root = tk.Tk()
    # root.withdraw()  # ซ่อนหน้าต่างหลักของ tkinter

    # # เปิดหน้าต่างให้ผู้ใช้เลือกไฟล์ .jpg
    # file_path = filedialog.askopenfilename(filetypes=[("JPG files", "*.jpg")])
    
     # แยกชื่อไฟล์จาก path
    # file_name = os.path.basename(file_path)  # วิธีที่ 1: ใช้ os.path

    # predict_image("C:/Users/teera/Downloads/kfc.jpg")

