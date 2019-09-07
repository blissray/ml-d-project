Lab #9 - File IO Example (file_io_example)
=======
Copyright 2017 © document created by teamLab.gachon@gmail.com

## Introduction
이번 Lab은 다행히도 어렵지 않으며 함수도 5개밖에 없습니다.
이번 Lab은 Text Handling 시리즈의 첫 번째 Lab입니다. 이번 Lab은 간단한 파일을 다운로드 받고, 파일안에 있는 정보를 추출하는 것을 목표로 합니다. 그러면 이제 바로 본론으로 들어가도록 하겠습니다.

## 숙제 template 파일 다운로드
먼저 숙제 template 파일을 다운받아야 합니다. Chrome 또는 익스플로러와 같은 웹 브라우저 주소창에 아래 주소를 입력합니다.

https://github.com/TeamLab/Gachon_CS50_Python_KMOOC/blob/master/lab_assignment/lab_9/lab_9.zip

다운로드를 위해 View Raw 또는 Download 버튼을 클릭합니다. 또는 Lab 9 - 다운로드 링크 를 클릭하면 자동으로 다운로드가 됩니다. 다운로드 된 lab_9.zip 파일을 작업 폴더로 이동한 후 압축해제 후 작업하길 바랍니다.


## file_io_example.py 파일 Overview
`atom`으로 `file_io_example.py`을 열어 전체적인 개요를 살펴봅시다. 이번 Lab은 오직 5개의 함수로만 구성되어 있으며, Main 함수는 존재하지 않습니다.

이제 수정해야 할 함수 리스트를 살펴봅시다.

함수           | 설명
--------       | ---
get_file_contents | 문자열값으로 filename을 입력받아 해당 파일에 존재하는 모든 text 데이터를 문자열 형태로 반환함
get_number_of_characters_with_blank | 문자열값으로 filename을 입력받아 해당 파일에 존재하는 모든 글자의 갯수를 integer 값으로 반환함
get_number_of_characters_without_blank | 문자열값으로 filename을 입력받아 해당 파일에 존재하는 모든 글자의 갯수를 공백을 제외하고 integer 값으로 반환함. 단 여기서 공백은 " ", "\t", "\n" 을 의미함
get_number_of_lines | 문자열값으로 filename을 입력받아 해당 파일에 존재하는 모든 줄(line)수를  integer 값으로 반환함. 이때 마지막 줄은 count에서 제외함
get_number_of_target_words | 문자열값으로 filename과 찾고자하는 target_words을 입력받아 해당 파일에 존재하는 target_words와 같은 글자의 수를 대소문자와 상관없이 integer 값으로 반환함


## 결과확인
정말 쉽습니다. cmd창에서 작업 폴더로 이동하신 후, python shell에서 간단하게 test 한다면 다음과 같은 결과가 나올 것입니다.

```python
Type "help", "copyright", "credits" or "license" for more information.
>>> import file_io_example as fie
>>> fie.get_file_contents("1984.txt").split("\n")[0]
'GEORGE ORWELL'
>>> fie.get_number_of_characters_with_blank("1984.txt")
558840
>>> fie.get_number_of_characters_without_blank("1984.txt")
459038
>>> fie.get_number_of_lines("1984.txt")
1414
>>> fie.get_number_of_target_words("1984.txt", "Hi")
3938
>>> fie.get_number_of_target_words("1984.txt", "had")
1327
>>> exit()
```

## 숙제 제출하기
모든 함수를 다 수정했다면, 아래와 같이 제출하시면 됩니다.
- `windows`+`r`를 누르고 cmd 입력 후 확인을 클릭합니다.
- 작업폴더로 경로를 이동합니다.
- cmd 창에서 아래의 코드를 입력합니다.

```python
python submit.py
```

제대로 작성했다면 아래와 같은 메세지가 뜰 것입니다.
```bash
-------------------- | ---------- | --------------------
       Function Name |    Passed? |             Feedback
-------------------- | ---------- | --------------------
 get_number_of_lines |       PASS |             Good Job
   get_file_contents |       PASS |             Good Job
get_number_of_characters_with_blank |       PASS |             Good Job
get_number_of_characters_without_blank |       PASS |             Good Job
get_number_of_target_words |       PASS |             Good Job
-------------------- | ---------- | --------------------
```  

## Next Work
이번 랩은 어렵지 않아서 많은 시간을 들이지 않고 금방 푸셨을겁니다. 보너스로 2개의 Lab이 남아있습니다. 그리고 당신 (비기너) 파이썬 마스터가 될 것입니다.

> **Human knowledge belongs to the world** - from movie 'Password' -

## Footnotes
