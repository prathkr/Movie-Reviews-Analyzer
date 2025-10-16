import streamlit as st
from google import genai


client = genai.Client(api_key="YOUR_API_KEY_HERE")

st.set_page_config(page_title="Movie Reviews Analyzer", page_icon="🎬", layout="centered")

st.title("🎬 Movie Reviews Analyzer")
st.markdown("*Get AI-powered summaries for any movie*")
st.divider()

movie_name = st.text_input("Enter a movie name:", placeholder="e.g., Oppenheimer, Dune")

if st.button("Analyze", use_container_width=True, type="primary"):
    if not movie_name.strip():
        st.error("Please enter a movie name")
    else:
        try:
            with st.spinner("Analyzing reviews..."):
                prompt = f"""You are a movie review summarizer. Analyze and summarize Reviews for the movie \"{movie_name}\". Provide:
1. Overall sentiment (positive/mixed/negative)
2. Key themes praised by reviewers
3. Common criticisms or concerns
4. Any patterns in ratings (e.g., most reviews are 4 stars, etc.).
5. Summary of what audiences think
Keep it concise and informative."""
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )
                st.success("Analysis complete!")
                import re
                rating_match = re.search(r"(\d(?:\.\d)?)\s*stars", response.text, re.IGNORECASE)
                stars = None
                if rating_match:
                    try:
                        rating = float(rating_match.group(1))
                        full_stars = int(rating)
                        half_star = rating - full_stars >= 0.5
                        stars = "".join(["⭐" for _ in range(full_stars)])
                        if half_star:
                            stars += "✬"  
                        stars += "☆" * (5 - full_stars - (1 if half_star else 0))
                    except Exception:
                        stars = None
                if stars:
                    st.markdown(f"#### Rating: {stars}")
                st.markdown(f"### Reviews for \"{movie_name}\"")
                st.info(response.text)
        except Exception as e:
            st.error(f"Error: {str(e)}")
