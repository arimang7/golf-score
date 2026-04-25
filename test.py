import re
kor_num_map = {'영': '0', '공': '0', '빵': '0', '병': '0', '용': '0', '형': '0', '엉': '0', '명': '0', '정': '0', '경': '0', '일': '1', '인': '1', '실': '1', '일번': '1', '임': '1', '일은': '1', '이': '2', '리': '2', '이는': '2', '삼': '3', '산': '3', '상': '3', '사': '4', '사는': '4', '오': '5', '어': '5', '오는': '5'}
t = '1 -1 공 3'
mapped_text = ''
is_negative = False
for char in t:
    if char == '-':
        is_negative = True
    elif char.isdigit():
        if is_negative:
            mapped_text += f'-{char} '
            is_negative = False
        else:
            mapped_text += f'{char} '
    elif char in kor_num_map:
        val = kor_num_map[char]
        if is_negative:
            mapped_text += f'-{val} '
            is_negative = False
        else:
            mapped_text += f'{val} '
print(re.findall(r'-?\d+', mapped_text))