import requests
from bs4 import BeautifulSoup
import re

# Function to log in and retrieve the desired web pages to be processed
def get_posts(login_url, urlList, payload):
    htmlList = []
    # Start session
    session = requests.Session()
    # Login
    response = session.post(login_url, data=payload)
    
    # Request all post pages in target's homepage
    for i in range(len(urlList)):
        protected_url = "https://bbs.saraba1st.com/2b/" + urlList[i]
        # Check if login was successful
        if response.status_code == 200:
            # Now request the protected page
            response = session.get(protected_url)
            # Check if the request was successful
            if response.status_code == 200:
                # Parse the HTML content
                soup = BeautifulSoup(response.text, 'html.parser')
                if soup:
                    htmlList.append(soup)
                else:
                    print(f"Failed to retrieve the protected page. Status code: {response.status_code}")
        else:
            print(f"Failed to log in. Status code: {response.status_code}")
    return htmlList
    
    
# for each webpage retrieve filtered info
def parse_html_filtered_posts(htmlList, keywords):
    replyList = []
    
    # Regular expressions to match all posts
    author_pattern = r'<a class="xw1" href="space-uid-\d+.html" target="_blank">.*?</a>'
    time_pattern = r'<em id="authorposton\d+">.*?</em>'
    content_pattern = r'<td class="t_f" id="postmessage_\d+">.*?<div class="cm" id="comment_\d+">'
    
    # Iterate through the HTML content
    count = 1
    for html in htmlList:
        replyList.append(count)
        html = str(html)
        html = html.replace('<div class="locked">提示: <em>作者被禁止或删除 内容自动屏蔽</em></div>', '<td class="t_f" id="postmessage_000000">提示: 作者被禁止或删除 内容自动屏蔽</td></tr></table></div><div class="cm" id="comment_000000">')
        
        # Extract all authors
        authors = re.findall(author_pattern, html, re.DOTALL)
        # Extract all timestamps
        times = re.findall(time_pattern, html, re.DOTALL)
        # Extract all content blocks
        contents = re.findall(content_pattern, html, re.DOTALL)
        
        # Combine the extracted time and content for each post
        for author, time, content in zip(authors, times, contents):
            reply = author + '<p>' + time + '</p>' + '<p>' + content + '</p>'
            # Check if any keyword from the list is in the content
            if any(keyword in content for keyword in keywords):
                replyList.append(reply)
        if replyList[-1] == count:
            replyList.pop()
        count += 1
    return replyList


def save_output(replyList, tid):
    title = 'Filtered Results'
    beginner = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
    </head>
    <body>
    """

    ender = """
    </body>
    </html>
    """

    output = beginner
    for reply in replyList:
        if isinstance(reply, int):  # Check if the reply is a page number
            # Add the page number in bold
            output += f"<b>Page {reply}: </b><hr/>"
        else:
            # Add the reply as is
            output += reply + "<hr/>"
    output = output + ender

    # Replace relative_path with full_path
    pattern = r"forum.php\?mod=attachment"
    replace = "https://bbs.saraba1st.com/2b/forum.php?mod=attachment"
    output = re.sub(pattern, replace, output)
    # fix user page link
    pattern = r"space-uid-\d+\.html"
    replace = r"https://bbs.saraba1st.com/2b/\g<0>"
    output = re.sub(pattern, replace, output)

    # Write the HTML content to a file
    with open(f'{tid}.html', 'w', encoding='utf-8') as file:
        file.write(output)