import numpy as np
import pandas as pd
import json
from unidecode import unidecode

class AddressExtractor():
    def __init__(self):
        self.quan_list = ['ba dinh', 'hoan kiem', 'tay ho', 'long bien', 'cau giay', 'dong da', 'hai ba trung', 'hoang mai', 'thanh xuan', 'ha dong', 'bac tu liem', 'nam tu liem', 'son tay', 'ba vi', 'chuong my', 'chuong mi', 'dan phuong', 'dong anh', 'gia lam', 'hoai duc', 'me linh', 'my duc', 'mi duc', 'phu xuyen', 'phu tho', 'quoc oai', 'soc son', 'thach that', 'thanh oai', 'thanh tri', 'thuong tin', 'ung hoa']
        self.phuong_list = {
                'ba dinh': ['cong vi', 'dien bien', 'doi can', 'giang vo', 'kim ma', 'lieu giai', 'ngoc ha', 'ngoc khanh', 'nguyen trung truc', 'phuc xa', 'quan thanh', 'thanh cong', 'truc bach', 'vinh phuc'],
                'hoan kiem': ['chuong duong', 'cua dong', 'cua nam', 'dong xuan', 'hang bac', 'hang bai', 'hang bo', 'hang bong', 'hang buom', 'hang dao', 'hang gai', 'hang ma', 'hang trong', 'ly thai to', 'phan chu trinh', 'phuc tan', 'tran hung dao', 'trang tien'],
                'tay ho': ['buoi', 'nhat tan', 'phu thuong', 'quang an', 'thuy khue', 'tu lien', 'xuan la', 'yen phu'],
                'long bien': ['bo de', 'cu khoi', 'duc giang', 'gia thuy', 'giang bien', 'ngoc lam', 'ngoc thuy', 'phuc dong', 'phuc loi', 'sai dong', 'thach ban', 'thuong thanh', 'viet hung', 'long bien'],
                'cau giay': ['dich vong', 'dich vong hau', 'mai dich', 'nghia do', 'nghia tan', 'quan hoa', 'trung hoa', 'yen hoa'],
                'dong da': ['cat linh', 'hang bot', 'kham thien', 'khuong thuong', 'kim lien', 'lang ha', 'lang thuong', 'nam dong', 'nga tu so', 'o cho dua', 'phuong lien', 'phuong mai', 'quang trung', 'quoc tu giam', 'thinh quang', 'tho quan', 'trung liet', 'trung phung', 'trung tu', 'van chuong', 'van mieu'],
                'hai ba trung': ['bach khoa', 'bach dang', 'bach mai', 'cau den', 'dong mac', 'dong nhan', 'dong tam', 'le dai hanh', 'minh khai', 'nguyen du', 'pham dinh ho', 'pho hue', 'quynh loi', 'quynh mai', 'thanh luong', 'thanh nhan', 'truong dinh', 'vinh tuy'],
                'hoang mai': ['dai kim', 'dinh cong', 'giap bat', 'hoang liet', 'hoang van thu', 'linh nam', 'mai dong', 'tan mai', 'thanh tri', 'thinh liet', 'tran phu', 'tuong mai', 'vinh hung', 'yen so'],
                'thanh xuan': ['ha dinh', 'khuong dinh', 'khuong mai', 'khuong trung', 'kim giang', 'nhan chinh', 'phuong liet', 'thanh xuan bac', 'thanh xuan nam', 'thanh xuan trung', 'thuong dinh'],
                'ha dong': ['bien giang', 'dong mai', 'yen nghia', 'duong noi', 'ha cau', 'la khe', 'mo lao', 'nguyen trai', 'phu la', 'phu lam', 'phu luong', 'kien hung', 'phuc la', 'quang trung', 'van phuc', 'van quan', 'yet kieu'],
                'bac tu liem': ['co nhue 1', 'co nhue 2', 'co nhue', 'duc thang', 'dong ngac', 'thuy phuong', 'lien mac', 'thuong cat', 'tay tuu', 'minh khai', 'phu dien', 'phuc dien', 'xuan dinh', 'xuan tao'],
                'nam tu liem': ['cau dien', 'my dinh 1', 'my dinh 2', 'my dinh', 'mi dinh', 'phu do', 'me tri', 'trung van', 'dai mo', 'tay mo', 'phuong canh', 'xuan phuong'],
                'son tay': ['le loi', 'ngo quyen', 'phu thinh', 'quang trung', 'son loc', 'trung hung', 'trung son tram', 'vien son', 'xuan khanh', 'co dong', 'duong lam', 'kim son', 'son dong', 'thanh my', 'xuan son'],
                'ba vi': ['tay dang', 'ba trai', 'cam linh', 'cam thuong', 'chau son', 'chu minh', 'co do', 'dong quang', 'dong thai', 'khanh thuong', 'minh chau', 'minh quang', 'phong van', 'phu chau', 'phu cuong', 'phu dong', 'phu phuong', 'phu son', 'son da', 'tan hong', 'tan linh', 'thai hoa', 'thuan my', 'thuy an', 'tien phong', 'tong bat', 'van hoa', 'van thang', 'vat lai', 'yen bai', 'ba vi'], 
                'chuong my': ['chuc son', 'xuan mai', 'dai yen', 'dong phuong yen', 'dong son', 'dong lac', 'dong phu', 'hoa chinh', 'hoang dieu', 'hoang van thu', 'hong phong', 'hop dong', 'huu van', 'lam dien', 'my luong', 'nam phuong tien', 'ngoc hoa', 'phu nam an', 'phu nghia', 'phung chau', 'quang bi', 'tan tien', 'tien phuong', 'tot dong', 'thanh binh', 'thuy xuan tien', 'thuy huong', 'thuong vuc', 'tran phu', 'trung hoa', 'truong yen', 'van vo'],
                'chuong mi': ['chuc son', 'xuan mai', 'dai yen', 'dong phuong yen', 'dong son', 'dong lac', 'dong phu', 'hoa chinh', 'hoang dieu', 'hoang van thu', 'hong phong', 'hop dong', 'huu van', 'lam dien', 'my luong', 'nam phuong tien', 'ngoc hoa', 'phu nam an', 'phu nghia', 'phung chau', 'quang bi', 'tan tien', 'tien phuong', 'tot dong', 'thanh binh', 'thuy xuan tien', 'thuy huong', 'thuong vuc', 'tran phu', 'trung hoa', 'truong yen', 'van vo'],
                'dan phuong': ['phung', 'dong thap', 'ha mo', 'hong ha', 'lien ha', 'lien hong', 'lien trung', 'phuong dinh', 'song phuong', 'tan hoi', 'tan lap', 'tho an', 'tho xuan', 'thuong mo', 'trung chau', 'dan phuong'],
                'dong anh': ['bac hong', 'co loa', 'dai mach', 'dong hoi', 'duc tu', 'hai boi', 'kim chung', 'kim no', 'lien ha', 'mai lam', 'nam hong', 'nguyen khe', 'tam xa', 'thuy lam', 'tien duong', 'uy no', 'van ha', 'van noi', 'viet hung', 'vinh ngoc', 'vong la', 'xuan canh', 'xuan non', 'dong anh'],
                'gia lam': ['trau quy', 'yen vien va 20 xa: bat trang', 'co bi', 'da ton', 'dang xa', 'phu thi', 'dong du', 'duong ha', 'duong quang', 'duong xa', 'kieu ky', 'kim lan', 'van duc', 'le chi', 'ninh hiep', 'dinh xuyen', 'phu dong', 'trung mau', 'yen thuong', 'yen vien', 'kim son'],
                'hoai duc': ['tram troi', 'an khanh', 'an thuong', 'cat que', 'dac so', 'di trach', 'dong la', 'duc giang', 'duc thuong', 'duong lieu', 'kim chung', 'la phu', 'lai yen', 'minh khai', 'son dong', 'song phuong', 'tien yen', 'van canh', 'van con', 'yen so'],
                'me linh': ['chi dong', 'quang minh', 'chu phan', 'dai thinh', 'hoang kim', 'kim hoa', 'lien mac', 'tam dong', 'thach da', 'thanh lam', 'tien phong', 'tien thang', 'tien thinh', 'trang viet', 'tu lap', 'van yen', 'van khe', 'me linh'],
                'my duc': ['dai nghia', 'an my', 'an phu', 'an tien', 'bot xuyen', 'dai hung', 'doc tin', 'dong tam', 'hong son', 'hop thanh', 'hop tien', 'hung tien', 'huong son', 'le thanh', 'my thanh', 'phu luu te', 'phuc lam', 'phung xa', 'thuong lam', 'tuy lai', 'van kim', 'xuy xa'],
                'mi duc': ['dai nghia', 'an my', 'an phu', 'an tien', 'bot xuyen', 'dai hung', 'doc tin', 'dong tam', 'hong son', 'hop thanh', 'hop tien', 'hung tien', 'huong son', 'le thanh', 'my thanh', 'phu luu te', 'phuc lam', 'phung xa', 'thuong lam', 'tuy lai', 'van kim', 'xuy xa'],
                'phu xuyen': ['phu minh va 25 xa: bach ha', 'chau can', 'chuyen my', 'dai thang', 'dai xuyen', 'hoang long', 'hong minh', 'hong thai', 'khai thai', 'minh tan', 'nam phong', 'nam tien', 'nam trieu', 'phu tuc', 'phu yen', 'phuc tien', 'phuong duc', 'quang lang', 'quang trung', 'son ha', 'tan dan', 'tri thuy', 'tri trung', 'van hoang', 'van tu', 'phu xuyen'],
                'phuc tho': ['hat mon', 'hiep thuan', 'lien hiep', 'long xuyen', 'ngoc tao', 'phuc hoa', 'phung thuong', 'sen phuong', 'tam hiep', 'tam thuan', 'thanh da', 'tho loc', 'thuong coc', 'tich giang', 'trach my loc', 'van ha', 'van nam', 'van phuc', 'vong xuyen', 'xuan dinh', 'phuc tho'],
                'quoc oai': ['can huu', 'cong hoa', 'dai thanh', 'dong quang', 'dong yen', 'hoa thach', 'liep tuyet', 'nghia huong', 'ngoc liep', 'ngoc my', 'phu cat', 'phu man', 'phuong cach', 'sai son', 'tan hoa', 'tan phu', 'thach than', 'tuyet nghia', 'yen son', 'dong xuan', 'quoc oai'],
                'soc son': ['bac phu', 'bac son', 'dong xuan', 'duc hoa', 'hien ninh', 'hong ky', 'kim lu', 'mai dinh', 'minh phu', 'minh tri', 'nam son', 'phu cuong', 'phu linh', 'phu lo', 'phu minh', 'quang tien', 'tan dan', 'tan hung', 'tan minh', 'thanh xuan', 'tien duoc', 'trung gia', 'viet long', 'xuan giang', 'xuan thu', 'soc son'],
                'thach that': ['binh phu', 'binh yen', 'cam yen', 'can kiem', 'canh nau', 'chang son', 'dai dong', 'di nau', 'dong truc', 'ha bang', 'huong ngai', 'huu bang', 'kim quan', 'lai thuong', 'phu kim', 'phung xa', 'tan xa', 'thach hoa', 'thach xa', 'tien xuan', 'yen binh', 'yen trung'],
                'thanh oai': ['kim bai', 'bich hoa', 'binh minh', 'cao duong', 'cao vien', 'cu khe', 'dan hoa', 'do dong', 'hong duong', 'kim an', 'kim thu', 'lien chau', 'my hung', 'phuong trung', 'tam hung', 'tan uoc', 'thanh cao', 'thanh mai', 'thanh thuy', 'thanh van', 'xuan duong'],
                'thanh tri': ['van dien', 'dai ang', 'dong my', 'duyen ha', 'huu hoa', 'lien ninh', 'ngoc hoi', 'ngu hiep', 'ta thanh oai', 'tam hiep', 'tan trieu', 'thanh liet', 'tu hiep', 'van phuc', 'vinh quynh', 'yen my'],
                'thuong tin': ['chuong duong', 'dung tien', 'duyen thai', 'ha hoi', 'hien giang', 'hoa binh', 'khanh ha', 'hong van', 'le loi', 'lien phuong', 'minh cuong', 'nghiem xuyen', 'nguyen trai', 'nhi khe', 'ninh so', 'quat dong', 'tan minh', 'thang loi', 'thong nhat', 'thu phu', 'tien phong', 'to hieu', 'tu nhien', 'van diem', 'van binh', 'van phu', 'van tu', 'van tao', 'thuong tin'],
                'ung hoa': ['van dinh', 'cao thanh', 'dai cuong', 'dai hung', 'doi binh', 'dong lo', 'dong tien', 'dong tan', 'hoa son', 'hoa lam', 'hoa nam', 'hoa phu', 'hoa xa', 'hong quang', 'kim duong', 'lien bat', 'luu hoang', 'minh duc', 'phu luu', 'phuong tu', 'quang phu cau', 'son cong', 'tao duong van', 'tram long', 'trung tu', 'truong thinh', 'van thai', 'vien an', 'vien noi']
        }

    def extract(self, addr):
        addr = str(addr)
        addr = unidecode(addr).lower()

        phuong, quan = None, None
        for it in self.quan_list:
            if it in addr:
                quan = it
                addr.replace(quan, ' ')
                break

        if quan is None:
            return None, None

        for it in self.phuong_list[quan]:
            if it in addr:
                phuong = it
                break
        
        return phuong, quan


def func(row):
    if len(str(row['price'])) == 3 or row['price'] == 'Thỏa thuận':
        return row['price']
    elif row['price'].find('tỷ') != -1 :
        import pdb; pdb.set_trace()
        return float(row['price'].split(' ')[0])*1000
    elif row['price'].find('triệu/m²') != -1:
        return float(row['price'].split(' ')[0])*row['area']
    else:
        return float(row['price'].split(' ')[0])

def findWard(x):
    if len(str(x)) == 3:
        return None
    else:
        extractor = AddressExtractor()
        phuong, quan = extractor.extract(x)
        return phuong
    # x = x.lower()
    # if x.find('-') != -1:
    #     x = x.replace('-',',')

    # if x.find('phường') != -1:
    #     return x.split('phường')[1].split(',')[0].strip()
    # else:
    #     # if len(x.split(',')) < 3:
    #     #     return 'KXD'
    #     # else:
    #     #     y = x.split(',')[-3].strip()
    #     #     if y.find('dự án') != -1 or y.find('phố') != -1 or y.find('đường') != -1 or y.find('hà nội') != -1:
    #     #         return 'KXD'
    #     #     else:
    #     #         return y
    #     return 'KXD' #15987


def findDistrict(x):
    if len(str(x)) == 3:
        return None
    else:
        extractor = AddressExtractor()
        phuong, quan = extractor.extract(x)
        return quan       
    # elif x.find(',') != -1:
    #     if x.lower().find('quận') != -1:
    #         return x.lower().split('quận')[1].split(',')[0].strip()
    #     else:
    #         return x.lower().split(',')[-2].strip()
    # elif x.find('-') != -1:
    #     x = x.lower()
    #     if x.find('quận') != -1:
    #         return x.split('quận')[1].split('-')[0].strip()
    #     else:        
    #         return x.split('-')[-2].strip()
    # else:
    #     return 'KXD'




def preprocess(data):
    #parse
    price = data.apply(func, axis = 1)
    square = data['area']
    bedrooms = data['bedrooms']
    bathrooms = data['toilets']
    ward = data['address'].apply(lambda x: findWard(x))
    district = data['address'].apply(lambda x : findDistrict(x))
    direction = data['direction']
    balcony_direction = data['balcony_direction']
    doc = data['law_doc'].apply(lambda x: 'đỏ' if str(x).lower().find('đỏ') != -1 else x).apply(lambda x: 'hồng' if str(x).lower().find('hồng') != -1 else x)
    law_doc = doc.apply(lambda x: 'có giấy tờ' if len(str(x)) > 4 else x)

    project = data['project']
    investor = data['investor']
    post_month = data['post_date'].apply(lambda x: x.split('/')[1].strip() if len(str(x)) > 3 else x)
    post_id = data['id']


    nhadatdf = {'id': post_id, 'month': post_month, 'project': project, 'investor': investor, 'square': square, 'bedrooms': bedrooms, 'bathrooms': bathrooms,'direction': direction,'balcony' : balcony_direction, 'district': district, 'ward': ward , 'law_doc': law_doc, 'price': price}
    dfBDS = pd.DataFrame(nhadatdf)
    return dfBDS


data1 = pd.read_json('data1_4000.json', orient='records', dtype= {"id" : "string", "bedrooms": "int", "toilets":"int"})
data2 = pd.read_json('data4000_7500.json', orient='records', dtype= {"id" : "string", "bedrooms": "int", "toilets":"int"})

# data1 = pd.read_json('data1_4000.json', orient='records')
# data2 = pd.read_json('data4000_7500.json', orient='records')

df1 = preprocess(data1) 
df2 = preprocess(data2)
dfBDS = df1.append(df2, ignore_index = True) 
dfBDS.to_csv (r'dfBDS.csv', index = False, header=True)

print('DONE')
