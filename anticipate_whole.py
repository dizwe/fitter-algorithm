from anticipate_size import *


def manual_answer(whole_d):
    user_sex = 'woman'
    user_height = 1770
    user_weight = 70

    shw_filtered_sizes = whole_d[user_sex]
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
    # 그냥 몸 부위별로 해서
    suggested_size = guess_int_by_question(question, size_each_parameter)  # 숫자니까..
    print(suggested_size)


def make_question_tree(whole_d):
    question_tree = {}
    for sex in ['woman']:  #, 'woman']:
        shw_filtered_sizes = whole_d[sex]
        height_key = list(shw_filtered_sizes.keys())
        height_key = list(map(int, height_key))  # 원래 문자니까
        question_tree[sex] = {}

        for height in range(min(height_key), max(height_key)+10, 10):
            question_tree[sex][height] = {}
            for weight in range(15, 105):  # 해보니 그렇던데?(남자,15,152)
                hw_filtered_size_nums = int_find_good_data(height, weight, shw_filtered_sizes)
                """"자료가 너무 멀어서 유의미 하지 않다면"""
                if hw_filtered_size_nums is None:
                    print(height, weight)
                    question_tree[sex][height][weight] = None
                    continue
                size_each_parameter = [[one_person[parameter]
                                        for one_person in hw_filtered_size_nums]
                                       for parameter in range(len(hw_filtered_size_nums[0]))]  # 변수개수만큼 돌리기

                par_list = ['shoulder', 'chest', 'arm', 'waist',
                            'bottom_waist', 'crotch', 'thigh', 'length', 'hem', 'hip',
                            'crotch_height', 'middle_thigh', 'knee', 'calf', 'nipple']

                parameter_answer_dict = {}
                for i, parameter in enumerate(size_each_parameter):
                    if len(set(parameter)) == 1:  # 자료 종류가 하나라면(여러개지만 다 똑같다)
                        parameter_answer = {'0': parameter[0],
                                            '1': parameter[0],
                                            '2': parameter[0]}
                    else:  # 종류가 여러개라면 질문에 맞춰서
                        sorted_param = sorted(parameter)
                        parameter_answer = {'0': get_median(sorted_param),
                                            '1': find_size_under_significance(sorted_param, start_index=-1),
                                            '2': find_size_under_significance(sorted_param, start_index=0)}

                    parameter_answer_dict[par_list[i]] = parameter_answer  # ~['shoulder'] ={0:,1:,2:}
                question_tree[sex][height][weight] = parameter_answer_dict

    return question_tree


def make_question_iter(whole_d):
    # data 과부하 줄이기
    for sex in ['man', 'woman']:
        shw_filtered_sizes = whole_d[sex]
        height_key = list(shw_filtered_sizes.keys())
        height_key = list(map(int, height_key))  # 원래 문자니까
        for height in range(min(height_key), max(height_key)+10, 10):
            for weight in range(15, 152):  # 해보니 그렇던데?
                yield (sex, height, weight)


if __name__ == "__main__":
    # 바뀌는 파트
    hw_filtered_sizes = readAndSave.read_json('whole_hw_filtered_survey_man_woman.json', 'utf8')
    readAndSave.save_json(make_question_tree(hw_filtered_sizes), 'question_tree_woman.json', 'utf8')
    # man = readAndSave.read_json('question_tree_man.json', 'utf8')
    # woamn = readAndSave.read_json('question_tree_woman.json', 'utf8')