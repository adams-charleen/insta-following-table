import os

# Define input and output paths
input_file = '/Users/charleenadams/scraping_insta/instagram_following.txt'
output_file = '/Users/charleenadams/scraping_insta/instagram_following_table.html'

# Read the data from the file
data = {}
with open(input_file, 'r') as file:
    for line in file:
        if ':' in line:
            account, following = line.split(':', 1)
            account = account.strip()
            # Clean up the following list: remove brackets and split into list
            following = following.strip().strip('[]').replace("'", "").split(', ')
            data[account] = following

# Create HTML content with CSS styling
html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Instagram Following Table</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }
        th, td {
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }
        th {
            background-color: #f2f2f2;
            color: #333;
        }
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        tr:hover {
            background-color: #f1f1f1;
        }
        .following-list {
            max-height: 100px;
            overflow-y: auto;
            display: block;
        }
    </style>
</head>
<body>
    <h2>Instagram Following Data - March 30, 2025</h2>
    <table>
        <tr>
            <th>Account</th>
            <th>Following</th>
        </tr>
"""

# Add rows to the table
for account, following in data.items():
    following_html = "<div class='following-list'>" + "<br>".join(following) + "</div>"
    html_content += f"""
        <tr>
            <td>{account}</td>
            <td>{following_html}</td>
        </tr>
    """

# Close the HTML
html_content += """
    </table>
</body>
</html>
"""

# Write to the output file
with open(output_file, 'w') as file:
    file.write(html_content)

print(f"HTML table saved to {output_file}")
