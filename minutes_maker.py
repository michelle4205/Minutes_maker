import streamlit as st
import openai
import os
from docx import Document

# 환경 변수 설정(Windows)
# setx OPENAI_API_KEY "my_secret_key"

# 환경 변수에서 API 키 읽기
os.environ["OPENAI_API_KEY"] = "my_secret_key"

openai.api_key = os.getenv("OPENAI_API_KEY")  # 또는 직접 API 키 입력

if openai.api_key is None:
    st.error("OpenAI API key is not set in environment variables.")
    raise ValueError("OpenAI API key is not set in environment variables.")

# 사이드바 제목
st.sidebar.title("Minutes maker")

# 로고 이미지 로컬 파일에서 불러오기
logo_path = "m.png" # 로고 이미지 경로
st.sidebar.image(logo_path, use_column_width=True) 

# 페이지 제목
st.markdown("<h1 style='text-align: center; color: Grey;'>회의록 작성 서비스</h1>", unsafe_allow_html=True)

# 회의 데이터 업로드 섹션
st.sidebar.header('파일 업로드')
uploaded_file = st.sidebar.file_uploader("파일 선택", type=['txt', 'docx'])

# 사이드바 배경 색상
st.sidebar.markdown(
    """
    <style>
    .css-1aumxhk {
        background-color: #f0f2f6;
    }
    </style>
    """, unsafe_allow_html=True
)

# 회의록 생성 버튼
if st.sidebar.button('회의록 생성'):
    if uploaded_file is not None:
        if uploaded_file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            # Word 파일 처리
            doc = Document(uploaded_file)
            file_content = "\n".join([para.text for para in doc.paragraphs])
        else:
            # 텍스트 파일 처리
            file_content = uploaded_file.read().decode('utf-8')
        
        # GPT API를 사용해 회의록 생성
        client = openai.OpenAI(api_key = openai.api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # 또는 "gpt-4" 모델 사용 가능
            messages=[
                {"role": "system", "content": "당신은 공공기관의 회의록 작성 도우미입니다."},
                {"role": "user", "content": f"회의 내용:\n{file_content}\n\n회의록:"} # 도대체 무슨 문법으로 돌아가는거냐... 공부 필요
            ],
            max_tokens=300,  # 요약문의 최대 길이 설정                temperature=0.5,  # 창의성 조절 (0.0-1.0)
            )
        generated_minutes = response.choices[0].message.content
        total_bill = response.usage.prompt_tokens * 0.0015/1000 + response.usage.completion_tokens * 0.002/1000
        st.session_state['generated_minutes'] = generated_minutes
        st.success('회의록이 성공적으로 생성되었습니다.')

    else:
        st.warning('먼저 파일을 업로드하세요.')

# 생성된 회의록 표시 섹션
st.header('회의록')
if 'generated_minutes' in st.session_state:
    st.text_area('회의록 내용', st.session_state['generated_minutes'], height=300)
else:
    st.text_area('회의록 내용', '회의록 내용이 여기에 표시됩니다', height=300)

# 페이지 하단 배경 색상
st.markdown(
    """
    <style>
    .css-1lcbmhc {
        background-color: #f0f2f6;
    }
    </style>
    """, unsafe_allow_html=True
)
