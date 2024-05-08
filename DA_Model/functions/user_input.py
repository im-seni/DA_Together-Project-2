def get_input (prompt, choices=None, multi_selection =False):
    while True:
        if choices:
            for index, choice in enumerate(choices):
                print(f"{index + 1}. {choice}")
            print('복수 선택은 쉼표(,)로 구분하여 번호를 입력해주세요. (예: 1, 2, 3)')
            user_input = input(prompt)
            if multi_selection:
                try:
                    selected_indices = [int(i) for i in user_input.split(',')]
                    if all(0 < i <= len(choices) for i in selected_indices):
                        return [choices[i - 1] for i in selected_indices]
                    else:
                        print('하나 이상의 유효하지 않은 입력이 있습니다. 다시 시도해주세요.')
                except ValueError:
                    print('유효하지 않은 입력입니다. 다시 시도해주세요.')
            else:
                if user_input.isdigit() and 0 < int(user_input) <= len(choices):
                    return choices[int(user_input) - 1]
                else:
                    print('유효하지 않은 입력입니다. 다시 시도해주세요.')
        else:
            user_input = input(prompt)
            return user_input

def navigate(questions, responses):
    current = 0 
    while current < len(questions):
        key, question, choices, multi_selection = questions[current]
        responses[key] = get_input(question, choices, multi_selection)

        if current < len(questions) - 1:
                next = input('다음 질문으로 넘어가려면 엔터를 누르고, 이전 질문으로 돌아가려면 back을 입력해주세요')
                if next.strip().lower() == 'back':
                    current = max(0, current - 1)
                else:
                    current += 1
        else:
            break