import json
import time
import requests

import google.generativeai as genai
import os


def stt(id, pwd, audio_path):
    resp = requests.post(
        'https://openapi.vito.ai/v1/authenticate',
        data={'client_id': id,
            'client_secret': pwd}
    )

    access = resp.json()['access_token']

    config = {}
    resp = requests.post(
        'https://openapi.vito.ai/v1/transcribe',
        headers={'Authorization': 'bearer '+access},
        data={'config': json.dumps(config)},
        files={'file': open(audio_path, 'rb')}
    )

    ids = resp.json()['id']

    time.sleep(2.5)

    conversation = requests.get(
        'https://openapi.vito.ai/v1/transcribe/'+ids,
        headers={'Authorization': 'bearer '+access},
    )

    conv = []

    for con in conversation.json()['results']['utterances']:
        conv.append(con['msg'])
    results = ''.join(conv)

    print('귀하의 입력 정보는 아래와 같습니다 : ', results)

    return results

# prompt engineering

def career(user, model):
    prompt = f'''<<너의 역할은 사용자의 대답에서 근무 기간과 직책, 수행 업무를 각각 분리해 정리하는거야. 네가 정리한 내용은 이력서에 들어갈 내용이니 
            정확성과 신뢰성이 무엇보다 중요해. 사용자 응답에서 정보를 찾을 수 없다면 절대 답을 만들어내지 말고 "정보 없음"으로 답해줘.>>
            
            Input :1995년부터 2008년까지 약 14년간 KT에서 인사 담당자로 근무했습니다. 
            사원에서 시작해서 팀장 직책까지 달았지요. 주로 신입사원 교육 프로그램 구성을 담당했습니다. 
            오랜 시간 근무한만큼 사회적 흐름도 빠르게 변화했는데, 변화의 물결에 뒤쳐지지 않는 프로그램 구성으로 인정받아왔습니다. 
            그 다음으로는 복지재단으로 옮겨 가서 5년간 강사로 일했어요. 거기서도 노인들을 대상으로 한 교육 프로그램을 구성하고 진행하는 역할을 담당했지요. 

            Output : 1995-2008,인사 담당자 (팀장),신입사원 교육 프로그램 구성, \n
                     정보 없음,강사,노인 대상 프로그램 구성 및 진행 
            
            위의 예시를 참고해 답변해줘. 아래는 사용자 응답이야.
            {user}'''
    return model.generate_content(prompt)

def introduce1(motivation, career, model):
    prompt = f'''<<너의 역할은 사용자 경력 정보를 바탕으로 자기소개서 내용을 "줄글로 풀어서" 작성하는거야. 질문은 아래와 같아
        (1) 지원 동기 및 직무 적합성 : 귀하의 지원 동기와 직무 적합성을 간략하게 소개해주세요.

        네가 답변을 작성할 때 "반드시" 유의해야 할 사항 몇 가지를 더 알려줄게 : 
        - 답변을 작성할 때는, 지원 동기와 경력 정보를 모두 포함해 작성해줘. 단, 유사한 내용이 반복되지 않도록 주의해줘
        - 가능하다면 답변은 공백 제외 300자 이상, 450자 이하가 되어야 해. 명심해!

        
        네가 작성한 내용은 실제 구직자의 이력서와 자기소개서가 되어 기업 인사 담당자에게 전달될거야. 그만큼 중요한 일이고.
        아래 질문 중 사용자 응답에서 정보를 찾을 수 없는 내용이 있다면, 답을 만들어내지 말고 "정보 없음"이라고 답변해줘.
        자기소개서 항목을 작성할 때는, 사용자 답변 내용을 함축적으로 담을 수 있는 소제목을 꼭 설정해줘.>>
        
        Input1 :
            경력 정보 : 1995년부터 2008년까지 약 14년간 KT에서 인사 담당자로 근무했습니다. 
            사원에서 시작해서 팀장 직책까지 달았지요. 주로 신입사원 교육 프로그램 구성을 담당했습니다. 
            오랜 시간 근무한만큼 사회적 흐름도 빠르게 변화했는데, 변화의 물결에 뒤쳐지지 않는 프로그램 구성으로 인정받아왔습니다. 
            그 다음으로는 복지재단으로 옮겨 가서 5년간 강사로 일했어요. 거기서도 노인들을 대상으로 한 교육 프로그램을 구성하고 진행하는 역할을 담당했지요. 
            
            지원 동기 : 저는 한평생 함께하는 성장을 위해 노력해 온 사람입니다. KT에서 인사 담당자로 근무하며 신입사원 교육 프로그램을 구성하는 일을 담당했을 때에도, 은퇴 이후 복지재단에서 노인 교육 프로그램을 기획했을 때에도
            제가 구성한 교육 프로그램을 통한 타인의 성장을 지켜보며 큰 보람을 느꼈습니다. 이런 경험을 토대로, 저는 더 많은 사람들의 성장을 도울 수 있는 기회를 찾고자 합니다. 25년이 넘는 시간동안 교육 프로그램 구성에 힘 써온 제 경력은 분명
            관련 직무를 수행하는 데 큰 도움이 될 것이라고 생각합니다. 시간과 사람의 변화에 뒤쳐지지 않고, 끊임없이 성장하는 사람으로서, 함께 성장하는 기회를 제공받고 싶습니다.

            
        Output1 :        
                 [꾸준한 성장에 함께하는 페이스메이커가 되겠습니다.] 
                저는 25년 이상 교육 프로그램을 기획하고 실행해온 경험을 갖고 있습니다. KT에서 14년 동안 인사 담당자로 근무하며 신입사원 교육 프로그램을 총괄했고, 은퇴 후에는 복지재단에서 노인 대상 교육 프로그램을 담당했습니다. 
                이 두 경험 모두에서 저는 교육 프로그램을 통해 참여자들의 성장을 이끌어내는 것에 큰 보람을 느꼈습니다. 변화하는 사회 트렌드에 빠르게 적응하며 항상 최신의 교육 방법을 도입해왔고, 이는 저를 지속적으로 성장하게 하는 원동력이 되었습니다. 
                이러한 배경은 저를 이 직무에 매우 적합한 후보로 만든다고 생각합니다. 귀 기관에서도 제가 축적한 경험과 지식을 활용하여 더 많은 사람들이 자신의 잠재력을 깨닫고 성장할 수 있도록 돕고 싶습니다. 
                흘러가는 시간 속에서도 늘 함께 성장하는 페이스메이커가 되고자 하는 저의 열정과 전문성이 귀 기관의 목표와 잘 부합할 것이라 확신합니다. 
                 
        
        Input 2: 
                경력 정보 : 1994년부터 2014년까지 20년간 도봉구 사회복지센터에서 사회복지사로 근무했어요. 사회복지센터 은퇴 후에는 2015년부터 2018년까지 도봉초등학교 방과후교실에서 돌봄교사로 일했고요.
                근무하는 동안 수많은 민원과 어려움을 마주했지만, 그럼에도 친절함을 잃지 않는 걸로 유명했어요. 직장에서 올해의 사회복지사 상을 타기도 했죠.
                본격적으로 아이들을 키우게 되면서 일을 그만두게 되었지만, 예전 기억을 살려 다시 한 번 열심히 일해보고 싶습니다.

                지원 동기 : 사람을 향한 정성과 애정은 개인과 지역사회에 긍정적인 변화를 가져올 수 있다고 믿습니다. 20년간 사회복지센터에서 근무하며 수많은 민원과 도전을 직면했음에도 사람에 대한 애정으로 항상
                친절함을 유지한 경험은 저를 인내심 있는 사회복지사로 성장하게 했습니다. 근무하는 동안 올해의 사회복지사 상을 수상하며 동료들과 지역사회에 긍정적인 영향을 끼쳐 왔다고 생각합니다. 은퇴 이후에 돌봄교사로 일하는 동안에도
                아이들과 상호작용하며 즐거움을 느꼈고, 이러한 경험을 통해 저는 사람을 애정 담아 대하는 것에 즐거움을 느끼고, 또 잘 해낼 수 있다는 것을 깨달았습니다. 제가 쌓아온 경험과 열정은 여전히 활기차고, 상호작용을 통해 사람과 세상을 밝히고 싶다는
                의지 역시 투철합니다. 사람과 지역사회에 긍정적인 변화를 가져올 수 있도록, 제가 다시 사회복지 현장에 몸담을 수 있는 귀중한 기회를 제공받고 싶습니다. 


        Output 2: [사랑과 진심으로 주변을 밝히는 사회복지사가 되겠습니다.]
                  저는 오랜 기간 사회복지사로 근무하며 어려운 상황에서도 친절을 잃지 않고 민원을 해결해왔습니다. 이 경험은 저를 더욱 인내심있는 사회복지사로 성장하게 했으며,
                  저와 마주한 수많은 민원인의 삶에도 긍정적인 영향을 미쳤다고 생각합니다. 은퇴 이후 돌봄교사로서 아이들과 함께 지낸 시간은 교육자로서의 경험을 쌓는 계기가 되었습니다.
                  이런 제 직업적 여정은 더욱 많은 사람들의 삶에 긍정적인 변화를 가져오고 싶다는 열망으로 이어졌습니다.

                  사회복지 현장으로 돌아가 사랑과 진심으로 주변을 밝히는 사람이 되고 싶습니다. 그간의 경험과 열정을 기반으로 더 많은 사람들의 어려움을 해결하고 돕고 싶습니다.
                  귀 기관에서 이런 목표를 실현하는 데 기여할 수 있는 기회를 갖게 되기를 희망합니다. 제가 이루고자 하는 바는 귀 기관의 비전과 매우 부합하며, 제 경력과 지식이 해당 직무에서 큰 자산이 될 것입니다.
                  
        
        위의 답변을 참고해줘. 아래는 사용자 응답 두 가지야. 두 가지 내용을 모두 고려해서 경력사항, 성격과 강점에 관한 이야기를 자기소개서에 잘 풀어 써 줘야해.
        사용자 경력 관련 정보 : {career}, 
        사용자 지원 동기 관련 정보 : {motivation}'''
    
    return model.generate_content(prompt)

def introduce2(career, personality, pre, model):
    prompt = f'''<<너의 역할은 사용자 응답 정보를 바탕으로 자기소개서 내용을 작성하는거야. 자기소개서 질문은 아래와 같아.
        (1) 성격과 강점 : 귀하의 성격과 강점을 서술하고, 이런 성격과 강점이 어떻게 조직에 도움이 될 수 있는지 설명해주세요.

        네가 답변을 작성할 때 "반드시" 유의해야 할 사항 몇 가지를 더 알려줄게 :
        - 답변을 작성할 때는, 경력 정보와 성격 정보를 모두 포함해서 작성해줘. 단, 경력 정보는 전체 문단의 30% 정도만 들어가면 좋겠어.
        - 유사한 내용이 반복되지 않도록 주의해줘. 또, 자소서의 이전 항목 작성 정보를 줄 테니 이것과 너무 유사하거나 중복되지 않도록 주의해줘. 
        - 경력 정보와 성격 정보를 완전히 분리해서 쓰기보다, 두 가지 정보를 조화롭게 섞어서 작성해줘. -
        - 가능하다면 답변은 공백 제외 350자 이상, 550자 이하가 되어야 해. 명심해!
        
        네가 작성한 내용은 실제 구직자의 이력서와 자기소개서가 되어 기업 인사 담당자에게 전달될거야. 그만큼 중요한 일이고.
        사용자 응답에서 질문에 대한 답변 정보를 찾을 수 없다면, 답을 만들어내지 말고 반드시 "정보 없음"이라고 답변해줘.
        자기소개서 항목을 작성할 때는, 사용자 답변 내용을 함축적으로 담을 수 있는 소제목을 꼭 설정해줘.>>
        
        Input1 :
            경력 정보 : 1995년부터 2008년까지 약 14년간 KT에서 인사 담당자로 근무했습니다. 
            사원에서 시작해서 팀장 직책까지 달았지요. 주로 신입사원 교육 프로그램 구성을 담당했습니다. 
            오랜 시간 근무한만큼 사회적 흐름도 빠르게 변화했는데, 변화의 물결에 뒤쳐지지 않는 프로그램 구성으로 인정받아왔습니다. 
            그 다음으로는 복지재단으로 옮겨 가서 5년간 강사로 일했어요. 거기서도 노인들을 대상으로 한 교육 프로그램을 구성하고 진행하는 역할을 담당했지요. 
            
            성격 정보 : 저는 융통성 있는 사람입니다. 빠르게 변화하는 세상에서도 뒤쳐지지 않고 늘 변화를 수용해왔지요. 이런 제 성격은 어디서 일을 하든 젊은 직원들과 융화되고 
            시대의 흐름에 맞는 것들을 기획하는 데 크게 도움이 될 것이라고 생각합니다. 제가 가진 경험과 지혜가 융통성을 만나면 큰 힘을 발휘할 수 있을 것이라고 생각해요. 
            
        Output1 :        
                 [20년의 세월과 융통성이 만나 지혜를 만든다]
                 저는 융통성 있는 사람입니다. KT에서 인사 담당자로 약 14년을 근무하는 동안에도, 변화하는 사회적 흐름에 뒤쳐지지 않고 적합한 신입사원 교육 프로그램을 구성해
                 능력을 인정받아 왔습니다. 늦은 나이에 젊은 사원들과 함께 근무를 해야 하는 입장에서, 이런 제 성격은 분명히 강점이 될 것이라고 생각합니다. 융통성 있고 포용력 높은 성격을 바탕으로
                 지난 20년의 세월동안 쌓아온 경험을 더해 지혜를 발휘할 수 있는 사원이 되겠습니다. 조직에 자연스럽게 융화되면서도 필요한 경험과 지혜를 줄 수 있는 저는
                 시대의 흐름에 발맞춰 나아가는 지원자입니다. 
        
        Input 2: 
                경력 정보 : 1994년부터 2014년까지 20년간 도봉구 사회복지센터에서 사회복지사로 근무했어요. 사회복지센터 은퇴 후에는 2015년부터 2018년까지 도봉초등학교 방과후교실에서 돌봄교사로 일했고요.
                근무하는 동안 수많은 민원과 어려움을 마주했지만, 그럼에도 친절함을 잃지 않는 걸로 유명했어요. 직장에서 올해의 사회복지사 상을 타기도 했죠.
                본격적으로 아이들을 키우게 되면서 일을 그만두게 되었지만, 예전 기억을 살려 다시 한 번 열심히 일해보고 싶습니다.

                성격 정보 : 저는 따뜻하고 다정한 사람이예요. 오랜 기간 사회복지사로 일하며 다양한 사람들을 상대해 온 만큼 사람들과 소통하는 것도 좋아하죠. 
                어떤 상황에서도 따뜻한 미소를 잃지 않고 사람을 진심으로 대할 자신이 있습니다. 제 경험과 성격이 일하는 공간을 따뜻하게 밝혀줄거라고 생각해요


        Output 2: [사람에 대한 따뜻한 진심으로 세상을 밝히다]
                  20년간 사회복지사로, 은퇴 이후에는 돌봄교실 교사로 일하며 다양한 사람들을 마주해왔습니다. 일하는 동안 수많은 민원과 어려움을 마주하는 순간도 있었지만,
                  그럴 때 마다 사람에 대한 제 진심과 따뜻한 성격은 빛을 발해 왔습니다. 친절함을 잃지 않는 사회복지사로 유명했던 저는, 직장에서 올해의 사회복지사 상을 타기도 했습니다.
                  이런 제 성격과 강점은 어디서든 큰 도움이 될 것이라고 생각합니다. 저는 사람과 소통하고 교류하는 것을 즐깁니다. 결국 세상은 사람과 사람간의 상호작용으로 이루어진 만큼, 
                  제 경험과 성격을 기반으로 제가 속해 있는 공간을 따뜻하게 밝힐 수 있는 사원이 되겠습니다.
        
        위의 답변을 참고해줘. 아래는 사용자 응답 두 가지야. 두 가지 내용을 모두 고려해서 경력사항, 성격과 강점에 관한 이야기를 자기소개서에 잘 풀어 써 줘야해.
        사용자 경력 관련 정보 : {career}, 
        사용자 성격 관련 정보 : {personality}
        자소서의 다른 항목 : {pre}'''
    
    return model.generate_content(prompt)



def prompting(key, car, motivation, personality):
    genai.configure(api_key=key)
    model = genai.GenerativeModel('gemini-pro')

    job = career(car, model).text.split(',')
    brief1 = introduce1(motivation, car, model).text
    brief2 = introduce2(car, personality,brief1, model).text

    return job, brief1, brief2 