# -*- coding: utf8 -*-

import urllib.request
import csv

def get_stock_data(url_address):
    """url_address로 Yahoo 서버에 요청하면 해당 정보를 다운로드 받은후 Two Dimensional List 변환하여 반환함

    아래 코드를 활용하면 Yahoo 서버에서 데이터를 String Type으로 다운로드 받을 수 있음

        >>> url_address = 'http://real-chart.finance.yahoo.com/table.csv?s=005930.KS&a=0&b=1&c=2013&d=11&e=31&f=2015&g=d'
        >>> r = urllib.request.urlopen(url_address)
        >>> stock_data_string = r.read().decode("utf8")    # String Type으로 다운로드 받은 데이터
        >>> stock_data_string[:100]
    'Date,Open,High,Low,Close,Volume,Adj Close\n2015-11-06,1343000.00,1348000.00,1330000.00,1338000.00,164'

    다운된 데이터는 String Type으로 각 줄은 "\n"으로 구분되며, 필드 데이터들은 ","으로 구분됨

    Args:
        url_address (str): Yahoo 금융 서버에 주식 csv 데이터를 요청하는 URL 주소

    Returns:
        list: Two Dimensioanl List 0번째 index에는 필드의 Header 정보를 포함하고 있으며,
        1번째 index부터 각 필드의 data를 가지고 있음

    Examples:
        >>> import stock_data_crawler as sdc
        >>> url = 'http://real-chart.finance.yahoo.com/table.csv?s=005930.KS&a=0&b=1&c=2013&d=11&e=31&f=2015&g=d'
        >>> sdc.get_stock_data(url)[:3]
        [['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close'], ['2015-11-06',
         '1343000.00', '1348000.00', '1330000.00', '1338000.00', '164300', '1338000.00']
        , ['2015-11-05', '1330000.00', '1354000.00', '1330000.00', '1342000.00', '173000
        ', '1342000.00']]
    """
    r = urllib.request.urlopen(url_address)
    stock_data_string = r.read().decode("utf8")
    result = None
    # ===Modify codes below=============

    # ==================================
    return result


def get_header_data(stock_data):
    """get_stock_data 함수의 Return 값에서 Header 값만 추출하여 list로 반환함

    Args:
        stock_data (list): get_stock_data 함수의 Return 값으로 나온 주식 정보 two dimensional list

    Returns:
        list: 입력된 stcok_data list 값 중 0번째 index에 있는 header 정보만 추출하여 반환함

    Examples:
        >>> import stock_data_crawler as sdc
        >>> url = 'http://real-chart.finance.yahoo.com/table.csv?s=005930.KS&a=0&b=1&c=2013&d=11&e=31&f=2015&g=d'
        >>> stock_data = sdc.get_stock_data(url)
        >>> sdc.get_header_data(stock_data)
        ['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 'Adj Close']
    """
    result = None
    # ===Modify codes below=============

    # ==================================
    return result


def get_attribute_data(stock_data, attribue, year=None, month=None):
    """get_stock_data 함수의 Return 값,추출하고자 하는 Header의 이름, 추출하고자 하는 년도, 월을 입력받으면
    해당 조건의 값만 추출하여 list로 반환함

    Note:
        입력할 경우 stock_data, attribue는 필수 입력이나,
        year 값을 입력하지 않을 경우에는 attribute에 해당하는 전체 값,
        year 값만 입력할 경우에는 attribute와 년도에 해당하는 값을
        month까지 입력했을 경우, attribute와 년도, 월에 해당하는 값을 추출함
        year를 입력하지 않으면 month를 입력하지 않는 걸로 가정함

    Args:
        stock_data (list): get_stock_data 함수의 Return 값으로 나온 주식 정보 two dimensional list
        attribue (str): 추출하고자 하는 필드의 Header 이름, 대소문자를 구분함
        year (int): 추출하고자 하는 년도, 입력하지 않을 경우 전체 값을 추출함 (default = None)
        month (int): 추출하고자 하는 월, 년도를 입력하지 않을 경우 입력할 수 없음 (default = None)

    Returns:
        list: 입력된 조건에 맞는 값을 header를 포함하여 list로 추출하여 반환함

    Examples:
        >>> import stock_data_crawler as sdc
        >>> url = 'http://real-chart.finance.yahoo.com/table.csv?s=005930.KS&a=0&b=1&c=2013&d=11&e=31&f=2015&g=d'
        >>> stock_data = sdc.get_stock_data(url)
        >>> header = sdc.get_header_data(stock_data)
        >>> sdc.get_attribute_data(stock_data, "High", 2014, 12)[:2]
        [['Date', 'High'], ['2014-12-31', '1327000.00']]
        >>> sdc.get_attribute_data(stock_data, header[1], 2013, 12)[:2]
        [['Date', 'Open'], ['2013-12-31', '1372000.00']]
    """

    result = None
    # ===Modify codes below=============

    # ==================================
    return result

def get_average_value_of_attribute(stock_data, attribue, year=None, month=None):
    """get_stock_data 함수의 Return 값,추출하고자 하는 Header의 이름, 추출하고자 하는 년도, 월을 입력받으면
    해당 조건의 값의 평균을 float Type으로 반환함

    Note:
        입력할 경우 stock_data, attribue는 필수 입력이나,
        year 값을 입력하지 않을 경우에는 attribute에 해당하는 전체 값,
        year 값만 입력할 경우에는 attribute와 년도에 해당하는 값을
        month까지 입력했을 경우, attribute와 년도, 월에 해당하는 값을 추출함
        year를 입력하지 않으면 month를 입력하지 않는 걸로 가정함

    Args:
        stock_data (list): get_stock_data 함수의 Return 값으로 나온 주식 정보 two dimensional list
        attribue (str): 추출하고자 하는 필드의 Header 이름, 대소문자를 구분함
        year (int): 추출하고자 하는 년도, 입력하지 않을 경우 전체 값을 추출함 (default = None)
        month (int): 추출하고자 하는 월, 년도를 입력하지 않을 경우 입력할 수 없음 (default = None)

    Returns:
        float: 입력된 조건에 맞는 header를 제외하고 list로 추출한 후 (전체합 / 데이터 갯수)로 계산하여 반환함

    Examples:
        >>> import stock_data_crawler as sdc
        >>> url = 'http://real-chart.finance.yahoo.com/table.csv?s=005930.KS&a=0&b=1&c=2013&d=11&e=31&f=2015&g=d'
        >>> stock_data = sdc.get_stock_data(url)
        >>> header = sdc.get_header_data(stock_data)
        >>> sdc.get_average_value_of_attribute(stock_data, "Open", 2013, 12)
        1423909.0909090908
        >>> sdc.get_average_value_of_attribute(stock_data, "Open", 2014, 12)
        1313043.4782608696
        >>> sdc.get_average_value_of_attribute(stock_data, header[3], 2014, 12)
        1301260.8695652173
    """

    result = None
    # ===Modify codes below=============

    # ==================================
    return result

def write_csv_file_by_result(stock_data, filename):
    """stock_data를 가지고 있는 two dimensional list 값을 csv 파일로 생성함

    Args:
        stock_data (list): 저장하고자 하는 주식 정보 two dimensional list
        filename (str): 데이터가 저장될 파일이름

    Examples:
        >>> import stock_data_crawler as sdc
        >>> url = 'http://real-chart.finance.yahoo.com/table.csv?s=005930.KS&a=0&b=1&c=2013&d=11&e=31&f=2015&g=d'
        >>> stock_data = sdc.get_stock_data(url)
        >>> high_data = sdc.get_attribute_data(stock_data, "High", 2014, 12)
        >>> sdc.write_csv_file_by_result(stock_data,"example.csv")
        >>> f = open("example.csv", "r", encoding="utf8")
        >>> f.read()[:100]
        'Date,Open,High,Low,Close,Volume,Adj Close\n2015-11-06,1343000.00,1348000.00,133
        0000.00,1338000.00,164'
        >>> f.close()
    """
    result = None
    # ===Modify codes below=============

    # ==================================
    return result


def separate_user_query(user_input):
    """사용자의 입력 값을 종류별로 나눠 list로 반환하며 반드시 각 list에 값들은 빈칸이 제거된 후 저장되어야함

    Note:
        사용자의 입력은 ","를 사용하여 구분되며, 예시는 아래와 같음
        SAMSUNG, 2014-12, Open, ALL
        첫 번째는 다운로드 하고자 하는 회사명, 현 숙제에서는 바뀌지 않음
        두 번째는 추출할 년도-월 정보
        세 번째는 추출한 Header 이름
        네 번째는 추출 유형 - ALL, MEAN, FILE 이 있으며 대소문자를 구분하지 않음
         ALL - 조건의 맞는 모든 데이터를 모두 추출하는 명령어 get_attribute_data를 사용함
         MEAN - 조건의 맞는 모든 데이터를 모두 추출하여 평균을 계산하는 명령어 get_average_value_of_attribute 사용함
         FILE - 조건의 맞는 모든 데이터를 모두 추출한 후 파일로 저장하는 명령어 write_csv_file_by_result 사용함
                FILE을 입력할 경우 파일명을 FILE 다음에 작성해 주어야 함
                ex) SAMSUNG, 2014-12, Open, FILE, test.csv

    Args:
        user_input (str): 사용자가 입력하는 데이터 ex) SAMSUNG, 2014-12, Open, ALL

    Returns:
        list: user_input을 "," 기준으로 분할하여 list 값으로 반환함, 단 각 list에 있는 값들은 양쪽 공백이 제거되어야 함

    Examples:
        >>> import stock_data_crawler as sdc
        >>> sdc.separate_user_query("SAMSUNG, 2014-12, Open, ALL")
        ['SAMSUNG', '2014-12', 'Open', 'ALL']
        >>> sdc.separate_user_query("SAMSUNG, 2014-12, Open, FILE, example.csv")
        ['SAMSUNG', '2014-12', 'Open', 'FILE', 'example.csv']
        >>> sdc.separate_user_query("SAMSUNG, 2014-13, High, MEAN, example.csv")
        ['SAMSUNG', '2014-13', 'High', 'MEAN', 'example.csv']
    """
    result = None
    # ===Modify codes below=============

    # ==================================
    return result


def main():
    print("Stock Data Crawler Program!!")
    user_input = 999
    url = 'http://real-chart.finance.yahoo.com/table.csv?s=005930.KS&a=0&b=1&c=2013&d=11&e=31&f=2015&g=d'
    # ===Modify codes below=============

    # ==================================

if __name__=="__main__":
    main()