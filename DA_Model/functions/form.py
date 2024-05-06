def save_responses(responses, job, brief1, brief2, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write("텍스트 입력 응답들:\n")
        for key, value in responses.items():
            file.write(f"{key}: {value}\n")
        file.write('\n경력사항: \n')
        for item in job:
            file.write(item)
            file.write('\n')
        file.write('\n자기소개서 1: \n')
        file.write(brief1)
        file.write('\n자기소개서 2: \n')
        file.write(brief2)
