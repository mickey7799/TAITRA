# coding: utf-8
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from tqdm import tqdm

PATH = 'file_repo/'
COUNTRY_CODE = {'Sudan (North + South)': '736', 'Bulgaria': '100', 'Tanzania, United Republic of': '834', 'Saint Vincent and the Grenadines': '670', 'Pitcairn': '612', 'Western Sahara': '732', 'Central African Republic': '140', 'Comoros': '174', 'Montenegro': '499', 'Barbados': '052', 'Gabon': '266', 'Bouvet Island': '074', 'Saint Helena': '654', 'Sri Lanka': '144', 'French South Antarctic Territories': '260', 'Vanuatu': '548', 'Taipei, Chinese': '490', 'Falkland Islands (Malvinas)': '238', 'Somalia': '706', 'Samoa': '882', 'Libya, State of': '434', 'Uruguay': '858', 'West Asia not elsewhere specified': '879', 'Christmas Islands': '162', 'Slovakia': '703', 'Andorra': '020', 'Denmark': '208', 'Djibouti': '262', 'Japan': '392', 'Burkina Faso': '854', 'Madagascar': '450', 'Romania': '642', 'Faroe Islands': '234', 'Trinidad and Tobago': '780', 'Tuvalu': '798', 'United Kingdom': '826', 'Seychelles': '690', 'Colombia': '170', 'Latvia': '428', 'Nepal': '524', 'French Polynesia': '258', 'Switzerland': '757', 'Chile': '152', 'Cayman Islands': '136', 'Mayotte': '175', 'Kenya': '404', 'Swaziland': '748', 'Guyana': '328', 'Sao Tome and Principe': '678', 'Centr.Amer.Com.Market (CACM) Nes': '471', 'Cambodia': '116', 'British Virgin Islands': '092', 'All': '-2', 'Maldives': '462', 'Europe Othr. Nes': '568', 'Croatia': '191', 'Honduras': '340', 'Guinea-Bissau': '624', 'Bahrain': '048', 'New Zealand': '554', 'Kiribati': '296', 'Azerbaijan': '031', 'Kazakhstan': '398', 'El Salvador': '222', 'Paraguay': '600', 'Eritrea': '232', 'Ecuador': '218', 'Aruba': '533', 'Marshall Islands': '584', 'Bolivia, Plurinational State of': '068', 'Ethiopia': '231', 'East Europe not elsewhere specified': '221', 'Saudi Arabia': '682', 'Norfolk Island': '574', 'Angola': '024', 'Norway': '579', 'Burundi': '108', 'St. Pierre and Miquelon': '666', 'British Indian Ocean Territories': '086', 'Lesotho': '426', 'Sierra Leone': '694', 'Bangladesh': '050', 'Macedonia, The Former Yugoslav Republic of': '807', 'Dominica': '212', 'Oman': '512', 'European Union Nes': '492', 'Guatemala': '320', 'Serbia and Montenegro': '891', 'Algeria': '012', 'New Caledonia': '540', "Cote d'Ivoire": '384', 'Asia not elsewhere specified': '946', 'Bhutan': '064', 'Serbia': '688', 'Timor-Leste': '626', 'Togo': '768', 'Afghanistan': '004', 'America not elsewhere specified': '636', 'North Africa not elsewhere specified': '290', 'Korea, Republic of': '410', 'Saint Kitts and Nevis': '659', 'Philippines': '608', 'Cyprus': '196', 'Guam': '316', 'Austria': '040', 'Thailand': '764', 'Brazil': '076', 'Russian Federation': '643', 'Neutral Zone': '536', 'China': '156', 'Cook Islands': '184', 'Egypt': '818', 'Pakistan': '586', 'Greece': '300', 'Tokelau': '772', 'Haiti': '332', 'South Africa': '710', 'Rwanda': '646', 'Armenia': '051', 'Suriname': '740', 'Viet Nam': '704', 'Ireland': '372', 'Benin': '204', 'Nauru': '520', 'Iraq': '368', 'Cabo Verde': '132', 'Wallis and Futuna Islands': '876', 'Malaysia': '458', 'Zambia': '894', 'Micronesia, Federated States of': '583', 'Cocos (Keeling) Islands': '166', 'Indonesia': '360', 'Gibraltar': '292', 'Lithuania': '440', 'Cameroon': '120', 'Argentina': '032', 'Israel': '376', 'Guinea': '324', 'Cuba': '192', 'Nicaragua': '558', 'Area Nes': '899', 'Nigeria': '566', 'Macao, China': '446', 'Senegal': '686', 'Uganda': '800', 'Singapore': '702', 'Costa Rica': '188', 'Mozambique': '508', 'Palestine, State of': '275', 'Fiji': '242', 'Bosnia and Herzegovina': '070', 'Belarus': '112', 'Turks and Caicos Islands': '796', 'Iran, Islamic Republic of': '364', 'Slovenia': '705', 'Albania': '008', 'Estonia': '233', 'Equatorial Guinea': '226', 'Saint Lucia': '662', 'Myanmar': '104', 'Montserrat': '500', 'Congo': '178', 'Netherlands': '528', 'Morocco': '504', 'Grenada': '308', 'Jordan': '400', 'North America and Central America, nes': '637', 'Czech Republic': '203', 'Kuwait': '414', 'Germany': '276', "Korea, Democratic People's Republic of": '408', 'Northern Mariana Islands': '580', 'Georgia': '268', 'India': '699', 'Uzbekistan': '860', 'Niger': '562', 'Finland': '246', 'Anguilla': '660', 'Netherlands Antilles': '530', 'Mauritania': '478', 'Iceland': '352', 'Brunei Darussalam': '096', 'Mongolia': '496', 'Tunisia': '788', 'Luxembourg': '442', 'Territory not allocated': '999', 'Palau': '585', 'Malta': '470', 'Tonga': '776', 'Kyrgyzstan': '417', 'Special categories': '839', 'Chad': '148', 'Belize': '084', 'Botswana': '072', 'France': '251', 'Jamaica': '388', 'British Antarctic Territories': '080', 'Portugal': '620', 'Free Zones': '838', 'Papua New Guinea': '598', 'Zimbabwe': '716', 'United States of America': '842', 'Ukraine': '804', "Lao People's Democratic Republic": '418', 'Hong Kong, China': '344', 'Tajikistan': '762', 'Venezuela, Bolivarian Republic of': '862', 'Ship stores and bunkers': '837', 'Italy': '381', 'Panama': '591', 'Turkmenistan': '795', 'Niue': '570', 'Liberia': '430', 'United Arab Emirates': '784', 'Syrian Arab Republic': '760', 'Peru': '604', 'Europe EFTA not elsewhere specified': '697', 'Mauritius': '480', 'Belgium': '056', 'Bahamas': '044', 'LAIA not elsewhere specified': '473', 'Malawi': '454', 'Antigua and Barbuda': '028', 'Hungary': '348', 'Moldova, Republic of': '498', 'Lebanon': '422', 'Spain': '724', 'Ghana': '288', 'Mexico': '484', 'Africa not elsewhere specified': '577', 'American Samoa': '016', 'Oceania Nes': '527', 'Turkey': '792', 'Congo, Democratic Republic of the': '180', 'Greenland': '304', 'Namibia': '516', 'Solomon Islands': '090', 'Dominican Republic': '214', 'United States Minor Outlying Islands': '849', 'Caribbean Nes': '129', 'Mali': '466', 'Sweden': '752', 'Canada': '124', 'Yemen': '887', 'Gambia': '270', 'Australia': '036', 'Qatar': '634', 'Poland': '616', 'Bermuda': '060'}

payload = {
'__EVENTTARGET':'',
'__EVENTARGUMENT':'',
'__LASTFOCUS':'',
'__VIEWSTATEGENERATOR':'4C5EB0C8',
'ctl00$HeaderControl$HiddenField_Prev_PageName':'',
'ctl00$HeaderControl$HiddenField_Current_PageName':'',
'ctl00$MenuControl$DDL_Language':'en',
'ctl00$MenuControl$HiddenField_Prev_LanguageCode':'',
'ctl00$MenuControl$HiddenField_Current_LanguageCode':'',
'ctl00$NavigationControl$DropDownList_Product':'TOTAL',
'ctl00$NavigationControl$DropDownList_Product_Group':'-2',
'ctl00$NavigationControl$Country_Selection':'RadioButton_Country',
'ctl00$NavigationControl$DropDownList_Country':'392',
'ctl00$NavigationControl$DropDownList_Country_Group':'-2',
'ctl00$NavigationControl$DropDownList_Partner':'156',
'ctl00$NavigationControl$DropDownList_Partner_Group':'-2',
'ctl00$NavigationControl$HiddenField_MenuDisplay':'1',
'ctl00$NavigationControl$DropDownList_TradeType':'E',
'ctl00$NavigationControl$DropDownList_OutputType':'TSY',
'ctl00$NavigationControl$DropDownList_OutputOption':'ByProduct',
'ctl00$NavigationControl$DropDownList_ProductClusterLevel':'6',
'ctl00$NavigationControl$DropDownList_TS_Indicator':'V',
'ctl00$NavigationControl$DropDownList_TS_Currency':'USD',
'ctl00$NavigationControl$HiddenField_ProductClusterLevel':'',
'ctl00$NavigationControl$HiddenField_Prev_ProductCode':'TOTAL',
'ctl00$NavigationControl$HiddenField_Prev_ServiceCode':'',
'ctl00$NavigationControl$HiddenField_Prev_ProductGroupCode':'',
'ctl00$NavigationControl$HiddenField_Prev_ProductClusterLevel':'6',
'ctl00$NavigationControl$HiddenField_Prev_CountryCode':'392',
'ctl00$NavigationControl$HiddenField_Prev_CountryGroupCode':'',
'ctl00$NavigationControl$HiddenField_Prev_PartnerCode':'156',
'ctl00$NavigationControl$HiddenField_Prev_PartnerGroupCode':'',
'ctl00$NavigationControl$HiddenField_Prev_OutputOption':'ByProduct',
'ctl00$NavigationControl$HiddenField_Prev_OutputType':'TS',
'ctl00$NavigationControl$HiddenField_Prev_DirectMirror':'D',
'ctl00$NavigationControl$HiddenField_Prev_TS_FrequencyData':'Y',
'ctl00$NavigationControl$HiddenField_Prev_TS_Indicator':'V',
'ctl00$NavigationControl$HiddenField_Prev_DataFamilyType':'P',
'ctl00$NavigationControl$HiddenField_Prev_QuantityUnit':'QUNIT1',
'ctl00$NavigationControl$HiddenField_Current_ProductCode':'TOTAL',
'ctl00$NavigationControl$HiddenField_Current_ServiceCode':'',
'ctl00$NavigationControl$HiddenField_Current_ProductGroupCode':'',
'ctl00$NavigationControl$HiddenField_Current_ProductClusterLevel':'6',
'ctl00$NavigationControl$HiddenField_Current_CountryCode':'392',
'ctl00$NavigationControl$HiddenField_Current_CountryGroupCode':'',
'ctl00$NavigationControl$HiddenField_Current_PartnerCode':'156',
'ctl00$NavigationControl$HiddenField_Current_PartnerGroupCode':'',
'ctl00$NavigationControl$HiddenField_Current_OutputOption':'ByProduct',
'ctl00$NavigationControl$HiddenField_Current_OutputType':'TS',
'ctl00$NavigationControl$HiddenField_Current_DirectMirror':'D',
'ctl00$NavigationControl$HiddenField_Current_TS_FrequencyData':'Y',
'ctl00$NavigationControl$HiddenField_Current_TS_Indicator':'V',
'ctl00$NavigationControl$HiddenField_Current_DataFamilyType':'P',
'ctl00$NavigationControl$HiddenField_Current_QuantityUnit':'QUNIT1',
'ctl00$PageContent$GridViewPanelControl$ImageButton_ExportExcel.x':'13',
'ctl00$PageContent$GridViewPanelControl$ImageButton_ExportExcel.y':'5',
'ctl00$PageContent$GridViewPanelControl$HiddenField_OldNumTimePeriod':'3',
'ctl00$PageContent$GridViewPanelControl$HiddenField_OldGridViewColumns':'51',
'ctl00$PageContent$GridViewPanelControl$HiddenField_CurrentLastTimePeriod':'2016',
'ctl00$PageContent$GridViewPanelControl$DropDownList_NumTimePeriod':'3',
'ctl00$PageContent$GridViewPanelControl$DropDownList_PageSize':'300',
'ctl00$PageContent$GridViewPanelControl$HiddenField_Prev_OutputMode':'T',
'ctl00$PageContent$GridViewPanelControl$HiddenField_Prev_PageSizeTab':'300',
'ctl00$PageContent$GridViewPanelControl$HiddenField_Prev_TS_NumTimePeriod':'3',
'ctl00$PageContent$GridViewPanelControl$HiddenField_Prev_TS_NumTimePeriod_TS':'3',
'ctl00$PageContent$GridViewPanelControl$HiddenField_Prev_TS_LastTimePeriod':'2016',
'ctl00$PageContent$GridViewPanelControl$HiddenField_Prev_TS_ReferencePeriod':'2015',
'ctl00$PageContent$GridViewPanelControl$HiddenField_Current_OutputMode':'T',
'ctl00$PageContent$GridViewPanelControl$HiddenField_Current_PageSizeTab':'300',
'ctl00$PageContent$GridViewPanelControl$HiddenField_Current_TS_NumTimePeriod':'3',
'ctl00$PageContent$GridViewPanelControl$HiddenField_Current_TS_NumTimePeriod_TS':'3',
'ctl00$PageContent$GridViewPanelControl$HiddenField_Current_TS_LastTimePeriod':'2016',
'ctl00$PageContent$GridViewPanelControl$HiddenField_Current_TS_ReferencePeriod':'2015',
'ctl00$PageContent$GridViewPanelControl$HiddenProductLabelLongTitle':'false',
'ctl00$PageContent$GridViewPanelControl$HiddenProductLabelLongGrid':'false',
}

headers = {
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
'Referer':'http://trademap.org/Bilateral_TS.aspx',
'Content-Type':'application/x-www-form-urlencoded',
'Cookie':'ASP.NET_SessionId=r4e5i4vtdizott45crpdeu55;trademap.org=E8725B453D161309ED60C54A4785D9EB374363A4265E6765A9CA98DEC8FC4F58AEC9FE8B55D8C110D66BBA9FB7F59661857797FFE4C5EC669088FA6D90BB43F14A4C95EF9EB6DCD718A3514496B7F5A2B6FB88D42D388711805DEE44CE31AD147557DA510B635E91A2FF646C83E2A69CF02C2F03F3DF0CA40DC4116341C266D9F0F32CE7;AspxAutoDetectCookieSupport=1',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36'
}


def reloginPage(username, password):
    ''' Use username and password to login the page and get the cookie'''
    c = None
    try:
        driver = webdriver.Chrome('./drivers/chromedriver.exe')
        driver.implicitly_wait(30)
        driver.get('http://trademap.org/Bilateral_TS.aspx')
        time.sleep(5)

        driver.find_element_by_id("ctl00_MenuControl_Img_Login").click()
        time.sleep(5)
        driver.switch_to_frame("iframe_login")
        time.sleep(5)

        driver.find_element_by_id("ctl00_PageContent_Login1_UserName").click()
        driver.find_element_by_id("ctl00_PageContent_Login1_UserName").clear()
        driver.find_element_by_id("ctl00_PageContent_Login1_UserName").send_keys(username)
        driver.find_element_by_id("ctl00_PageContent_Login1_Password").clear()
        driver.find_element_by_id("ctl00_PageContent_Login1_Password").send_keys(password)
        driver.find_element_by_id("ctl00_PageContent_Login1_Button").click()
        time.sleep(5)

        c =  ';'.join(['{}={}'.format(ele['name'], ele['value'])for ele in  driver.get_cookies()])

        driver.close()
        return c
    finally:
        try: driver.quit()
        except: pass


def getCountryXLSX(country_code, partner_code, trade_type):
    with requests.Session() as rs:
        # setup country code
        payload['__VIEWSTATEGENERATOR'] = '4C5EB0C8'

        #setup payload
        res = rs.get('http://www.trademap.org/Bilateral_TS.aspx', headers = headers)
        bs = BeautifulSoup(res.text, 'html.parser')
        for input_box in bs.select('input[type=hidden]'):
            if input_box['name'] == '__VIEWSTATE':
                payload[input_box['name']] = input_box['value']
    
        payload['ctl00$NavigationControl$DropDownList_TradeType']          = trade_type
        payload['ctl00$NavigationControl$DropDownList_Country']            = country_code
        payload['ctl00$NavigationControl$HiddenField_Prev_CountryCode']    = country_code
        payload['ctl00$NavigationControl$HiddenField_Current_CountryCode'] = country_code
    
        payload['ctl00$NavigationControl$DropDownList_Partner']            = partner_code
        payload['ctl00$NavigationControl$HiddenField_Prev_PartnerCode']    = partner_code
        payload['ctl00$NavigationControl$HiddenField_Current_PartnerCode'] = partner_code

        # Write HTML into file
        with open(PATH+'{}_{}_{}.html'.format(country_code,partner_code,trade_type), 'wb') as f:
            res2 = rs.post('http://trademap.org/Bilateral_TS.aspx', data= payload, headers = headers)
            f.write(res2.content)

        ### Need to add assert to ensure that we got the right table
        ### ->

def checkHtml(res):
    pass

def combineHtmlToDataframe(reporter_code):
    """To reduce html file amoung"""
    pass


if __name__ == '__main__':
    # get cookie 
    c = reloginPage('l483120@mvrht.com', '1qaz@WSX')
    headers['Cookie'] = c
    if c is not None: 
        # iterate through all countries
        for reporter in tqdm(COUNTRY_CODE.values()):
            
            for partner in COUNTRY_CODE.values():
                if reporter != partner:
                    for trade_type in ['I']: # E for export or I for import
                        print(reporter, partner, trade_type)
                        getCountryXLSX(reporter, partner, trade_type)
