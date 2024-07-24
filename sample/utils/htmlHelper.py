def addHtmlHeader(st):
    with open("css/codegame.css", "r") as css_file:
        css = css_file.read()
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    with open("html/styles-link.html", "r") as styles_link:
        html_styles = styles_link.read()
    st.markdown(html_styles, unsafe_allow_html=True)
    with open("html/header.html", "r") as header_html:
        html_header = header_html.read()
    st.markdown(html_header, unsafe_allow_html=True)
    st.markdown("<div class='wk-auto-header'>WoltersKluwer Autonomous Testing Assistant</div>", unsafe_allow_html=True)
    st.markdown(
        "<div class='wk-auto-subheader'>Powered by MAS (Multi Agent System of Autonomous AI Agents), This will help you with designing and executing test cases for API and User Interface. It supports validations, Functional and Error handling testing</div>",
        unsafe_allow_html=True)
    print(f"loaded html")
