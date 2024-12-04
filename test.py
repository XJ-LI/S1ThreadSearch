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
login_url = 'https://bbs.saraba1st.com/2b/member.php?mod=logging&action=login&loginsubmit=yes&infloat=yes&lssubmit=yes&inajax=1'
keywords = config['keywords']








# main loop
urlList = []
for i in range(1,page_num+1):
    url = f'thread-{target_url}-{i}-1.html'
    urlList.append(url)
    
htmlList = get_posts(login_url, urlList, payload)    
print("All Required Pages Retrieved.")
replyList = parse_html_filtered_posts(htmlList, keywords)
print("Filtered, Generating HTML File...")
# Output
save_output(replyList, str(target_url)+'-'+str(page_num))