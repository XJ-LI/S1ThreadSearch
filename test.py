import json
import re
from utils import get_posts, parse_html_filtered_posts, save_output

config = json.load(open('./config.json', 'r', encoding='utf-8'))

payload = {
    'username': config['payload']['username'],
    'password': config['payload']['password']
}
page_num = config['page_number']
target_url = config['target_url']
login_url = 'https://stage1st.com/2b/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1'
keywords = config['keywords']








# main loop
replyList = []

for i in range(1, page_num + 1):
    url = f'thread-{target_url}-{i}-1.html'
    html = get_posts(login_url, [url], payload)[0]
    
    # Manually insert the current page number
    replyList.append(i)

    # Filter the page and append relevant posts
    filtered_replies = parse_html_filtered_posts([html], keywords)

    # Only filtered posts are included; no need to repeat the page number
    for reply in filtered_replies:
        if isinstance(reply, str):  # skip the page number if somehow included
            replyList.append(reply)

print("Filtered, Generating HTML File...")
save_output(replyList, f"{target_url}-{page_num}")
