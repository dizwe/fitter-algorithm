from anticipate_size import *

if __name__ == "__main__":
    """하의"""
    # 바뀌는 파트
    hw_filtered_sizes = readAndSave.read_json('bottom_hw_filtered_survey.json', 'utf8')
    user_height = 1770
    user_weight = 70

    # 괜찮은 사이즈를 찾고 글자 데이터를 숫자로 바꾸기
    hw_filtered_size_nums = int_find_good_data(user_height, user_weight, hw_filtered_sizes)

    # 몸 부위별로 모으기
    size_each_parameter = [[one_person[parameter]
                            for one_person in hw_filtered_size_nums]
                           for parameter in range(len(hw_filtered_size_nums[0]))]  # 변수개수만큼 돌리기

    """예상 사이즈 추천하기"""
    # 답변에 따라서
    # ['waist', 'crotch', 'thigh', 'length', 'hem', 'hip'] 순서
    question = [0, 1, 2, 1, 1, 2]  # ~하면 가 남는 편이다
    suggested_size = guess_int_by_question(question, size_each_parameter)  # 숫자니까..
    # suggested_real = size_to_real(suggested_size)
    print(suggested_size)