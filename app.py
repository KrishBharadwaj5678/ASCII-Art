import streamlit as st
from ascii_magic import AsciiArt
import re
import pyfiglet as p

st.set_page_config(
    page_title="ASCII Art",
    page_icon="icon.png",
    menu_items={
        "About":"Convert your text and images into stunning ASCII art with ease. ASCII Art provides a simple and intuitive way to create beautiful text-based art and image representations."
    }
)

st.write("<h2 style='color:#DA4C5C;font-size:34px;'>Your Portal to ASCII Art Creation</h2>",unsafe_allow_html=True)

tab1,tab2=st.tabs(["Text To ASCII","Image To ASCII"])

with tab1:
    text=st.text_input("Enter Text",placeholder="Lorem Ipsum")
    font=st.selectbox("Select Font",["big","banner3","5lineoblique","alphabet","acrobatic","banner","basic","bell","block","bubble","bulbhead","coinstak","colossal","contessa","cricket","cyberlarge","cybermedium","digital","doh","doom","dotmatrix","epic","fender","fourtops","invita","isometric1","isometric2","isometric3","isometric4","marquee","mini","nipples","ogre","pawp","pebbles","puffy","roman","rounded","shadow","short","slant","speed","standard","starwars","stop","tinker-toy","twopoint","univers"])

    btn1=st.button("Generate",key=1)

    if "load_state" not in st.session_state:
        st.session_state.load_state=False

    if btn1 or st.session_state.load_state:
        st.session_state.load_state=True
        ascii_txt=p.figlet_format(text=text,font=font)
        st.code(ascii_txt)

with tab2:
    upd_opt=st.radio("Choose Upload Option",["File Upload","Via URL"])
    if upd_opt=="File Upload":
        file=st.file_uploader("Upload File",type=["png","jpeg"])
    else:
        url=st.text_input("Enter Image URL",placeholder="https://picsum.photos/200/300")

    btn2=st.button("Generate",key=2)

    if btn2:
        if upd_opt:
            image=AsciiArt.from_image(file) if upd_opt=="File Upload" else AsciiArt.from_url(url)

            try:
                with st.spinner("Processing, please wait..."):
                    # Html File
                    image.to_html_file('ascii_art.html', columns=300, width_ratio=2)
                    # Text File
                    data=image.to_terminal(100,2)
                    def remove_ansi_escape_codes(text):
                        ansi_escape = re.compile(r'\x1B[@-_][0-?]*[ -/]*[@-~]')
                        return ansi_escape.sub('', text)
                    clean_output = remove_ansi_escape_codes(data)

                    with open('ascii_art.txt',"w") as file:
                        file.write(clean_output)

                    with open('ascii_art.html',"r") as file:
                        st.download_button("Download (html)",file.read(),"ascii_art.html")

                    with open('ascii_art.txt',"r") as file:
                        st.download_button("Download (txt)",file.read(),"ascii_art.txt")
            except:
                st.error("Something Went Wrong :(")