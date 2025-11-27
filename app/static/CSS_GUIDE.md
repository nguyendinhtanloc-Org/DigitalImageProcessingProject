# Custom CSS Examples for Streamlit

Streamlit hỗ trợ custom CSS thông qua `st.markdown()` với `unsafe_allow_html=True`.

## Cách 1: External CSS File (Recommended)

Tạo file `static/styles.css` và load trong app:

```python
from pathlib import Path

def load_css():
    css_file = Path(__file__).parent / "static" / "styles.css"
    with open(css_file) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css()
```

## Cách 2: Inline CSS

```python
st.markdown("""
<style>
.custom-class {
    color: #ff0000;
    font-size: 20px;
}
</style>
""", unsafe_allow_html=True)
```

## Cách 3: CSS cho Streamlit Components

```python
# Custom button
st.markdown("""
<style>
.stButton > button {
    background-color: #4CAF50;
    color: white;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)
```

## Useful CSS Classes

Các class CSS của Streamlit có thể target:

- `.stButton > button` - Buttons
- `.stTextInput > div > div > input` - Text inputs
- `.stSelectbox` - Select boxes
- `.stProgress > div > div` - Progress bars
- `.stAlert` - Alert boxes
- `.main` - Main container

## Dark Mode Support

```css
@media (prefers-color-scheme: dark) {
    .custom-class {
        color: #ffffff;
        background-color: #333333;
    }
}
```

## Responsive Design

```css
@media (max-width: 768px) {
    h1 {
        font-size: 1.5rem;
    }
}
```

## Tips

1. Sử dụng `!important` nếu CSS không apply (Streamlit có CSS mạnh)
2. Inspect element (F12) để tìm class names của Streamlit
3. Test trên nhiều browsers
4. Dùng external CSS file cho dễ maintain
