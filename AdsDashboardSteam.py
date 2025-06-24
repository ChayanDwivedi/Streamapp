import streamlit as st
import pandas as pd
import urllib.request
import base64

# Set wide layout and page title
st.set_page_config(page_title="Ads Dashboard", page_icon="📊",layout="wide")

st.title("📊 Ads Dashboard")

# Load the data
@st.cache_data
def load_data():
    return pd.read_excel("AdsData_with_mediaType.xlsx")

@st.cache_data
def fetch_image_base64(url):
    image_bytes = urllib.request.urlopen(url).read()
    return base64.b64encode(image_bytes).decode()

df = load_data()
df['CPV'].fillna('',inplace=True)
df['CPL'].fillna('',inplace=True)
# df['CPV'] = df['CPV'].replace('nan','')
# df['CPL'] = df['CPL'].replace('nan','')

# Clean column names
df.columns = df.columns.str.strip()

# Sort by Visitor Count descending
df = df.sort_values(by='visitors Count', ascending=False)

# Get unique projects
projects = sorted(df['project'].dropna().unique().tolist())

# Tab level 1: Projects
project_tabs = st.tabs(projects)

for i, project in enumerate(projects):
    with project_tabs[i]:
        st.session_state.project = project
        filtered_project = df[df['project'] == project]

        # Tab level 2: Platforms within this project
        platforms = sorted(filtered_project['platform'].dropna().unique().tolist())
        platform_tabs = st.tabs(platforms)

        for j, platform in enumerate(platforms):
            with platform_tabs[j]:
                st.session_state.platform = platform
                filtered_platform = filtered_project[filtered_project['platform'] == platform]

                st.subheader(f"{project} - {platform}")

                # Show table
                st.markdown("### 📌 Creative Details")
                table_df = filtered_platform[['cId', 'Lead Count', 'visitors Count', 'amountSpent', 'CPV', 'CPL']]
                st.dataframe(table_df.reset_index(drop=True), use_container_width=True)

                # Show creatives
                st.markdown("---")
                st.subheader("🖼️ Creative Previews")

                creative_links = filtered_platform[
                    ['FinalCreativeLink', 'cId', 'Lead Count', 'visitors Count', 'amountSpent', 'CPV', 'CPL', 'mediaType']
                ].dropna(subset=['FinalCreativeLink', 'mediaType'])

                cols_per_row = 4

                for i in range(0, len(creative_links), cols_per_row):
                    row = st.columns(cols_per_row)
                    for j, col in enumerate(row):
                        if i + j < len(creative_links):
                            row_data = creative_links.iloc[i + j]
                            creative_url = row_data['FinalCreativeLink']
                            cid = row_data['cId']
                            media_type = row_data['mediaType'].lower()

                            leads = row_data['Lead Count']
                            visitors = row_data['visitors Count']
                            spent = row_data['amountSpent']
                            cpv = row_data['CPV']
                            cpl = row_data['CPL']

                            try:
                                if media_type.startswith('video'):
                                    content_html = f"""
                                    <div style="border:1px solid #ccc; padding:10px; border-radius:10px; text-align:center;">
                                        <h6 style="margin-bottom:5px;">URL: {cid}</h6>
                                        <video width="100%" height="250" controls style="border-radius: 8px; box-shadow: 2px 2px 8px #aaa;">
                                            <source src="{creative_url}" type="{media_type}">
                                            Your browser does not support the video tag.
                                        </video>
                                        <p style="font-size:20px;">
                                            Leads: {leads}<br>
                                            Visitors: {visitors}<br>
                                            Spent: ₹{spent}<br>
                                            CPV: ₹{cpv}<br>
                                            CPL: ₹{cpl}
                                        </p>
                                        <a href="{creative_url}" download="{cid}.mp4">📥 Download Video</a>
                                    </div>
                                    """
                                    col.markdown(content_html, unsafe_allow_html=True)

                                elif media_type.startswith('image'):
                                    encoded = fetch_image_base64(creative_url)
                                    ext = media_type.split('/')[-1]

                                    content_html = f"""
                                    <div style="border:1px solid #ccc; padding:10px; border-radius:10px; text-align:center;">
                                        <h6 style="margin-bottom:5px;">URL: {cid}</h6>
                                        <a href="{creative_url}" target="_blank">
                                            <img src="{creative_url}" alt="Creative" width="250" height="250" style="border-radius: 8px; box-shadow: 2px 2px 8px #aaa;" />
                                        </a>
                                        <p style="font-size:20px;">
                                            Leads: {leads}<br>
                                            Visitors: {visitors}<br>
                                            Spent: ₹{spent}<br>
                                            CPV: ₹{cpv}<br>
                                            CPL: ₹{cpl}
                                        </p>
                                        <a href="data:{media_type};base64,{encoded}" download="{cid}.{ext}">📥 Download Image</a>
                                    </div>
                                    """
                                    col.markdown(content_html, unsafe_allow_html=True)

                                else:
                                    col.warning(f"⚠️ Unsupported media type for CID {cid}: {media_type}")
                            except Exception as e:
                                col.warning(f"❌ Error loading creative for CID {cid}: {e}")





# import streamlit as st
# import pandas as pd
# import urllib.request
# import base64

# # Load the data
# @st.cache_data
# def load_data():
#     # Replace this with your actual data source if dynamic
#     return pd.read_excel("AdsData_with_mediaType.xlsx")

# import mimetypes

# # def guess_content_type(url):
# #     type_guess, _ = mimetypes.guess_type(url)
# #     return type_guess or 'application/octet-stream'

# df = load_data()

# st.set_page_config(page_title="Ads Dashboard", layout="wide")

# st.title("📊 Ads Dashboard")

# # Clean column names
# df.columns = df.columns.str.strip()

# # Sort by Visitor Count descending
# df = df.sort_values(by='visitors Count', ascending=False)

# # Get unique projects
# projects = list(set(df['project'].to_list()))


# # Tab level 1: Projects
# project_tabs = st.tabs(projects)

# for i, project in enumerate(projects):
#     with project_tabs[i]:
#         st.session_state.project = project
#         filtered_project = df[df['project'] == project]

#         # Tab level 2: Platforms within this project
#         platforms = list(set(filtered_project['platform'].to_list()))
#         platform_tabs = st.tabs(platforms)

#         for j, platform in enumerate(platforms):
#             with platform_tabs[j]:
#                 st.session_state.platform = platform
#                 filtered_platform = filtered_project[filtered_project['platform'] == platform]

#                 st.subheader(f"{project} - {platform}")

#                 # Show table
#                 st.markdown("### 📌 Creative Details")
#                 table_df = filtered_platform[['cId', 'Lead Count', 'visitors Count', 'amountSpent', 'CPV', 'CPL']]
#                 st.dataframe(table_df.reset_index(drop=True), use_container_width=True)

#                 # Show creatives
#                 st.markdown("---")
#                 st.subheader("🖼️ Creative Previews")

#                 creative_links = filtered_platform[['FinalCreativeLink', 'cId', 'Lead Count', 'visitors Count', 'amountSpent', 'CPV', 'CPL']].dropna()
#                 cols_per_row = 4  # Changed from 3 to 4
#                 for i in range(0, len(creative_links), cols_per_row):
#                     row = st.columns(cols_per_row)
#                     for j, col in enumerate(row):
#                         if i + j < len(creative_links):
#                             row_data = creative_links.iloc[i + j]
#                             creative_url = row_data['FinalCreativeLink']
#                             cid = row_data['cId']
#                             try:
#                                 # Detect MIME type using HEAD
#                                 request = urllib.request.Request(creative_url, method='HEAD')
#                                 response = urllib.request.urlopen(request, timeout=5)
#                                 content_type = response.info().get_content_type()
#                                 # content_type = guess_content_type(creative_url)

#                                 leads = row_data['Lead Count']
#                                 visitors = row_data['visitors Count']
#                                 spent = row_data['amountSpent']
#                                 cpv = row_data['CPV']
#                                 cpl = row_data['CPL']

#                                 # Build content box HTML
#                                 if content_type.startswith('video'):
#                                     content_html = f"""
#                                     <div style="border:1px solid #ccc; padding:10px; border-radius:10px; text-align:center;">
#                                         <h6 style="margin-bottom:5px;">CID: {cid}</h6>
#                                         <video width="100%" height="250" controls style="border-radius: 8px; box-shadow: 2px 2px 8px #aaa;">
#                                             <source src="{creative_url}" type="{content_type}">
#                                             Your browser does not support the video tag.
#                                         </video>
#                                         <p style="font-size:25px;">
#                                             Leads: {leads} | Visitors: {visitors}<br>
#                                             Spent: ₹{spent} | CPV: ₹{cpv} | CPL: ₹{cpl}
#                                         </p>
#                                         <a href="{creative_url}" download="{cid}.mp4">📥 Download Video</a>
#                                     </div>
#                                     """
#                                     col.markdown(content_html, unsafe_allow_html=True)

#                                 elif content_type.startswith('image'):
#                                     image_bytes = urllib.request.urlopen(creative_url).read()
#                                     encoded = base64.b64encode(image_bytes).decode()
#                                     ext = content_type.split('/')[-1]

#                                     content_html = f"""
#                                     <div style="border:1px solid #ccc; padding:10px; border-radius:10px; text-align:center;">
#                                         <h6 style="margin-bottom:5px;">CID: {cid}</h6>
#                                         <a href="{creative_url}" target="_blank">
#                                             <img src="{creative_url}" alt="Creative" width="100%" height="150" style="border-radius: 8px; box-shadow: 2px 2px 8px #aaa;" />
#                                         </a>
#                                         <p style="font-size:25px;">
#                                             Leads: {leads} | Visitors: {visitors}<br>
#                                             Spent: ₹{spent} | CPV: ₹{cpv} | CPL: ₹{cpl}
#                                         </p>
#                                         <a href="data:{content_type};base64,{encoded}" download="{cid}.{ext}">📥 Download Image</a>
#                                     </div>
#                                     """
#                                     col.markdown(content_html, unsafe_allow_html=True)

#                                 else:
#                                     col.warning(f"Unsupported media type for CID {cid}: {content_type}")

#                             except Exception as e:
#                                 col.warning(f"❌ Error loading creative for CID {cid}: {e}")


                