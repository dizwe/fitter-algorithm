from anticipate_size import *

if __name__ == "__main__":
    # 바뀌는 파트
    hw_filtered_sizes = readAndSave.read_json('whole_hw_filtered_survey_man_woman.json', 'utf8')
    user_sex = 'woman'
    user_height = 1770
    user_weight = 70

    shw_filtered_sizes = hw_filtered_sizes[user_sex]
    # 괜찮은 사이즈를 찾고 글자 데이터를 숫자로 바꾸기
    hw_filtered_size_nums = int_find_good_data(user_height, user_weight, shw_filtered_sizes)

    # 몸 부위별로 모으기
    size_each_parameter = [[one_person[parameter]
                            for one_person in hw_filtered_size_nums]
                           for parameter in range(len(hw_filtered_size_nums[0]))]  # 변수개수만큼 돌리기

    """예상 사이즈 추천하기"""
    # 답변에 따라서
    # ['shoulder', 'chest', 'arm', 'waist'
    # 'bottom_waist', 'crotch', 'thigh', 'length', 'hem', 'hip',
    # 'crotch_height', 'middle_thigh', 'knee', 'calf', 'nipple']
    question = [0, 2, 1, 1,
                1, 2, 2, 1, 1, 2,
                1, 1, 2, 1, 2, 2]
    suggested_size = guess_int_by_question(question, size_each_parameter)  # 숫자니까..
    print(suggested_size)